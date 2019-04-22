#!/usr/bin/python3
# encoding: utf-8


import socket
import time
import json
import logging
import requests
import psycopg2
from multiprocessing import Pool, Manager
from encrypt import EncryptJSON
from keys import server_database_pro, server_database_dev, disable_url, authority


# create an empty global list that are shared between different processes
hosts_list = Manager().list()

# log file config
logging.basicConfig(filename='scan.log', level=logging.INFO)


# connect database and fetch low traffic hosts
def get_scan_servers():
    try:
        conn = psycopg2.connect(database=server_database_pro['database'], user=server_database_pro['user'], password=server_database_pro['password'], host=server_database_pro['host'], port=server_database_pro['port'])
        # conn = psycopg2.connect(database=server_database_dev['database'], user=server_database_dev['user'], password=server_database_dev['password'], host=server_database_dev['host'], port=server_database_dev['port'])
        cur = conn.cursor()
        cur.execute('SELECT "host" FROM node WHERE hour_transfer < 50000 AND "enableStatus" = 9')
        rows = cur.fetchall()
        # conn.commit()
    except Exception as e:
        logging.info("Connect database error: " + str(e) + '\n')
    finally:
        cur.close()
        conn.close()
    return rows

                  
def if_block(ip):
    
    try:
        #创建socket对象，AF_INET指定使用IPv4协议，SOCK_STREAM指定使用面向流的TCP协议
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
                # print(ip)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
                # with open('./bloeckedServers', 'a') as f:
                #     f.write("%25s : %20s\n" % (current_time, ip)) 
                hosts_list.append(ip)
                logging.info('boock ip: ' + ip + ', ' + current_time)
                break
    finally:
        sk.close()   


# construct a json string and inform the backend by put method
def secret_put(hosts, url):

    # construct a json string 
    secret_dict = {'hosts': hosts}
    json_str = json.dumps(secret_dict)

    # encrypt the json string
    encrypt_str = EncryptJSON().Encrypt(json_str)

    # inform the backend by put method
    headers = {'authorization': authority}
    try:
        result = requests.put(url, data = {'body':encrypt_str}, headers = headers)
        status_code = result.status_code
    except requests.exceptions.ConnectionError as e:
        logging.exception(e)
        status_code = "Connection failed! "     
    except Exception as e:
        logging.exception(e)
        status_code = 'Error!'
    finally:              
        # log the inform result
        logging.info(str(status_code) + ": " + json_str)

    return status_code



if __name__ =='__main__':
    # test_list = ['123.123.123.123', '6.6.6.6']
    # secret_put(test_list, disable_url)
    scan_pool = Pool(4)
    ip_list = get_scan_servers()

    for ip in ip_list: 
        scan_pool.apply_async(if_block, args=(ip[0], ))
    
    scan_pool.close()
    scan_pool.join()
    #使用Manager().list()创建的对象是能在各进程间共享的ListProxy对象，但该对象无法直接进行json序列化或迭代，因此需要hosts_list[:]或是copy模块的copy.copy(hosts_list)返回一个常规list再进行接下来的处理
    hosts = hosts_list[:]
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    try:
        if len(hosts) > 0:
            secret_put(hosts, disable_url)
    except Exception as e:
        logging.exception(current_time + ': ' e)    
    else:
        print(current_time + '\n' + 'success disable blocked nodes: ' + str(hosts))        