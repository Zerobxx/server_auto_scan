#!/usr/bin/python3
# encoding: utf-8

import socket
import time
from multiprocessing import Pool


with open('./ips', 'r') as f:
    ip_list = f.readline().split(',')

                  
def if_block(ip):
    
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(5)
        sk.connect((ip, 22))
    except Exception:
        n = 1
        for i in range(0, 3):
            time.sleep(1)
            try:
                skerr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                skerr.settimeout(5)
                skerr.connect((ip, 22))
            except Exception:
                n += 1    
            finally:
                skerr.close()  
            if n >= 3:
                print(ip)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                with open('./bloeckedServers', 'a') as f:
                    f.write("%25s : %20s\n" % (current_time, ip)) 
                break
    finally:
        sk.close()   



scan_pool = Pool(4)

for ip in ip_list: 
    scan_pool.apply_async(if_block, args=(ip, ))
  
scan_pool.close()
scan_pool.join()

