# cli2influxdb
Make-shift telemetry solution based on scheduled copy commands on legacy devices and Influxdb

## Use Case Description
This proof of concept software provides a skeleton for ingesting data based on cli commands on legacy devices, into influxdb as time series data points.

## Installation
these installation instructions assumes you have a python environment with python-pip installed.

```
pip install -r requirements.txt
```

## Configuration of the middleware application
Setting up the middleware application on a system with an IP address that's reachable from the network devices from which you want to receive data
```
export INFLUXDB_URL="<influxdb_url>"
export INFLUXDB_TOKEN="<influxdb_token>"
export INFLUXDB_ORG="<influxdb_org>"
export INFLUXDB_BUCKET="<influxdb_bucket>"
```

## Configuration of the Cisco catalyst device
In our example we're using a Catalyst 2960S running 122-55.SE5

first we need to disable the copy prompt so that the necessary commands can be executed w/o confirmation
```
configure terminal
file prompt quiet
```

## Usage
Start the app on a server (the collector) reachable from the network devices
```
python app.py
```

Dump some data from the device and copy it to a http destination, i.e the collector
```
show mac address-table | redirect flash:num_macs
copy flash:num_macs http://<ip of the collector>/num_macs
```

"num_macs", as path of the url, will be resolved to a method name that will be executed by the app, so whenever a new "topic" is needed, a new method by the same name should be introduced and do the massaging and mapping of the received data, and finally passed as an influxdb-valid update body (see example)

In order to get recurring data, use either kron scheduler to execute the above commands, or EEM to do it using a TCL script.

### DevNet resources
If you want to try this out in a demo-environment, have a look at the following always on virtual network devices that could be used as sources for the transmitted data. 

1. [DevNet Always-on sandboxes](https://developer.cisco.com/docs/ios-xe-voip/#!sandbox/always-on-sandboxes) 

## Known issues
Metrics are logged based on the IP address transmitting the URL. If you want influxdb to describe the host names, you could solve this either by introducing a mapping table in the code which will translate the reporting ip addresses to an FQDN, or use socket-library or similar to resolve the ip address to an FQDN using DNS.

## Getting help

If you have questions, concerns, bug reports, etc., please create an issue against this repository.

## Getting involved

This project is supposed to work as a tutorial on how to get started with InfluxDB for network monitoring, using legacy Cisco devices as an example.. If you have any suggestions on what else to include, feel free to reach ut by creating an issue.

----

## Licensing info


`Copyright (c) 2023, Miradot AB`

This code is licensed under the GNU GPL License. See [LICENSE](./LICENSE) for details.

----