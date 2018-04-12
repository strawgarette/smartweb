#!/usr/bin/env python
#coding=utf-8
#set softtabstop=0
"""

官方文档
https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.z5MWoh&treeId=257&articleId=105735&docType=1

这个接口的消息格
官方文档
http公司就怎样规范。
"""

import sys
import urllib.request
import urllib.parse
import requests #这个库需要非常小心
import json
import time
import datetime
from mysql import MoonMysql#访问自己写的类


#自定义机器人的封装类
class DtalkRobot(object):
    """docstring for DtRobot"""
    webhook = ""
    def __init__(self, webhook):
        super(DtalkRobot, self).__init__()
        self.webhook = webhook

    #text类型
    def sendText(self, msg, isAtAll=False, atMobiles=[]):
        data = {"msgtype":"text","text":{"content":msg},"at":{"atMobiles":atMobiles,"isAtAll":isAtAll}}
        return self.post(data)



    #markdown类型
    def sendMarkdown(self, title, text):
        data = {"msgtype":"markdown","markdown":{"title":title,"text":text}}
        return self.post(data)

    #link类型
    def sendLink(self, title, text, messageUrl, picUrl=""):
        data = {"msgtype": "link","link": {"text": text, "title":title,"picUrl": picUrl,"messageUrl": messageUrl}}
        return self.post(data)

    #ActionCard类型
    def sendActionCard(self, actionCard):
        data = actionCard.getData()
        return self.post(data)

    #FeedCard类型
    def sendFeedCard(self, links):
        data = {"feedCard":{"links":links},"msgtype":"feedCard"}
        return self.post(data)



    def post(self, data):#这个问题坑了笔者一天，从网页上的python2.0的教程再到自己写的python3.0的教程
        print(data)
        headers = {
            'Content-Type':'application/json;charset=utf-8'
        }
        post_data = json.dumps(data)
        res = requests.post(self.webhook, data=post_data, headers=headers)

        return res.text



#ActionCard类型消息结构
class ActionCard(object):
    """docstring for ActionCard"""
    title = ""
    text = ""
    singleTitle = ""
    singleURL = ""
    btnOrientation = 0
    hideAvatar = 0
    btns = []

    def __init__(self, arg=""):
        super(ActionCard, self).__init__()
        self.arg = arg

    def putBtn(self, title, actionURL):
        self.btns.append({"title":title,"actionURL":actionURL})

    def getData(self):
        data = {"actionCard":{"title":self.title,"text":self.text,"hideAvatar":self.hideAvatar,"btnOrientation":self.btnOrientation,"singleTitle":self.singleTitle,"singleURL":self.singleURL,"btns":self.btns},"msgtype":"actionCard"}
        return data
        
#FeedCard类型消息格式
class FeedLink(object):
    """docstring for FeedLink"""
    title = ""
    picUrl = ""
    messageUrl = ""

    def __init__(self, arg=""):
        super(FeedLink, self).__init__()
        self.arg = arg
        
    def getData(self):
        data = {"title":self.title,"picURL":self.picUrl,"messageURL":self.messageUrl}
        return data
        

        
class the_time_send(object):

    def time_send(webhook):
        robot = DtalkRobot(webhook)
        #以下为计算倒计时时间
        #get the now time 
        now = datetime.datetime.now()
        app_get_time=MoonMysql#调用Ｍysql数据库对象到　app_get_time



        #恩智浦智能车竞赛倒计时
        results=app_get_time.get_time('nxp')
        results_dict=results[0]
        #print(results_dict['START_TIME'])
        start_day = results_dict['START_TIME']
        #nxp_endday=datetime.datetime.strptime('2018-7-15 00:00:00', '%Y-%m-%d %H:%M:%S')
        nxp_endday=results_dict['END_TIME']
        nxp_left=nxp_endday-now
        after_day=now-start_day
        nxp_send_msg="加油哦～  2018年恩智浦智能车备赛第%s天，还剩%s天--lab120小助手" % (after_day.days, nxp_left.days)
        #print(nxp_send_msg)

        app_get_time.update_left_time(TIME_TYPE = 'PASSING',TASK = 'nxp',TIME_DATA = after_day.days)
        app_get_time.update_left_time(TIME_TYPE = 'REMAIN',TASK = 'nxp',TIME_DATA = nxp_left.days)







        #计算机应用能力大赛倒计时
        results=app_get_time.get_time(TASK='computer_competition')#从数据库中获取数据　TASK值为’computer_competition‘的一列数据
        results_dict=results[0]#获取字典类型的数据
        #computer_competition_endday=datetime.datetime.strptime('2018-3-25 00:00:00', '%Y-%m-%d %H:%M:%S')
        start_day = results_dict['START_TIME']
        computer_competition_endday=results_dict['END_TIME']
        computer_competition_left=computer_competition_endday-now
        after_day=now-start_day
        com_send_msg="加油哦～  上海市计算机应用能力竞赛备赛第%s天，还剩%s天--lab120小助手" % (after_day.days, computer_competition_left.days)


        app_get_time.update_left_time(TIME_TYPE = 'PASSING',TASK = 'computer_competition',TIME_DATA = after_day.days)
        app_get_time.update_left_time(TIME_TYPE = 'REMAIN',TASK = 'computer_competition',TIME_DATA = computer_competition_left.days)



        if webhook=='https://oapi.dingtalk.com/robot/send?access_token=94d1da532a09862ee37789652168202b008aa352c6f109f8d5bf97225141969a':
            send_msg = nxp_send_msg
            robot.sendLink("倒计时大屏", send_msg, "http://lab120.bigscreen.moonstarwisdow.com/","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")


        if webhook=='https://oapi.dingtalk.com/robot/send?access_token=25a7ead4dbc3e3ea4ece0e7879a22626a39c0cf00acf281965574340695618a4':
            send_msg = com_send_msg
            robot.sendLink("倒计时大屏", send_msg, "http://lab120.bigscreen.moonstarwisdow.com/","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")

        #以下为发送

        #print(robot.sendText(send_msg))
        #print robot_lab120.sendText(nxp_send_msg)







