from django_rq import job
from ua_parser import user_agent_parser

from .models import Entry
from .utils import get_ip_data, get_shodan_data


@job
def parse_data(entry_pk, data):
    parsed = {
        'headers': {},
        'ipinfo': {},
        'browser': {},
        'cookies': [],
        'shodan': {}
    }

    # Headers
    for key in data['headers']:
        if key == 'Cookie':
            parsed['cookies'] = list(map(
                lambda x: x.strip(), data['headers'][key].split(';')
            ))
            continue

        parsed['headers'][key] = data['headers'][key]

    # IP Data
    ip = data['ip']
    if ip:
        parsed['ipinfo'] = get_ip_data(ip)
        parsed['shodan'] = get_shodan_data(ip)

    # User-Agent
    parsed['user_agent'] = user_agent_parser.Parse(
        data['headers'].get('User-Agent', '')
    )

    entry = Entry.objects.get(pk=entry_pk)
    entry.data = parsed
    entry.save()
