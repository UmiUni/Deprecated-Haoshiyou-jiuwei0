# -*- coding: UTF-8 -*-  
import requests
import itchat
from itchat.content import *
import sys  
import json
import time
from time import sleep
reload(sys)  
sys.setdefaultencoding('utf8')
freq = {}
usersDict = {}
itchat.auto_login(enableCmdQR=2,hotReload=True)
itchat.get_chatrooms(update=True)

v0= u"您好，湾区九尾萌盟小助手😊为您服务～\n"
v1= u"回复 1 加九尾萌盟聚餐活动群;\n"
v2= u"回复 2 加九尾萌盟【南湾】;\n"
v3= u"回复 3 加九尾萌盟【东湾】;\n"
v4= u"回复 4 加九尾萌盟棋牌社;\n"
v5= u"回复 5 加九尾萌盟湾区车行。\n"
vT =v0+v1+v2+v3+v4+v5
def getName(chatroomName):
    itchat.get_chatrooms(update=True)
    cur_chatrooms = itchat.search_chatrooms(name=chatroomName)
    detailedChatroom = itchat.update_chatroom(cur_chatrooms[0]['UserName'], detailedMember=True)
    #print(json.dumps(cur_chatrooms)+"\n")
    return detailedChatroom["UserName"]

@itchat.msg_register('Friends')
def add_friend(msg):
    #print("add message:")
    #print(json.dumps(msg))
    #msg.user.verify()
    #itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    #itchat.add_friend(userName = msg['RecommendInfo']['UserName'], status=3, verifyContent=u'UIUC万群汇总', autoUpdate=True)
    #msg.user.send(vT)
    #response = itchat.add_friend(userName = CurUserName, status=3, autoUpdate=True)
    itchat.send_msg(vT, msg['RecommendInfo']['UserName'])

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : '8028064e9e2f46c78a111276823f94b1',
        'info'   : msg,
        'userid' : 'superchaoran',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return msg
#"ChatRoomOwner": "@cb680fd93595dafaaeb9c915e08c8d0c6ec5878f4a8e33612ab0ba95c2dc3992"
# 这里是我们在“1. 实现微信消息的获取”中已经用到过的同样的注册方法
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    CurUserName = msg['FromUserName']
    #print(json.dumps(response)+"\n")
    print("userid:"+CurUserName+"\n") 
    if(CurUserName in usersDict):
        usersDict[CurUserName] = usersDict[CurUserName] + 1
        if(usersDict[CurUserName] >= 7):
            itchat.send_msg(u'您已达到今日加群上限，请明日再来～😊', CurUserName)
            return
    else:
        usersDict[CurUserName] = 1

    msgText = msg['Text']
    if "1" in msgText and ("10" not in msgText):
      pullMembersMore(msg, u'九尾萌盟聚餐', CurUserName)
      sleep(0.5)
    elif "2" in msgText:
      pullMembersMore(msg, u'九尾萌盟【南湾】租房', CurUserName)
      sleep(0.5)
    elif "3" in msgText:
      pullMembersMore(msg, u'九尾萌盟【东湾】租房', CurUserName)
      sleep(0.5)
    elif "4" in msgText:
      pullMembersMore(msg, u'九尾萌盟棋牌', CurUserName)
      sleep(0.5)
    elif "5" in msgText:
      pullMembersMore(msg, u'🚗九尾萌盟湾区车', CurUserName)
      sleep(0.5)
    itchat.send_msg(vT, CurUserName)
    sleep(0.5)

def pullMembersMore(msg, chatroomName, CurUserName):
    cur_chatrooms = itchat.search_chatrooms(name=chatroomName)
    #print(json.dumps(cur_chatrooms)+"\n")
    chatRoomUserName = cur_chatrooms[0]['UserName']
    #print(chatRoomUserName + "\n")
    #print(CurUserName+ "\n")
    r = itchat.add_member_into_chatroom(chatRoomUserName,[{'UserName':CurUserName}],useInvitation=True)

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    msgS = msg.text
    '''
    print(msg['isAt'])
    print(msg['ActualNickName'])
    print(msg['Content'])
    '''
    '''
    if "@Stanford加群" in msg['Content']:
        replyS = get_response(msgS)
        if msg.actualNickName.count("@")>=2:
            msg.user.send(u'%s' % (replyS+'~想进群加我😊 '))
        else:
            msg.user.send(u'@%s\u2005%s' % (msg.actualNickName, replyS+'~想进群加我😊 '))
    '''
    if msg['ActualNickName']=="超然":
      content = msg['Content']
      if(content[0]=="@"):
        arr = content.rsplit(None,1)
        if "广告" in arr[1]:
          delUser = searchUser(msg['User']['MemberList'],arr[0])
          itchat.delete_member_from_chatroom(msg['FromUserName'],[{'UserName':delUser}])
          msg.user.send('谢谢，已清除~😊')

def searchUser(users,target):
  for user in users:
    if(user['NickName']==target[1:] or user['DisplayName']==target):
      return user['UserName']



itchat.run() 




