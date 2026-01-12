import requests
import threading
import os
import time
import webbrowser
from queue import Queue

def print_banner():
    print("""\033[93m
          
██╗░░██╗███████╗██╗░░░██╗███╗░░██╗
██║░░██║╚════██║╚██╗░██╔╝████╗░██║
███████║░░░░██╔╝░╚████╔╝░██╔██╗██║
██╔══██║░░░██╔╝░░░╚██╔╝░░██║╚████║
██║░░██║░░██╔╝░░░░░██║░░░██║░╚███║
╚═╝░░╚═╝░░╚═╝░░░░░░╚═╝░░░╚═╝░░╚══╝  
    >> PROXY SCRAPER <<
\033[0m""")

q = Queue()
current_format = "1" 

def scrape_and_check(protocol):
    global current_format
    api_urls = {
        "http": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "socks4": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all",
        "socks5": "https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all"
    }
    
    print("\n\033[93mSelect Output Format:\033[0m")
    print(" [1] protocol://ip:port")
    print(" [2] ip:port")
    current_format = input("\nFormat Choice > ").strip()

    url = api_urls.get(protocol)
    print(f"\n[*] Harvesting {protocol.upper()} proxies...")
    
    try:
        res = requests.get(url, timeout=10)
        proxies = list(set([p.strip() for p in res.text.splitlines() if p.strip()]))
        print(f"[+] Found {len(proxies)} unique proxies. Checking...")
        
        for p in proxies:
            clean_p = p.split('://')[-1]
            q.put((clean_p, protocol))
            
        for _ in range(50):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
        
        q.join()
        print(f"\n\033[92m[!] Done. Working {protocol.upper()} saved to hzy_{protocol}.txt\033[0m")
        input("\nPress Enter to return...")
        
    except Exception as e:
        print(f"\033[91m[!] Error: {e}\033[0m")
        time.sleep(2)

def worker():
    while not q.empty():
        ip_port, protocol = q.get()
        
        if protocol == "socks5":
            proxy_url = f"socks5h://{ip_port}"
        else:
            proxy_url = f"{protocol}://{ip_port}"

        proxies_config = {"http": proxy_url, "https": proxy_url}
        
        try:
            r = requests.get("https://httpbin.org/ip", proxies=proxies_config, timeout=7)
            if r.status_code == 200:
                print(f"\033[92m[+] {ip_port:22} | {protocol.upper()} ALIVE\033[0m")
                with open(f"h7yn_{protocol}.txt", "a") as f:
                    if current_format == "1":
                        f.write(f"{protocol}://{ip_port}\n")
                    else:
                        f.write(f"{ip_port}\n")
        except:
            pass
        q.task_done()

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print(" [1] Scrape HTTP")
        print(" [2] Scrape SOCKS4")
        print(" [3] Scrape SOCKS5")
        print(" [4] Join Discord")
        print(" [5] Exit Program")
        
        choice = input("\n\033[93mH7YN > \033[0m").strip()

        if choice == "1":
            scrape_and_check("http")
        elif choice == "2":
            scrape_and_check("socks4")
        elif choice == "3":
            scrape_and_check("socks5")
        elif choice == "4":
            print("[*] Opening browser...")
            webbrowser.open("https://discord.gg/pyUEV5UZ4M")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("\033[91m[!] Invalid Selection\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    main()