# SRVSTATUS

## version 1.0

## Getting status of the SystemD services using Telegraf with InfluxDB & Grafana

![Alt text](https://github.com/ratibor78/servicestat/blob/master/services_grafana.png?raw=true "Grafana dashboard example")
![Alt text](https://github.com/ratibor78/servicestat/blob/master/services_grafana1.png?raw=true "Grafana dashboard example")

## New features in version 1.0
 - Added more statuses
 - Fixed bugs with empty output when the systemd services was not found
 - tested and moved to the Python3


The main goal of this python3 script, checking the list of the given SystemD services and sending their statuses
in to the InfluxDB database, so you can use them for the Grafana dashboards.

The script is written on python and I tried to use standard lib's as much as possible,
but you still need run pip install.


  This script send a JSON format with services statuses coded by digits:
```
  active (running) = 1
  active (exited) = 2
  inactive (dead) = 3
  failed  = 4
  no match = 0
```  
  so you need to convert it back to string in Grafana.
  You can take a look on my test Grafana dashboard to see how it may be done.

  Actually the last Telegraf version accepts the string values in JSON format,
  but if you want to use Grafana alerting you still need a numeric format to put it on alert graphs then.

  Also script provide a service name and time recent service status in seconds,
  so you can use it in Grafana dashboards also.

  You can find the Grafana dashboard example in service_status.json file or on grafana.com:https://grafana.com/dashboards/8348

  There are also a very pretty Grafana dashboard example https://grafana.com/grafana/dashboards/13309 from https://github.com/b4b857f6ee

## Installation

```
$ cd /opt && git clone https://github.com/ratibor78/srvstatus.git
$ cd /opt/srvstatus
$ python3 -m venv venv && source venv/bin/activate
$ pip3 install -r requirements.txt
$ chmod +x ./service.py
```

  Rename **settings.ini.back** to **settings.ini** and specify a list of services that you need to check in one string
  separated with spaces:

```
   [SERVICES]
    name = docker.service nginx.service
```
  You can also add your own **user services** list same to (systemctl --user some.service):

```
   [USER_SERVICES]
    name = syncthing.service
```

Then configure the telegraf **exec** plugin this way:

```
    [[inputs.exec]]

    commands = [
     "/opt/srvstatus/venv/bin/python3 /opt/srvstatus/service.py"
    ]

    timeout = "5s"
    name_override = "services_stats"
    data_format = "json"
    tag_keys = [
      "service"
    ]
```
That's all, now you can create nice and pretty Grafana dashboards for system services with alerting.

Good luck.

License
----

MIT

**Free Software, Hell Yeah!**
