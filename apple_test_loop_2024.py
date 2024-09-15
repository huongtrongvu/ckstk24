from threading import main_thread
#import pandas as pd
#import numpy as np
import socket
#import pyodbc

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import schedule

import requests
# from bs4 import BeautifulSoup
import time
import json

import requests
TOKEN2 = "6520255012:AAFyvArkYCZ0akXPm638Cli61jVPBLsU8FU"
chat_id = "5933792581"
TOKEN = "6542202630:AAFBrS3kkBu6wMWc7H5G5uLsnzinCWKUNSw"
chat_id2 = "5933792581"
TOKEN3 = "6304000921:AAHH5PbFMM-jOAeENQWgBe5SHMvmeowTjVQ"
chat_id3 = "5933792581"
TOKEN4 = "6584999815:AAGk5CCOTqLNb06_8M1AOrq3Shosy9MaT-w"
chat_id4 = "5933792581"
TOKEN5 = "6107812774:AAEKv8I6VZe28bCPa4i4ZTlhZ7726jaQXSQ"
chat_id5 = "5933792581"
TOKEN6 = "6228488082:AAHNbCEKtoq55I86Fn_TVLGzBVIq_idZ5sM"
chat_id6 = "5933792581"
# TOKEN6 = "5716086925:AAGEof-lJe-o4UF41TKJbGe82VDAkUIutJI"
# chat_id6 = "5298130105"
# TOKEN7 = "5542027397:AAGUG6j4oph22LA4QGYDc_BkrJXW9Nm3lf4"
# chat_id7 = "5298130105"

proxy1 = {
    "https": "14a926dcc999d:6cbc621633@88.151.57.78:12323"
}

proxy2 = {
    "https": "14a926dcc999d:6cbc621633@203.166.131.101:12323"
}

proxy3 = {
    "https": "htvu91:Appl31pad@193.228.193.86:11248",
    "http": "htvu91:Appl31pad@193.228.193.86:11248"
}

allproduct = ['MYWX3ZP/A'#,'MYX23ZP/A',
              #'MYWW3ZP/A','MYX13ZP/A'
              ]
              # 'MQ9X3ZP/A', 'MQAM3ZP/A', 
              #'MQC53ZP/A', 'MQ9W3ZP/A', 'MQ913LL/A' ,'MQ8W3LL/A', 'MQ8R3LL/A',# 
              
# allwatch = [#'MNHG3ZP/A',
#             #'MNHF3ZP/A', 'MQFK3ZP/A',
#             'MQFL3ZP/A','MNHH3ZP/A','MQFM3ZP/A'
#             #'MQFN3ZP/A', 'MQFR3ZP/A', 
#             #'MNHK3ZP/A',
#             #'MQFW3ZP/A', 'MNHL3ZP/A'
#             ]


countryandstore = {
    'ZP/A': ['sg','R633'],
    'LL/A': ['', 'R077'],
    'ZA/A': ['sg','R633'],
    'FE/A': ['sg','R633']
    }
numberofstorearound = 3

