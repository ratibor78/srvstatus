#! /usr/bin/env python


# Getting SystemD services status and uptime
# Alexey Nizhegolenko 2018


import os
import re
import json
import subprocess
import configparser
import parsedatetime
from datetime import datetime


def service_stat(service):
    out = subprocess.Popen(["systemctl", "status", service], stdout=subprocess.PIPE) # NOQA
    output, err = out.communicate()

    service_regx = r"Loaded:.*\/([^ ]*);"
    status_regx = r"Active:(.*) since (.*);(.*)"
    status_regx_fail = r"Active:(.*) ([^ ]+) since (.*);(.*)"

    service_status = {}
    output = output.decode("utf-8")
    for line in output.splitlines():
        # Match string like: name.service - Some Application Decription
        try:
            service_search = re.search(service_regx, line)
        except Exception as er:
            continue
        if service_search:
            service_status['service'] = service_search.group(1)
            continue
        # Match string like: Active: inactive (dead) since Wed 2018-09-19 10:57:30 EEST; 4min 26s ago  # NOQA
        status_search = re.search(status_regx, line)
        status_search_f = re.search(status_regx_fail, line)

        if status_search:
            status = status_search.group(1).strip()
            status_fail = status_search_f.group(1).strip()
            if status == 'active (running)':
                service_status['status'] = 1
            elif status == 'inactive (dead)':
                service_status['status'] = 3
            elif status_fail == 'failed':
                service_status['status'] = 4
            else:
                service_status['status'] = 0

            # Get and convert "since" date in to seconds
            since_date = status_search.group(2).strip()
            cal = parsedatetime.Calendar()
            time_struct, parse_status = cal.parse(since_date)
            delta = datetime.now() - datetime(*time_struct[:6])
            seconds = delta.total_seconds()
            service_status['status_time'] = int(seconds)
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
