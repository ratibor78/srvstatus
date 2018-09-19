# Servicestat

## version 0.1

## Status of SysteD services for Telegraf+InfluxDB

  Main goal for this short script is checking list of SystemD services 
  and sending this services status with UPtime for building some Grafana dashboards. 

  The script is written on python and I tried to use standart lib's so it's must be ok with 
  most Python versions and systems. 

  The script returns a Json format with services status information. 


## Install 

  **pip install requirements.txt**
  
  **chmod +x ./service.py **
  
  Rename **settings.ini.back** to **settings.ini**  and specifying a list of services that you need to check: 

```
   [SERVICES]
    name = docker.service nginx.service
```

Then configure the telegraf **exec** plugin, something like this: 

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
After that use this for creating you nice and pretty Grafana dashboards.

Good luck. 

