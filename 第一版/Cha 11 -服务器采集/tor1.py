import socket
import socks
import requests

# Tor使用9150端口为默认的socks端口
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
# 获取这次抓取使用的IP地址
a = requests.get("http://checkip.amazonaws.com").text

print (a)