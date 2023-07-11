# coding=utf-8
"""
:author: Lyzen
:date: 2023.04.03
:brief: app主文件
"""

import os
import signal
import sys
import logging
import platform
import threading

from dylr.core import version, config, record_manager, monitor
from dylr.util import logger
from dylr.plugin import plugin

# 处理 ctrl+c
stop_all_threads = False


def init():
    # 处理 ctrl+c
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGTERM, sigint_handler)

    if not check_dependencies():
        return

    logger.info(f"software started. version: {version}")
    logger.info(f"platform: {platform.platform()}")
    logger.info(f"python version: {platform.python_version()}")
    print("=" * 80)
    print(f"Douyin Live Recorder v.{version} by Lyzen")
    print(f"软件仅供科研数据挖掘与学习交流，因错误使用而造成的危害由使用者负责。")
    print("=" * 80)

    config.read_configs()
    if config.debug():
        logger.instance.setLevel(logging.DEBUG)
    record_manager.rooms = config.read_rooms()

    monitor.init()


def sigint_handler(signum, frame):
    global stop_all_threads
    stop_all_threads = True
    logger.fatal_and_print("catched SIGINT(Ctrl+C) signal")
    plugin.on_close()


def check_dependencies():
    has_requests = True
    has_websocket = True
    has_protobuf = True
    try:
        import requests
    except:
        has_requests = False
    try:
        import websocket
    except:
        has_websocket = False
    try:
        import google.protobuf
    except:
        has_protobuf = False

    if has_requests and has_websocket and has_protobuf:
        return True
    res = []
    if not has_requests:
        res.append("requests")
    if not has_websocket:
        res.append("websocket-client")
    if not has_protobuf:
        res.append("protobuf")
    return False