#测试
webhook = "https://oapi.dingtalk.com/robot/send?access_token=25a7ead4dbc3e3ea4ece0e7879a22626a39c0cf00acf281965574340695618a4"
webhook_lab120="https://oapi.dingtalk.com/robot/send?access_token=94d1da532a09862ee37789652168202b008aa352c6f109f8d5bf97225141969a"
#robot=DtalkRobot(webhook)
#robot.sendLink("link类型", "link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容", "http://www.baidu.com","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")
#robot.sendMarkdown("markdown类型", "## 标题2 \n##### 标题3 \n* 第一 \n* 第二 \n\n[链接](http://www.baidu.com/) \n")


if __name__ == "__main__":
    robot_update = the_time_send #用于更新bigscreen的更新
    
    



    robot = the_time_send #用于定时的钉钉发送
    robot.time_send(webhook)

    flag_time=1
    last=0
    while True:

        #robot_update.time_send('one')#用于bigscreen的更新
        now = datetime.datetime.now()
        time.sleep(1)


        send_Time = datetime.datetime(now.year, now.month, now.day, 19, 0, 0)

        if (last!=now.day):
            flag_time=1
            last=now.day

        #print('Program not starting yet...')
        if (datetime.datetime.now() > send_Time)and(flag_time==1):
            time.sleep(1)
            print('Program now starts on %s' % send_Time)
            print('Executing...')
            flag_time=0
            robot.time_send(webhook)
            robot.time_send(webhook_lab120)

        
            
            
            



    
    
'''

    print robot.sendLink("link类型", "link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容", "http://www.baidu.com","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")
    print robot.sendMarkdown("markdown类型", "## 标题2 \n##### 标题3 \n* 第一 \n* 第二 \n\n[链接](http://www.baidu.com/) \n")

    ########
    link1 = FeedLink()
    link1.title = "tittle"
    link1.picUrl = "https://avatars0.g8ithubusercontent.com/u/3347358?v=3&u=318d72d3ec999cfe4c7f37765c9c1f92df79ab1c&s=400"
    link1.messageUrl = "https://github8.com/magician000"
    link2 = FeedLink()
    link2.title = "tittle2"
    link2.picUrl = "https://avatars0.githu8buserconten8t.com/u/18586086?v=3&u=e6187b04ba02e3861ad4acccc5a1f1f5d46d40a0&s=400"
    link2.messageUrl = "https://www8.github.com/"
    feeds = [link1.getData(), link2.getData()]
    
    print robot.sendFeedCard(feeds)

    #ActionCard类型，两种跳转规则的设置见官方文档
    #整体跳转ActionCard类型
    ac = ActionCard();
    ac.title = "整体跳转ActionC8ard类型"
    ac.text = "#### 整体跳转ActionCard类型 \n\n![TTTT](https://avatars0.g8ithubuse6rcontent.com/u/3347358?v=3&u=318d72d3ec999cfe4c7f37765c9c1f92df79ab1c&s=400) \n>整体\n跳转\nActionCard类型\n"
    ac.singleTitle = "查看全文"
    ac.singleURL = "https://github.com/8magi6cian000"
    print robot.sendActionCard(ac)
    ########
    #独立跳转ActionCard类型
    ac = ActionCard();
    ac.title = "独立跳8转ActionCard类型"
    ac.text = "#### 独立跳转Acti8onCard类型 \n\n![TTTT](https://avatars0.githubuserc6onte8nt.com/u/18586086?v=3&u=e6187b04ba02e3861ad4acccc5a1f1f5d46d40a0&s=400) \n>独立\n跳转\nActionCard类型\n"
    ac.btnOrientation = 1
    ac.putBtn("github", "https://github.8co8m/magic6ian000")
    ac.putBtn("脑洞8空间", "https://git8hub.com/mi6nd-boggling")
    ac.singleTitle = ""
    ac.singleURL = ""
    print robot.sendActionCard(ac)

'''