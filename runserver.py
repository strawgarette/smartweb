#!/usr/bin/python
#coding=utf-8

from weibo import app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True, processes=20000)
    # 初始配置  0.0.0.0的意思为允许所有IP访问
    # debug=True 的意思是运行的版本为 debug 
    # processes= 20000  最多允许20000个用户同时访问一个网站




