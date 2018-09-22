# Servicestat

## version 0.1

## Status of SysteD services for Telegraf+InfluxDB

  Main goal of this short script is checking list of given SystemD services 
  and sending this services status with UP/DOWN time in to InfluxDB and Grafana dashboards. 
  
  The script is written on python and I tried to use standard lib's as much as possible,
  but you still need a pip install.
  
  This script returns a Json format with services status coded by digits: 
  
  active = 1
  reloading = 2 
  inactive = 3
  failed  = 4 
  activating = 5
  deactivating = 6 
  
  so you need to convert it back to string in Grafana. 
  
  Actualy the last Telegraf version accepts the string values in json format, but if you want 
  to use Grafana alerting you need some digits to put it on alert graphs. 
  
  Also script provide a service name and time recent service status in seconds, 
  so you can use it to build UP/DOWN time in Grafana dashboards.

## Installation

  **pip install requirements.txt**
  
  **chmod +x ./service.py**
  
  Rename **settings.ini.back** to **settings.ini**  and specifying a list of services that you need to check: 

```
   [SERVICES]
    name = docker.service nginx.service
```

Then configure the telegraf **exec** plugin, something like this: 

### You need to use latest version of Telegraf compile from github, because older versions 
### didn't support string format in json plugin.

```
    [[inputs.exec]]

    commands = [
     "/opt/telegraf/service.py"
    ]

    timeout = "5s"
    name_override = "services_stats"
    data_format = "json"
    tag_keys = [
      "service"
    ]
```
That's all, now we can create nice and pretty Grafana dashboards of system services with alerting. 

Good luck. 

