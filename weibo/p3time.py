    #!/usr/bin/env python
#coding=utf-8
#set softtabstop=0
"""


学习python时做的练习，纯粹为了娱乐
如果存在bug请自行修改，不提供任何支持




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


    def post(self, data):
        print(data)
        headers = {
            'Content-Type':'application/json;charset=utf-8'
        }
        post_data = json.dumps(data)
        res = requests.post(self.webhook, data=post_data, headers=headers)
        #req.add_header('Content-Type','application/json') 
        return res.text


        

def time_send():

    #以下为计算倒计时时间
    d1 = datetime.datetime.strptime('2017-10-10 00:00:00', '%Y-%m-%d %H:%M:%S')
    nxp_endday=datetime.datetime.strptime('2018-7-15 00:00:00', '%Y-%m-%d %H:%M:%S')
    computer_competition_endday=datetime.datetime.strptime('2018-3-25 00:00:00', '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    delta=now-d1
    nxp_left=nxp_endday-now
    computer_competition_left=computer_competition_endday-now
    send_msg="离上海市计算机应用能力竞赛作品提交还剩%s天，加油哦～--来自lab120小助手" % computer_competition_left.days
    nxp_send_msg="加油哦～  离恩智浦智能车竞赛还剩%s天--来自lab120小助手" % nxp_left.days
    print(robot.sendText(send_msg))
    #print robot_lab120.sendText(nxp_send_msg)







#测试
webhook = "https://oapi.dingtalk.com/robot/send?access_token=25a7ead4dbc3e3ea4ece0e7879a22626a39c0cf00acf281965574340695618a4"
webhook_lab120="https://oapi.dingtalk.com/robot/send?access_token=94d1da532a09862ee37789652168202b008aa352c6f109f8d5bf97225141969a"


if __name__ == "__main__":
    robot = DtalkRobot(webhook)    
    robot_lab120=DtalkRobot(webhook_lab120)

    flag_time=1
    last=0
    while True:
        now = datetime.datetime.now()
        time.sleep(1)
        print(now.day)
        send_Time = datetime.datetime(now.year, now.month, now.day, 12, 0, 0)
        
        if (last!=now.day):
            flag_time=1
            last=now.day

        print('Program not starting yet...')
        if (datetime.datetime.now() > send_Time)and(flag_time==1):
            time.sleep(1)
            print('Program now starts on %s' % send_Time)
            print('Executing...')
            flag_time=0
            time_send()
            
            



    
    

'''
    print robot.sendLink("link类型", "link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容link类型内容", "http://www.baidu.com","http://scimg.jb51.net/allimg/160716/103-160G61012361X.jpg")
    print robot.sendMarkdown("markdown类型", "## 标题2 \n##### 标题3 \n* 第一 \n* 第二 \n\n[链接](http://www.baidu.com/) \n")

    ########
    link1 = FeedLink()
    link1.title = "我的gi8thub"
    link1.picUrl = "https://avatars0.g8ithubusercontent.com/u/3347358?v=3&u=318d72d3ec999cfe4c7f37765c9c1f92df79ab1c&s=400"
    link1.messageUrl = "https://github8.com/magician000"
    link2 = FeedLink()
    link2.title = "githu8b官网"
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