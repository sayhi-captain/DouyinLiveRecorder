# coding=utf-8
import requests

from dylr.core import dy_api
from dylr.util import logger
from dylr.plugin import plugin

cookie_cache = None
# 记录cookie访问失败的次数
cookie_failed = 0
max_cookie_failed = 5


def record_cookie_failed():
    global cookie_failed
    cookie_failed += 1
    logger.debug("检测开播时返回系统繁忙")
    if cookie_failed == max_cookie_failed:
        logger.fatal_and_print("多次重试无法访问资源，可能是cookie失效")
        plugin.on_cookie_invalid()

    # 自动获取 cookie
    # if not config.is_using_custom_cookie() and cookie_failed == max_cookie_failed:
    if cookie_failed == max_cookie_failed:
        auto_get_cookie()


def auto_get_cookie():
    global cookie_cache, cookie_failed
    logger.info_and_print(f"获取cookie中...")

    url = "https://live.douyin.com"
    cookie = "__ac_nonce=0638733a400869171be51"
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
        "cookie": cookie,
    }
    resp = requests.get(url, headers=header, proxies=dy_api.get_proxies())
    ttwid = None
    for c in resp.cookies:
        if c.name == "ttwid":
            ttwid = c.value
            break

    if ttwid is not None:
        cookie += "; ttwid=" + ttwid
        cookie_cache = cookie
        logger.info_and_print(f"cookie获取完成")
    else:
        logger.fatal_and_print(f"cookie获取失败")

    cookie_failed = 0
