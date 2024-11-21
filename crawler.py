from __future__ import print_function

import re
import time
import sys
import os
import json

from urllib.parse import quote
from selenium.webdriver.common.by import By
import requests

g_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}

if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


def my_print(msg, quiet=False):
    if not quiet:
        print(msg)


def bing_gen_query_url(keywords):
    base_url = "https://www.bing.com/images/search?"
    keywords_str = "&q=" + quote(keywords)
    query_url = base_url + keywords_str
    filter_url = "&qft="
    # face only
    filter_url += "+filterui:face-face"

    query_url += filter_url

    return query_url


def bing_get_image_url_using_api(keywords, max_number=10000, proxy=None, proxy_type=None):
    proxies = None
    if proxy and proxy_type:
        proxies = {"http": "{}://{}".format(proxy_type, proxy),
                   "https": "{}://{}".format(proxy_type, proxy)}
    start = 1
    image_urls = []
    while start <= max_number:
        url = 'https://www.bing.com/images/async?q={}&first={}&count=35'.format(keywords, start)
        res = requests.get(url, proxies=proxies, headers=g_headers)
        res.encoding = "utf-8"
        image_urls_batch = re.findall('murl&quot;:&quot;(.*?)&quot;', res.text)
        if len(image_urls) > 0 and image_urls_batch[-1] == image_urls[-1]:
            break
        image_urls += image_urls_batch
        start += len(image_urls_batch)
    return image_urls


def crawl_image_urls(keywords, max_number=10000,
                     proxy=None, proxy_type="http", quiet=False):
    """
    Scrape image urls of keywords from Google Image Search
    :param keywords: keywords you want to search
    :param max_number: limit the max number of image urls the function output, equal or less than 0 for unlimited
    :param proxy: proxy address, example: socks5 127.0.0.1:1080
    :param proxy_type: socks5, http
    :return: list of scraped image urls
    """

    my_print("\nScraping From Bing Image Search ...\n", quiet)
    my_print("Keywords:  " + keywords, quiet)

    if max_number <= 0:
        my_print("Number:  No limit", quiet)
        max_number = 10000
    else:
        my_print("Number:  {}".format(max_number), quiet)

    # 默认引擎为bing
    query_url = bing_gen_query_url(keywords)

    my_print("Query URL:  " + query_url, quiet)

    image_urls = []

    # api
    # 默认引擎为bing
    image_urls = bing_get_image_url_using_api(keywords, max_number=max_number,
                                              proxy=proxy, proxy_type=proxy_type)

    if max_number > len(image_urls):
        output_num = len(image_urls)
    else:
        output_num = max_number

    my_print("\n== {0} out of {1} crawled images urls will be used.\n".format(
        output_num, len(image_urls)), quiet)

    return image_urls[0:output_num]
