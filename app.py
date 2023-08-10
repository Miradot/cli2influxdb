from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, abort
import os
import re

app = Flask(__name__)

# method to write to influxdb
def write_to_influxdb(bucket, payload):
    client = InfluxDBClient(url=os.getenv('INFLUXDB_URL'), token=os.getenv('INFLUXDB_TOKEN'), org=os.getenv('INFLUXDB_ORG'))
    write_api = client.write_api(write_options=SYNCHRONOUS)
    return write_api.write(bucket, os.getenv('INFLUXDB_ORG'), payload)

# parsers to extract topic-specific data and write to influxdb
def num_macs(data, request):
    target_value = None
    matching_pattern = re.compile(r'^.*criterion\:\s([0-9]+)$')
    for this_line in data.splitlines():
        if matching_pattern.match(this_line):
            target_value = int(matching_pattern.findall(this_line)[0])

    if target_value:
        update_body = {
            'measurement': os.getenv('INFLUXDB_BUCKET'),
            'tags': {'host': request.remote_addr},
            'fields': {
                'num_macs': target_value
            }
        }

        write_to_influxdb(os.getenv('INFLUXDB_BUCKET'), update_body)

@app.route('/<topic>', methods=['PUT'])
def post_message(topic):
    data = request.data.decode('utf-8')
    method_to_call = eval(topic)
    method_to_call(data, request)

    return "ok", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
