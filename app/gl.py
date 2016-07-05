# -*- coding: UTF-8 -*-
__author__ = 'wangdongxing'

TOKEN = 'wangdongxing'
ENCODINGAESKEY = 'VrfDVqIyVyxQEGIDjrTZTBAEEuIYAx9Tnk9nvZPWF3t'
MY_HOST = 'http://wangdongxing.tech'
APPID = 'wxfda724dc0050ab97'
APPSECRET = '7a2a6add1935f3799408369cbc6fea9d'
REFRESH_ACCESS_TOKEN_INTERVAL = 7000
COUNT_USER_RELATION_INTERVAL = 10
ACCESS_TOKEN = None
MY_WX_ID = 'gh_00be8f45ad24'

conn = None

error = "不知道你说啥呢"
no_face = MY_HOST + '/static/img/no_face.png'
da_shang = MY_HOST + '/static/img/dashang.jpg'
da_shang_html = MY_HOST + '/dashang.html'

welcome = "欢迎关注我的公众号！\n" \
          "我的身边有这样的一群男男女女，他们追求梦想，他们积极向上，他们在事业的道路上越走越长，" \
          "然而事到如今，他们独身前行却仍然还没有对象。\n" \
          "各位都是本宝宝的朋友，所以建立这样的一个平台，帮助大家有机会互相认识。\n" \

menu = "回复【1】收集你的信息\n" \
       "回复【2】计算你的匹配\n" \
       "回复【3】查看你的匹配\n" \
       "回复【4】查看你的信息\n" \
       "回复【5】查看互相喜欢\n" \
       "回复【6】打赏本宝宝\n"

begin_question = "确认开始收集你的信息？【是|否】"

begin_relation = "要找和你匹配几分以上的人呢(会随机出现一人，可多次回复【3】查看匹配)?【0-100分】"

questions = [
    '你是否是单身？【是|否】',
    '你的昵称？',
    '你的微信号(放心吧，互相Like之后，你的微信号才会被对方看到)?',
    '你的性别？【男|女】',
    '你的生日？【格式：19901105】',
    '你的家乡？【格式：河北+石家庄】',
    '你的工作地？【格式：北京+北京】',
    '你的大学？【格式：河北+保定+河北大学】',
    '你的职业?【IT|销售|文员|管理|whatever】多选一',
    '你的爱好？【格式：乒乓球+游泳】',
    '你的择偶要求？',
    '你的靓照（真实个人照片哦）？',
    '收集完成，感谢配合。\n回复【2】可计算匹配'
]