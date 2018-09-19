#! /usr/bin/env python


# Getting SystemD services status and uptime
# Alexey Nizhegolenko 2018


import os
import re
import json
import subprocess
import configparser


def service_stat(service):
    out = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE) # NOQA
    output, err = out.communicate()

    service_regx = r"Loaded:.*\/(.*service);"
    status_regx = r"Active:(.*) since (.*);(.*)"

    service_status = {}

    for line in output.splitlines():
        # Match string like: name.service - Some Application Decription
        service_search = re.search(service_regx, line)
        if service_search:
            service_status['service'] = service_search.group(1)
            continue
        # Match string like: Active: inactive (dead) since Wed 2018-09-19 10:57:30 EEST; 4min 26s ago  # NOQA
        status_search = re.search(status_regx, line)
        if status_search:
            service_status['status'] = status_search.group(1).strip()
            service_status['since'] = status_search.group(2).strip()
            service_status['status_time'] = status_search.group(3).strip()
            break

    return service_status


if __name__ == '__main__':

    def main():

        os.environ["LC_ALL"] = "C"

        # Getting params from config
        pwd = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        config = configparser.ConfigParser()
        config.read('%s/settings.ini' % pwd)

        services = config.get('SERVICES', 'name').split()

        # Run loop with service63s
        output = []
        for name in services:
            output.append(service_stat(name))
        print(json.dumps(output))

    try:
        main()
    except KeyboardInterrupt:
        os.system('clear')
