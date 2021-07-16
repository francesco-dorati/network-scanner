import queue
import socket
import threading
import subprocess
from queue import Queue

THREADS_NUMBER = 5

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
    
    dashes = 65
    print('\n' + '-' * dashes)
    print('  ip address\t\tmac address\t\thostname')
    print('-' * dashes)
    for host in up:
        print(f"  {host['ip']}\t\t{host['mac']}\t{host['hostname'].strip('.homenet.telecomitalia.it')}")
    print('-' * dashes + '\n')


def ping(ip):
    out = subprocess.Popen(f'arp {ip}',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    # print(out.stdout.read().decode('utf-8').strip().split())

    hostname, _, _, mac, *_ = out.stdout.read().decode('utf-8').strip().split()

    if mac.count(':') == 5:
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
