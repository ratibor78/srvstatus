# Servicestat 

## Status of SysteD services for Telegraf+InfluxDB

  Main goal for this short script is checking list of SystemD services 
and sending this services status with UPtime for building some Grafana dashboards or same. 

The script is written on python and I tried to use standart lib's so it's must be ok with 
most Python versions and systems. 

The script returns a Json format with services status information. 
