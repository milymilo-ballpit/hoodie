import json

import ipinfo as ipinfo_lib
import shodan as shodan_lib

from django.conf import settings

ipinfo = ipinfo_lib.getHandler(settings.IPINFO_TOKEN)
shodan = shodan_lib.Shodan(settings.SHODAN_TOKEN)


def get_ip_data(ip_address):
    data = ipinfo.getDetails(ip_address)
    return data.all


def get_shodan_data(ip_address):
    data = shodan.host(ip_address)
    print(json.dumps(data))
    return data


get_shodan_data("205.186.132.78")
