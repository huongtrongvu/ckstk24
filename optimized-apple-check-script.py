import random
import requests
import schedule
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

def get_product_list():
    model_control = "https://api.telegram.org/bot7463059683:AAEEEEq5XgK88S-lqHw09n2Hr7l0upUhlWg/getUpdates?offset=-1"
    try:
        result_model_control = requests.get(model_control).json()['result'][0]['message']['text']
    except:
        result_model_control = "SG"
        
    if result_model_control == "All":
        return ['MYWX3ZP/A', 'MYX23ZP/A', 'MYWW3ZP/A', 'MYX13ZP/A', 'MYW53LL/A']
    elif result_model_control == "SG":
        return ['MYWX3ZP/A', 'MYX23ZP/A', 'MYWW3ZP/A', 'MYX13ZP/A']
    elif result_model_control == "SGW":
        return ['MYWW3ZP/A', 'MYX13ZP/A']
    elif result_model_control == "USG":
        return ['MYW53LL/A']
    elif result_model_control == "Test":
        return ['MYNK3ZP/A','MYNF3ZP/A']
    else:
        return ['MYWX3ZP/A', 'MYX23ZP/A']

def get_proxy(proxy_config):
    if proxy_config == "P1":
        return {"https": "14a926dcc999d:6cbc621633@88.151.57.78:12323"}
    elif proxy_config == "P2":
        return {"https": "14a926dcc999d:6cbc621633@203.166.131.101:12323"}
    elif proxy_config == "P0":
        return {"http": "", "https": ""}
    else:
        proxy = random.choice(proxy_list)
        return {"http": proxy, "https": proxy}
    
def check_product_stock(prod, proxy_config):
    product_country_code = prod[-4:]
    link = f'https://www.apple.com/{COUNTRY_AND_STORE[product_country_code][0]}/shop/fulfillment-messages?parts.0={prod[0:7]}%2F{prod[-1:]}&searchNearby=true&store={COUNTRY_AND_STORE[product_country_code][1]}'
    
    proxies = get_proxy(proxy_config)
    try:
        response = requests.get(link, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        check_stock = [
            [x['partsAvailability'][prod]['pickupSearchQuote'],
             x['partsAvailability'][prod]['messageTypes']['regular']['storePickupProductTitle'],
             x['storeName']]
            for x in data['body']['content']['pickupMessage']['stores'][:NUMBER_OF_STORES_AROUND]
        ]
        
        return process_stock_info(check_stock, product_country_code)
    except requests.RequestException as e:
        return f"Error checking {prod}: {str(e)}"

def process_stock_info(check_stock, product_country_code):
    in_stock = []
    not_in_stock = []
    
    for info in check_stock:
        message = f"{info[1]}\n{info[0]}\n{info[2]}\n\n"
        if 'Available' in info[0]:
            in_stock.append(message)
        else:
            not_in_stock.append(message)
    
    return send_messages(in_stock, not_in_stock, product_country_code)

def send_messages(in_stock, not_in_stock, product_country_code):
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
    
    for token, chat_id, text in messages:
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error sending message: {str(e)}")
    
    return "Messages sent successfully"

def apple_check_loop(proxy_config):
    products = get_product_list()
    
    with ThreadPoolExecutor(max_workers=len(products)) as executor:
        future_to_product = {executor.submit(check_product_stock, prod, proxy_config): prod for prod in products}
        for future in as_completed(future_to_product):
            prod = future_to_product[future]
            try:
                result = future.result()
                print(f"Result for {prod}: {result}")
            except Exception as e:
                print(f"Error processing {prod}: {str(e)}")
                text1 = f"Error in apple_check_stock: {prod} - {str(e)}"
                url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
                requests.get(url)

def main():
    try:
        url_control = "https://api.telegram.org/bot6228488082:AAHNbCEKtoq55I86Fn_TVLGzBVIq_idZ5sM/getUpdates?offset=-1"
        result_control = requests.get(url_control).json()['result'][0]['message']['text']
        if result_control == 'No':
            text1 = 'User is stopping the stock check'
            url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
            requests.get(url)
        else:
            apple_check_loop(result_control)
    except Exception as e:
        text1 = f"Error in main: {str(e)}"
        url = f"https://api.telegram.org/bot{TOKEN5}/sendMessage?chat_id={chat_id5}&text={text1}"
        requests.get(url)
        apple_check_loop("Yes")

main()

schedule.every(59).seconds.do(main)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
