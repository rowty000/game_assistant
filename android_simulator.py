# -*- coding: utf-8 -*-
# @Time : 2019/4/11 9:37
# @Author : Vanya
from uiautomator import device as d

# print(d.info)
while True:
    name = input('filename:')
    if name == 'q':
        break
    d.screenshot('pics/' + name + '.png')
# d.click(1250, 765)
