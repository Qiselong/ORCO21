import time
import requests


#parameters
w_time = 5.1

def main():
    url = "http://10.22.168.65:9080/route/v1/driving/-117.851364,33.698206;-117.838925,33.672260"
    r = requests.get(url)
    res = r.json()
    res
    print("lol")
    

main()