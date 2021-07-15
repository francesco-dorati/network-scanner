import queue
import socket
import threading
import subprocess
from queue import Queue

THREADS_NUMBER = 100

queue = Queue()
ips = [f'192.168.1.{i}' for i in range(1, 255)]
up = []

def main():
    for ip in ips:
        queue.put(ip)

    threads = []

    for _ in range(THREADS_NUMBER):
        thread = threading.Thread(target=worker)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    
    for host in up:
        print(f"{host['hostname'].strip('.homenet.telecomitalia.it')}\t\t\t({host['ip']})\t\t\t[{host['mac']}]")


def ping(ip):
    out = subprocess.Popen(f'arp {ip}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    # print(out.stdout.read().decode('utf-8').strip().split())

    hostname, _, _, mac, *_ = out.stdout.read().decode('utf-8').strip().split()

    if hostname != '?':
        return hostname, mac
    else:
        return None


def worker():
    while not queue.empty():
        ip = queue.get()
        res = ping(ip)

        try:
            hostname, mac = res
            up.append({
                'ip': ip,
                'hostname': hostname,
                'mac': mac
            })
        except TypeError:
            pass
        


if __name__ == '__main__':
    main()




# import subprocess

# COUNT = '1'
# TIMEOUT = '1'

# hosts = []

# for i in range(1, 255):
#     cmd = f'ping -c {COUNT} -q -t {TIMEOUT} 192.168.1.{i}'

#     out = subprocess.Popen(cmd.split(),
#                             stdout=subprocess.PIPE,
#                             stderr=subprocess.PIPE).stdout.read().decode('utf-8')
                
#     if out.split('\n')[3].split()[3] == '1':
#         hosts.append(i)

# for host in hosts:
#     print(f'{host} is up.')
