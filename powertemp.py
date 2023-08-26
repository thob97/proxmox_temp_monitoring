from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import re
import subprocess

def start():
    # Config
    host = 'localhost' 
    port = 8086
    token = 'hBxXTtbVYs8YcoCC94wuSytIbSM6T10SPbkXNk-gqW_ETt-ZH5Eh22oOWBvR1hRU9gUpCNGOEyvK1xHjSinTGQ=='
    org = 'proxmox'  
    bucket = 'proxmox'

    # Connection
    client = InfluxDBClient(url=f"http://{host}:{port}", token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # annotate which components to monitor
    monitors = [Factory_Monitor.cpu(), Factory_Monitor.package(), Factory_Monitor.nvme()]
    while True:   
        #get sensor data
        sensors_data = subprocess.check_output("sensors", shell=True, text=True)

        #iterate throug each temp for each monitor
        for monitor in monitors:
            monitor: Monitor
            monitor.updateTempsFromSensor(sensor_string=sensors_data)
            for i, temp in enumerate(monitor.temps):
                #collect data
                data_point = {
                "measurement": "_custom_measurement", #table name
                "tags": {'host': monitor.name} ,
                "fields": {f'sensor_{i}': temp},
                "time": int(time.time() * 1e9)
                }
                #write
                write_api.write(bucket, org, data_point)
        
        time.sleep(15)        

class Monitor:
    def __init__(self, regex, name):
        self.regex = regex
        self.name = name
        self.temps = []

    def updateTempsFromSensor(self, sensor_string):
        temps = re.findall(self.regex, sensor_string)
        self.temps = [float(temp[1:]) for temp in temps]
    
class Factory_Monitor:
    def cpu():
        return Monitor(r"(?<=Core\s\d:)\s+(\+\d+\.\d+)", 'cpu')
    def package():
        return Monitor(r"(?<=Package\sid\s\d:)\s+(\+\d+\.\d+)", 'package')
    def nvme():
        return Monitor(r"(?<=Sensor\s\d:)\s+(\+\d+\.\d+)", 'nvme')

if __name__ == "__main__":
    start()
