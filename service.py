#! /usr/bin/env python

import os
import re
import subprocess
import configparser


def service_stat(service):
    out = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE) # NOQA
    output, err = out.communicate()
    # output = output.decode('utf-8')

    service_regx = r"Loaded:.*\/(.*service);"
    status_regx = r"Active:(.*) since (.*);(.*)"

    service_status = {}

    for line in output.splitlines():
        service_search = re.search(service_regx, line)
        status_search = re.search(status_regx, line)

        if service_search:
            service_status['service'] = service_search.group(1)
            # print("service:", service)
        elif status_search:
            service_status['status'] = status_search.group(1).strip()
            # print("status:", status.strip())
            service_status['since'] = status_search.group(2).strip()
            # print("since:", since.strip())
            service_status['uptime'] = status_search.group(3).strip()
            # print("uptime:", uptime.strip())

    return service_status


if __name__ == '__main__':

    def main():

        os.environ["LC_ALL"] = "C"

        # Getting params from config
        pwd = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        config = configparser.ConfigParser()
        config.read('%s/settings.ini' % pwd)

        services = config.get('SERVICES', 'name').split()
        for name in services:
            result = service_stat(name)
            print(result)

    try:
        main()
    except KeyboardInterrupt:
        os.system('clear')
