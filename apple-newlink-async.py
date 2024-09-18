import random
import requests
import schedule
import time
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import threading
import sys
import os


# Token and chat ID constants (unchanged)
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
TOKEN7 = "7463059683:AAEEEEq5XgK88S-lqHw09n2Hr7l0upUhlWg"
chat_id7 = "5933792581"
HANG_NOTIFICATION_TOKEN = "7469851491:AAH4T3MYOf5YUYf-5lxuhQvF4Ui0f7CmJpw"
HANG_NOTIFICATION_CHAT_ID = "5933792581"
# ... (other token and chat_id definitions)

# Proxy configurations
proxy_list = [
    '14ad0d760897d:1d0267825c@5.161.216.207:30032',
    '14ad0d760897d:1d0267825c@5.161.216.207:30118',
    '14ad0d760897d:1d0267825c@5.161.216.207:30128',
    '14ad0d760897d:1d0267825c@5.161.216.207:30129',
    '14ad0d760897d:1d0267825c@5.161.216.207:30130',
    '14a926dcc999d:6cbc621633@88.151.57.78:12323',
    '14a926dcc999d:6cbc621633@203.166.131.101:12323'
]

COUNTRY_AND_STORE = {
    'ZP/A': ['sg', 'R633'],
    'LL/A': ['', 'R077'],
    'ZA/A': ['sg', 'R633'],
    'FE/A': ['sg', 'R633']
}

NUMBER_OF_STORES_AROUND = 3

async def get_product_list():
    model_control = "https://api.telegram.org/bot7463059683:AAEEEEq5XgK88S-lqHw09n2Hr7l0upUhlWg/getUpdates?offset=-1"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(model_control) as response:
                result = await response.json()
                result_model_control = result['result'][0]['message']['text']
        except:
            result_model_control = "SG"
    
    if result_model_control == "All":
        return ['MYWX3ZP/A', 'MYX23ZP/A', 'MYW93LL/A', 'MYW53LL/A']
    elif result_model_control == "SG":
        return ['MYWX3ZP/A', 'MYX23ZP/A', 'MYWW3ZP/A', 'MYX13ZP/A']
    elif result_model_control == "SGW":
        return ['MYWW3ZP/A', 'MYX13ZP/A']
    elif result_model_control == "USG":
        return ['MYW53LL/A','MYW93LL/A']
    elif result_model_control == "Test":
        return ['MPQC3ZP/A','MPQC3LL/A']
    else:
        return ['MYWX3ZP/A', 'MYX23ZP/A']

def get_proxy(proxy_config):
    if proxy_config == "P1":
        return "http://14a926dcc999d:6cbc621633@88.151.57.78:12323"
    elif proxy_config == "P2":
        return "http://14a926dcc999d:6cbc621633@203.166.131.101:12323"
    elif proxy_config == "P0":
        return None
    else:
        return f"http://{random.choice(proxy_list)}"

async def check_product_stock(session, prod, proxy_config):
    product_country_code = prod[-4:]
    link = f'https://www.apple.com/{COUNTRY_AND_STORE[product_country_code][0]}/shop/fulfillment-messages?pl=true&mts.0=regular&mts.1=compact&cppart=UNLOCKED/WW&parts.0={prod[0:7]}%2F{prod[-1:]}&searchNearby=true&store={COUNTRY_AND_STORE[product_country_code][1]}'
    print(link)
    proxy = get_proxy(proxy_config)
    try:
        async with session.get(link, proxy=proxy, timeout=10) as response:
            data = await response.json()
            
            check_stock = [
                [x['partsAvailability'][prod]['pickupSearchQuote'],
                 x['partsAvailability'][prod]['messageTypes']['regular']['storePickupProductTitle'],
                 x['storeName']]
                for x in data['body']['content']['pickupMessage']['stores'][:NUMBER_OF_STORES_AROUND]
            ]
            
            return await process_stock_info(check_stock, product_country_code)
    except Exception as e:
        return f"Error checking {prod}: {str(e)}"

