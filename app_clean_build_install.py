#!/usr/bin/evn python
# coding: utf-8

import os
import re
import xml.etree.ElementTree as ET

pacakgename = ""
activityname = ""
gradle_file = './app/build.gradle'
manifest_file = './app/src/main/AndroidManifest.xml'
"""
获得applicationID
"""
try:
    with open(gradle_file, "r") as f:
        readlines = f.readlines()
        for line in readlines:
            res = re.findall(r"applicationId \"(\S+)\"", line)
            if (len(res) > 0):
                pacakgename = str.strip(res[0])
except IOError:
    print(IOError)
"""
获得mainactivity
"""
parse = ET.parse(manifest_file)
root = parse.getroot()
flag1 = False
flag2 = False
for child in root.iter('application'):
    for activity in child.iter('activity'):
        for filter in activity.iter('intent-filter'):
            for item in filter:
                values_ = list(item.attrib.values())[0]
                if (values_ == 'android.intent.action.MAIN'):
                    flag1 = True
                if (values_ == 'android.intent.category.LAUNCHER'):
                    flag2 = True
            if (flag1 & flag2):
                activityname = activity.attrib['{http://schemas.android.com/apk/res/android}name']
                break;
            else:
                flag1 = flag2 = False
print(activityname)
cmd = """./gradlew clean&&./gradlew assembleDebug&&\
            adb install -r ./app/build/outputs/apk/debug/app-debug.apk&&\
            adb shell am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER -n %s/%s%s"""%(pacakgename,pacakgename,activityname)
os.system(cmd)