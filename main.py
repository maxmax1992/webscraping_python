import requests 
import time
import json
import random
from bs4 import BeautifulSoup 
import numpy as np
from proxylists import proxies, append_new_line
import urllib.request

def getdata(url, proxy): 
    http_proxy_header = {
        "http": proxy
    }
    r = requests.get(url, proxies=http_proxy_header) 
    return r.text 
    
# per_page = 10
def get_json(link, proxy):
    htmldata = getdata(link, proxy) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    return json.loads(soup.text)


def is_valid(js):
    return len(js.keys()) == 1 and js.keys()[0] == 'errors'

get_link = lambda per_page, page : f"https://unsplash.com/napi/search/photos?query=office&per_page={per_page}&page={page}&xp="

get_random_proxy = lambda : np.random.choice(proxies)

# # Using readlines()
# file1 = open('myfile.txt', 'r')
# Lines = file1.readlines()

def main_loop_download_img_urls():
    result_array = []
    num_pages = np.inf
    curr_page = 0
    RESULTS_PER_PAGE = 20
    while curr_page < num_pages:
        rand_proxy = get_random_proxy()
        json_ob = get_json(get_link(RESULTS_PER_PAGE, curr_page), proxy=rand_proxy)
        if "total_pages" in json_ob:
            num_pages = int(json_ob['total_pages'])
        for result in json_ob['results']:
            append_new_line('download_urls.txt', result['urls']['regular'])
        print("SUCCESS! downloading page: ", curr_page)
        curr_page += 1
        time.sleep(0.2)


def download_image(url, path, proxy=None):
    # To save to an absolute path.
    if proxy:
        http_proxy_header = {
            "http": get_random_proxy()
        }
        r = requests.get(url, proxies=http_proxy_header) 
    else:
        r = requests.get(url)

    with open(path, 'wb') as f:
        f.write(r.content)

def main_loop_download_imgs():
    f = open('download_urls.txt', 'r')
    urls = f.readlines()
    TGT_FOLDER = "/data_disk_10TB/office_web_images/"
    i = 0 
    for img_url in urls:
        download_image(img_url, TGT_FOLDER + str(i) + ".jpg", get_random_proxy())
        i += 1
        time.sleep(0.2)



if __name__ == "__main__":
    # main_loop_download_img_urls()
    # uncomment next line if you don't have the urls for images
    main_loop_download_imgs()