async def process_stock_info(check_stock, product_country_code):
    in_stock = []
    not_in_stock = []
    
    for info in check_stock:
        # Use Markdown formatting
        message = f"*{info[1]}*\n_{info[0]}_\n{info[2]}\n\n"
        if 'Available' in info[0]:
            in_stock.append(message)
        else:
            not_in_stock.append(message)
    
    return await send_messages(in_stock, not_in_stock, product_country_code)

async def send_messages(in_stock, not_in_stock, product_country_code):
    messages = []
    global chat_id3
    global chat_id4
    global chat_id2
    global chat_id
    if product_country_code == 'LL/A':
        if in_stock:
            messages.append((TOKEN3, chat_id3, ''.join(in_stock)))
        if not_in_stock:
            messages.append((TOKEN4, chat_id4, ''.join(not_in_stock)))
    else:
        if in_stock:
            messages.append((TOKEN2, chat_id2, ''.join(in_stock)))
        if not_in_stock:
            messages.append((TOKEN, chat_id, ''.join(not_in_stock)))
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for token, chat_id, text in messages:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            params = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'Markdown'
            }
            tasks.append(session.post(url, data=params))
        
        await asyncio.gather(*tasks)
    
    return "Messages sent successfully"

async def apple_check_loop(proxy_config):
    products = await get_product_list()
    
    async with aiohttp.ClientSession() as session:
        tasks = [check_product_stock(session, prod, proxy_config) for prod in products]
        results = await asyncio.gather(*tasks)
    
    for prod, result in zip(products, results):
        print(f"Result for {prod}: {result}")

class Watchdog:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.timer = None

    def reset(self):
        if self.timer:
            self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self.callback)
        self.timer.start()

    def stop(self):
        if self.timer:
            self.timer.cancel()

def send_hang_notification_and_restart():
    message = "Warning: The Apple Check script has been hanging for 3 minutes! Attempting to restart..."
    url = f"https://api.telegram.org/bot{HANG_NOTIFICATION_TOKEN}/sendMessage"
    params = {
        'chat_id': HANG_NOTIFICATION_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, data=params)
    except Exception as e:
        print(f"Failed to send hang notification: {e}")
    
    print("Restarting the script...")
    os.execv(sys.executable, ['python'] + sys.argv)

async def main():
    watchdog = Watchdog(180, send_hang_notification_and_restart)  # 600 seconds = 10 minutes
    try:
        watchdog.reset()
        url_control = "https://api.telegram.org/bot6228488082:AAHNbCEKtoq55I86Fn_TVLGzBVIq_idZ5sM/getUpdates?offset=-1"
        async with aiohttp.ClientSession() as session:
            async with session.get(url_control) as response:
                result_control = (await response.json())['result'][0]['message']['text']
        
        if result_control == 'No':
            text1 = 'User is stopping the stock check'
            #print(text1)
            #time.sleep(35)
            url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
            async with aiohttp.ClientSession() as session:
                await session.get(url)
        else:
            await apple_check_loop(result_control)
    except Exception as e:
        text1 = f"Error in main: {str(e)}"
        url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
        async with aiohttp.ClientSession() as session:
            await session.get(url)
        await apple_check_loop("Yes")
    finally:
        watchdog.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    def run_main():
        loop.run_until_complete(main())

    schedule.every(61).seconds.do(run_main)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            error_message = f"An error occurred in the main loop: {str(e)}. Attempting to restart..."
            print(error_message)
            url = f"https://api.telegram.org/bot{HANG_NOTIFICATION_TOKEN}/sendMessage"
            params = {
                'chat_id': HANG_NOTIFICATION_CHAT_ID,
                'text': error_message,
                'parse_mode': 'Markdown'
            }
            try:
                requests.post(url, data=params)
            except:
                pass
            
            # Attempt to restart the script
            os.execv(sys.executable, ['python'] + sys.argv)