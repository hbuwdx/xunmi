# -*- coding: UTF-8 -*-
__author__ = 'wangdongxing'
from xml.dom.minidom import parseString
import time
from datetime import datetime


def get_million_time():
    return int(round(time.time() * 1000))


def get_now_year():
    return datetime.today().year


def parse_xml_data(data):
    dom_tree = parseString(data)
    root = dom_tree.documentElement
    return root


def mk_text_msg(to_user_name, from_user_name, content):
    msg = '<xml>'\
          '<ToUserName><![CDATA['+to_user_name+']]></ToUserName>' \
          '<FromUserName><![CDATA['+from_user_name+']]></FromUserName>' \
          '<CreateTime>'+get_million_time().__str__()+'</CreateTime>' \
          '<MsgType><![CDATA[text]]></MsgType>' \
          '<Content><![CDATA['+content+']]></Content>' \
          '</xml>'
    return msg


def mk_image_msg(to_user_name, from_user_name, media_id):
    msg = '<xml>' \
          '<ToUserName><![CDATA['+to_user_name+']]></ToUserName>' \
          '<FromUserName><![CDATA['+from_user_name+']]></FromUserName>' \
          '<CreateTime>'+get_million_time().__str__()+'</CreateTime>' \
          '<MsgType><![CDATA[image]]></MsgType>' \
          '<Image>' \
          '<MediaId><![CDATA['+media_id+']]></MediaId>' \
          '</Image>' \
          '</xml>'
    return msg


def mk_video_msg(to_user_name, from_user_name, media_id, description):
    msg = '<xml>' \
          '<ToUserName><![CDATA['+to_user_name+']]></ToUserName>' \
          '<FromUserName><![CDATA['+from_user_name+']]></FromUserName>' \
          '<CreateTime>'+get_million_time().__str__()+'</CreateTime>' \
          '<MsgType><![CDATA[video]]></MsgType>' \
          '<Video>' \
          '<MediaId><![CDATA['+media_id+']]></MediaId>' \
          '<<Description><![CDATA['+description+']]></Description>' \
          '</Video>' \
          '</xml>'
    return msg


def mk_full_text_msg(to_user_name, from_user_name, title, description, picurl, url):
    msg = '<xml>' \
          '<ToUserName><![CDATA['+to_user_name+']]></ToUserName>' \
          '<FromUserName><![CDATA['+from_user_name+']]></FromUserName>' \
          '<CreateTime>'+get_million_time().__str__()+'</CreateTime>' \
          '<MsgType><![CDATA[news]]></MsgType>' \
          '<ArticleCount>1</ArticleCount>' \
          '<Articles>' \
          '<item>' \
          '<Title><![CDATA['+title+']]></Title>' \
          '<Description><![CDATA['+description+']]></Description>' \
          '<PicUrl><![CDATA['+picurl+']]></PicUrl>' \
          '<Url><![CDATA['+url+']]></Url>' \
          '</item>' \
          '</Articles>' \
          '</xml>'
    return msg


def mk_user_info_msg(to_user_name, from_user_name, name, desc, pic_url, open_id):
    if name is None:
        return -1
    if desc is None:
        desc = '暂无择偶条件'
    if pic_url is None:
        pic_url = 'http://baidu.com'
    return mk_full_text_msg(to_user_name, from_user_name, name+'的个人信息',
                            desc, pic_url,
                            'http://wangdongxing.tech/user_info?x_id={0}&viewer_id={1}'.format(open_id, to_user_name))


def mk_full_list_text_msg(to_user_name, from_user_name, num, title, description, picurl, url):
    msg = '<xml>' \
          '<ToUserName><![CDATA['+to_user_name+']]></ToUserName>' \
        '<FromUserName><![CDATA['+from_user_name+']]></FromUserName>' \
        '<CreateTime>'+get_million_time().__str__()+'</CreateTime>' \
        '<MsgType><![CDATA[news]]></MsgType>' \
        '<ArticleCount>'+num.__str__()+'</ArticleCount>' \
        '<Articles>'
    for i in range(0, num):
        msg += '<item><Title><![CDATA['+title[i]+']]></Title><Description><![CDATA['+description[i]+']]></Description>' \
            '<PicUrl><![CDATA['+picurl[i]+']]></PicUrl>' \
                                          '<Url><![CDATA['+url[i]+']]></Url></item>'
    msg += '</Articles></xml>'
    return msg