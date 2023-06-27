import hashlib 
import os
from pbkdf2 import PBKDF2
import Crypto
import sys 
import itertools
import threading
import multiprocessing
from Crypto.Cipher import AES 
import time 
import sys 
import argparse

start = time.perf_counter()
IV = b'l\x078\x014$sX\x03\xffri3\x13aQ'
HMAC_KEY = b'\x8f\xf4\xf2\xbb\xad\xe9G\xea\x1f\xdfim\x80[5>'
BUILD_KEY = "dropbox"
CLIENT_KEY_NAME = "Client"
dropbox_path = os.path.expanduser('~') + "/.dropbox/instance1/hostkeys"

    
def decrypt_the_payload(data, key):
    keys = hashlib.md5(('ia9%sX' % key + 'a|ui20').encode()).digest()
    return AES.new(keys,mode=AES.MODE_CBC, IV=IV).decrypt(data)


def get_versioned_key(CLIENT_KEY_NAME, hmac_key,start,end,size,dropbox_path=dropbox_path):
    data = open(f"{dropbox_path}","rb").read()
    version, raw_payload = data[0], data[1:-16]

    for i in range(start, end):
        payload_ = decrypt_the_payload(raw_payload, i)
        padding  = payload_[-1] 
        payload_ = payload_[: - padding].decode('utf-8',errors='ignore').lower()
        if 'client' in payload_: 
            print(payload_)
            print("Inode Number :: ", i)
            open("inode_number",'w').write(str(i))
            exit(0)

def get_user_key(hmac_key,start,end,size): 
    get_versioned_key(CLIENT_KEY_NAME, hmac_key,start, end , size,dropbox_path=dropbox_path)

def db_key_store(dropbox_path,start,end,size):
    get_user_key(b'\xd1\x14\xa5R\x12e_t\xbdw.7\xe6J\xee\x9b',start, end,size)

def run_multithreading(start, end,size):

    no_of_threads = 2
    threads = []
    temp = int(str(start).zfill(size)[0])
    if(temp ==0):
        start = 1 * (10 **(size -1))
        end = 2 * (10 ** (size -1))
        print(start, end)
        thread = threading.Thread(target=db_key_store,args=(dropbox_path,start ,end,size,))
        thread.start()
        threads.append(thread)
    else:
        for i in range(0,no_of_threads ):

            start = ((temp +i) * (10 **(size -1)))
            end = ( (temp + i+1)* ( 10**(size -1)) )

            print(start,end)
            thread = threading.Thread(target=db_key_store,args=(dropbox_path,start ,end,size,))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def main(size):
    no_of_process = 5
    processes = []
    for i in range(no_of_process):
        process = multiprocessing.Process(target=run_multithreading,args=((i * 2) * (10 **(size -1)), (((i*2) +1) * 10**(size -1)), size,))
        process.start()
        processes.append(process)
    
    for process in processes:
        process.join()

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Script for brute-forcing Inode numbers')
    parser.add_argument('digits_length', type=int, help='Length of the Inode number in digits')
    args = parser.parse_args()
    digits_length = args.digits_length

    start = time.perf_counter()
    print("\033[1;32m  ---  Determining The Inode   ---\033[0m")
    if digits_length is None:
        parser.print_help()
        exit(1)

        raise Exception()
    main(int(sys.argv[1]))
    end = time.perf_counter()
    print("Time Taken : ",end - start)
