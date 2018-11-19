# !/usr/bin/env python
# -*- coding: utf-8 -*-
# author: HiTop time:2018/11/19
import os

# 1.执行gradle task
import requests
from requests_toolbelt import MultipartEncoder


app_file_name = ''
icon_file_path = ''
bundle_id=‘’
api_token=‘’

print("******************执行gradle**********************")
cmd = """./gradlew clean&&./gradlew assembleDebug"""
os.system(cmd)
print("******************解析properties**********************")
# 2.解析xml 获取versioncode version name
pic_path = "./project.properties"
properties = {}
try:
    with open(pic_path, 'r') as fopen:
        for line in fopen:
            line = line.strip()
            if line.find('=') > 0 and not line.startswith('#'):
                strs = line.split('=')
                properties[strs[0].strip()] = strs[1].strip()
except Exception as e:
    print(e)
versionCode = properties.get("versionCode")
versionName = properties.get("versionName")

# 3.请求接口 上传
print("******************请求接口上传**********************")
url = "http://api.fir.im/apps"
headers = {"Content-Type": "application/json"}
data = """{"type": "android", "bundle_id": %s, "api_token":%s}"""%(bundle_id,api_token)
post_request = requests.post(url, data, headers=headers)
request_json = post_request.json()

# 打印json数据 上传app的数据
app_key = request_json['cert']['binary']['key']
app_token = request_json['cert']['binary']['token']
app_upload_url = request_json['cert']['binary']['upload_url']

# 打印json数据 上传icon的数据
icon_key = request_json['cert']['icon']['key']
icon_token = request_json['cert']['icon']['token']
icon_upload_url = request_json['cert']['icon']['upload_url']

# 上传icon
icon_encoder = MultipartEncoder(
    fields={"key": app_key, "token": app_token, "file": ("ic_launcher.png", open(icon_file_path, 'rb'))})
# 上传icon
icon_port = requests.post(icon_upload_url, data=icon_encoder, headers={'Content-Type': icon_encoder.content_type})
if icon_port.status_code == 200:
    print("icon上传成功！！！")
else:
    print("图片传输："+icon_port.json()['error'])

# 上传参数
app_encoder = MultipartEncoder(
    fields={"key": app_key, "token": app_token, "file": ("debug", open(app_file_name, 'rb')), "x:name": "xxx",
            "x:version": versionName, "x:build": versionCode})  # version versionName  build versionCode
# 上传app
app_post = requests.post(app_upload_url, data=app_encoder, headers={'Content-Type': app_encoder.content_type})
if app_post.status_code == 200:
    print("app上传成功！！！")
    print("app上传下载为:" + app_post.json()['download_url'])

else:
    print("二维码传输:"+app_post.json()['error'])

