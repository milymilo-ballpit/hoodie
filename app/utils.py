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
    return _extract_shodan_data(data)


def _extract_shodan_data(d):
    extracted = {
        "last_update": d["last_update"],
        "vulns": d["vulns"],
        "domains": d["domains"],
        "ports": sorted(d["ports"]),
        "os": d["os"],
        "services": [],
    }

    for s in d["data"]:
        se = {
            "module": s["_shodan"]["module"],
            "product": s.get("product", None),
            "port": s["port"],
            "transport": s["transport"],
        }

        if "http" in s:
            se["http"] = {
                "host": s["http"]["host"],
                "location": s["http"]["location"],
                "server": s["http"]["server"],
                "title": s["http"]["title"],
                "robots": s["http"]["robots"],
                "components": s["http"]["components"]
            }

        if "dns" in s:
            se["dns"] = {
                "resolver_hostname": s["dns"]["resolver_hostname"],
                "recursive": s["dns"]["recursive"],
                "software": s["dns"]["software"],
            }

        if "ftp" in s:
            se["ftp"] = {
                "anonymous": s["ftp"]["anonymous"]
            }

        extracted["services"].append(se)

    return extracted
