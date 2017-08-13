#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

# 打开一个文件
fo = open("emails.txt", "r+")
str = fo.read();
print "读取的字符串是 : ", str
# 关闭打开的文件
wr = open("emails_splited.csv","w+")

splited=',,'.join(' '.join(str.split('\n')).split())
print "读取的字符串是 : ", splited
wr.write(splited)
#splited=re.split('\n| ',wr)
fo.close()