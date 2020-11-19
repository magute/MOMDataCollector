import os
import psutil
import datetime
import requests

#------------------------------------------------------------------------------
def api_writer(ComputerName,DateTime,Counter,CounterValue,CounterInstance):
    payload = {
    "computername": ComputerName,
    "datetime" : DateTime,
    "counter" : Counter,
    "countervalue" : CounterValue,
    "counterinstance" : CounterInstance,
    }

    requests.post('http://UbuntuDEV:8000/web01/v1/monitapp/', data = payload)
#------------------------------------------------------------------------------

try:
    while True:
        computerName = os.environ['COMPUTERNAME']
        localDateTime = datetime.datetime.now()
        CounterInstance = None

        # --- CPU --- #

        cpuPerfValue = psutil.cpu_percent(interval=2.5,percpu=False)
        api_writer(computerName,localDateTime,'cpu_percent_total',cpuPerfValue,CounterInstance)

        # --- MEMORY --- #

        memoryPerfValue = psutil.virtual_memory().percent
        api_writer(computerName,localDateTime,'memory_percent_used',memoryPerfValue,CounterInstance)

        # --- DISK --- #

        disk_partitions = []
        disk_partitions = psutil.disk_partitions()

        for disk in disk_partitions:
            diskPerfValue = psutil.disk_usage(disk.device).percent
            api_writer(computerName,localDateTime,'disk_percent_used',diskPerfValue, disk.device)
        
        # --- NETWORK --- #
        
        networkadapters = psutil.net_io_counters(pernic=True)
        
        for name in networkadapters:
            
            if 'Loopback' not in name:
                
                networkPerfValue = networkadapters[name].bytes_sent
                api_writer(computerName,localDateTime,'network_bytes_sent',networkPerfValue, name)
                
                networkPerfValue = networkadapters[name].bytes_recv
                api_writer(computerName,localDateTime,'network_bytes_recv',networkPerfValue, name)

except KeyboardInterrupt:
    print("Stopped by user!")
