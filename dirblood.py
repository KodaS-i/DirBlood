import queue
import threading
import urllib3
import urllib.parse as U
import urllib.error as E
import sys

#CORES

r = "\033[31m"
w = "\033[37m"
#_____________


print(f"(@){r}DESENVOLVIDO PELO KODAS-i{w}")

if len(sys.argv) < 3:
    print("Forma de uso: \"dirblood.py {site} {wordlist}\"")
    sys.exit()



threads = 5
target = sys.argv[1]
filepath = sys.argv[2]
ext = [".php",".html",".css",".js"]
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AplleWebKit/547.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

def wordlist(filepath):
    
    is_resume = False
    words = queue.Queue()

    with open(filepath) as fp:
        raw = fp.readline()
        while raw:
            word = raw.strip()
            words.put(word)
            raw = fp.readline()

    fp.close()
    return words

def brute_dir(word_queue,extensions=None):

    while not word_queue.empty():
        url_get = word_queue.get()
        url_list = []

        if "." not in url_get:
            url_list.append(f"/{url_get}/")
        
        else:
            url_list.append(f"/{url_get}")

    if extensions:
        for extension in extensions:
            url_list.append(f"/{url_get}{extension}")

    for brute in url_list:
        url = f"{target}{U.quote(brute)}"

        http = urllib3.PoolManager()
        head = {}
        head["User-Agent"] = user_agent         
        response = http.request("GET",headers=head,url=url)

        if len(response.data):
            if response.status != 404:
               print(f"{url} ==> [{response.status}]")
        '''except (E.URLError, E.HTTPError):
            if hasattr(E.HTTPError,'code') and E.HTTPError.code != 404:
                print("{url} ==> [{E.HTTPError.code}]")'''

list = wordlist(filepath)


for i in range(1):
    t = threading.Thread(target=brute_dir,args=(list,ext,))
    t.start()