def apple_check_loop(proxyconfig):
    # payload = {'api_key': '19afc51481b59e7a8f8b1a8bc4848a90', 'url': 'https://httpbin.org/ip'}
    # r = requests.get('http://api.scraperapi.com', params=payload)
    print(proxyconfig)
    error = '' 
    
    try:
        for prod in allproduct:
            
            productcountrycode = prod[-4:]
            linktoproduct = 'https://www.apple.com/' + countryandstore[productcountrycode][0] + '/shop/fulfillment-messages?parts.0=' + prod[0:7] + '%2F' + prod[-1:] + '&searchNearby=true&store=' + countryandstore[productcountrycode][1]
            # payload = {'api_key': '19afc51481b59e7a8f8b1a8bc4848a90', 'url': linktoproduct}
            # a = requests.get('http://api.scraperapi.com', params=payload)
            if proxyconfig == "P1":
                a = requests.get(linktoproduct, proxies=proxy1)
            elif proxyconfig == "P2":
                a = requests.get(linktoproduct, proxies=proxy2)
            elif proxyconfig == "P3":
                a = requests.get(linktoproduct, proxies=proxy3)
            else:
                a = requests.get(linktoproduct)
            check_stock = [[x['partsAvailability'][prod]['pickupSearchQuote'], x['partsAvailability'][prod]['messageTypes']['regular']['storePickupProductTitle'] , x['storeName']] for x in a.json()['body']['content']['pickupMessage']['stores'] ]
            print(check_stock)
            i = 0
            for info in check_stock:
                instocksg = ''
                notinstocksg = ''
                instockus = ''
                notinstockus = ''
                error = ''
                watchinstocksg = ''
                watchnostocksg = ''
                message = info[1] + '\n' + info[0]+ '\n'+ info[2] + '\n'+'\n'
                print(message)
                if 'Available' in info[0]:
                    #print(info[1])
                    print(message)
                    if productcountrycode == 'LL/A':
                        instockus += message
                    else:
                        instocksg += message
                else:
                    if productcountrycode == 'LL/A':
                        notinstockus += message
                    else:
                        notinstocksg += message
                i += 1
                
                
                if instocksg != '':
                    url = f"https://api.telegram.org/bot{TOKEN2}/sendMessage?chat_id={chat_id2}&text={instocksg}"
                    print(requests.get(url).json())
                else: #notinstocksg != '':
                    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={notinstocksg}"
                    print(requests.get(url).json()) 
                if instockus != '':
                    url = f"https://api.telegram.org/bot{TOKEN3}/sendMessage?chat_id={chat_id3}&text={instockus}"
                    print(requests.get(url).json())
                else: # if notinstockus != '':
                    url = f"https://api.telegram.org/bot{TOKEN4}/sendMessage?chat_id={chat_id4}&text={notinstockus}"
                    print(requests.get(url).json())
                if i == numberofstorearound:
                    break
        # for prod in allwatch:
        #     productcountrycode = prod[-4:]
        #     linktoproduct = 'https://www.apple.com/' + countryandstore[productcountrycode][0] + '/shop/fulfillment-messages?parts.0=' + prod[0:7] + '%2F' + prod[-1:] + '&searchNearby=true&store=' + countryandstore[productcountrycode][1]
        #     a = requests.get(linktoproduct)
        #     check_stock = [[x['partsAvailability'][prod]['pickupSearchQuote'], x['partsAvailability'][prod]['messageTypes']['regular']['storePickupProductTitle'] , x['storeName']] for x in a.json()['body']['content']['pickupMessage']['stores'] ]
        #     # print(check_stock)
        #     i = 0
        #     for info in check_stock:
        #         message = info[1] + '\n' + info[0]+ '\n'+ info[2] + '\n'+'\n'
        #         if 'Available' in info[0]:
        #             # print(info[1])
        #             # print(info[0])
        #             watchinstocksg += message
        #         else:
        #             watchnostocksg += message

        
        # if watchinstocksg != '':
        #     url = f"https://api.telegram.org/bot{TOKEN6}/sendMessage?chat_id={chat_id6}&text={watchinstocksg}"
        #     print(requests.get(url).json())
        # if watchnostocksg != '':
        #     url = f"https://api.telegram.org/bot{TOKEN7}/sendMessage?chat_id={chat_id7}&text={watchnostocksg}"
        #     print(requests.get(url).json())
    except IndexError:
        error += 'An Index Error Has Occured'
        url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={error}"
        print(requests.get(url).json())
    except:
        error += 'An Error Has Occured'
        url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={error}"
        print(requests.get(url).json())



def main():
    try:
        url_control = "https://api.telegram.org/bot6228488082:AAHNbCEKtoq55I86Fn_TVLGzBVIq_idZ5sM/getUpdates?offset=-1"
        result_control = requests.get(url_control).json()['result'][0]['message']['text']
        if result_control == 'No':
            text1 = 'User is stopping the stock check'
            url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
            print(requests.get(url).json())
        else:
            apple_check_loop(result_control)
    except:
        apple_check_loop("Yes")
        
        
#main()

# # schedule.every(1).minutes.do(apple_check_loop)
schedule.every(10).seconds.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
