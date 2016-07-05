# -*- coding: UTF-8 -*-
__author__ = 'wangdongxing'

import urllib2
import urllib
import json
import gl
from myxml import *
from db import *
import random


def accept():
    return 'hello'


def subscribe(from_user_name):
    return mk_text_msg(from_user_name, gl.MY_WX_ID, gl.welcome + gl.menu)


def unsubscribe(from_user_name):
    return 'success'


def menu_click(from_user_name, event_key):
    return 'success'


def http_post(url, data):
    json_data = urllib.urlencode(data)
    req = urllib2.Request(url, json_data)
    response = urllib2.urlopen(req)
    return response.read()


def http_get(url):
    response = urllib2.urlopen(url)
    return response.read()


def get_wx_access_token(app_id, app_secret):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+app_id+'&secret='+app_secret
    json_result_str = http_get(url)
    ret = json.loads(json_result_str)
    return ret['access_token']


def get_user_info(open_id):
    if gl.ACCESS_TOKEN is not None:
        access_token = gl.ACCESS_TOKEN
    else:
        access_token = get_wx_access_token(gl.APPID, gl.APPSECRET)

    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token='+access_token+'&openid='+open_id+'&lang=zh_CN'
    json_result_str = http_get(url)
    ret = json.loads(json_result_str)
    return ret


def refresh_access_token():
    print 'refresh access_token ...'
    gl.ACCESS_TOKEN = get_wx_access_token(gl.APPID, gl.APPSECRET)


def get_my_info(from_user_name):
    info = get_my_db_info(from_user_name)
    if info.__len__() == 0 or info is None or info[0] is None:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，还没有你的信息，回复【1】开始收集你的信息。')
    else:
        name = info[0][0]
        if name is None:
            name = '我'
        return mk_user_info_msg(from_user_name,gl.MY_WX_ID,name,info[0][1],info[0][2],from_user_name)


def begin_my_relation(from_user_name):
    if has_user(from_user_name) > 0:
        step, status = get_user_status(from_user_name)
        if status == 1:
            return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，你的信息不完整,'+gl.questions[step])
        update_user_question_status(from_user_name, 2)
        return mk_text_msg(from_user_name, gl.MY_WX_ID, gl.begin_relation)
    else:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，还没有你的信息，回复【1】开始收集你的信息。')


def get_my_darling(from_user_name, score):
    if score.isdigit():
        user = get_my_all_db_info(from_user_name)
        ret = get_my_relations(from_user_name, user['sex'], score)
        if ret.__len__() == 0:
            update_user_question_status(from_user_name, 0)
            return mk_text_msg(from_user_name, gl.MY_WX_ID, '没有匹配的人，可以回复【3】重新设置下分数，或者回复【1】重新填写信息')
        else:
            update_user_question_status(from_user_name, 0)
            x = ret[random.randint(0, ret.__len__()-1)]
            if user['sex'] == 1:
                x_main_id = x[1]
            else:
                x_main_id = x[0]
            x_man = get_my_db_info(x_main_id)
            name = x_man[0][0] + '('+x[2].__str__()+'分)'
            return mk_user_info_msg(from_user_name, gl.MY_WX_ID, name, x_man[0][1], x_man[0][2], x_main_id)
    else:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '分数是数字格式哦，亲！'+gl.begin_relation)


def collect_user_info(from_user_name, code):
    if has_user(from_user_name) > 0:
        if code == '1':
            return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，重新填写信息，相当于重启操作，之前的所有记录会丢失哦。回复【11】开始重填？')
        clear_user(from_user_name)
        insert_user(from_user_name)
    else:
        insert_user(from_user_name)

    return mk_text_msg(from_user_name,gl.MY_WX_ID,gl.questions[0])


def get_all_like(from_user_name):
    user = get_my_all_db_info(from_user_name)
    if user is None:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，还没有你的信息，回复【1】开始填写你的信息。')

    step, status = get_user_status(from_user_name)
    if status == 1:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，你的信息不完整,'+gl.questions[step])
    others = get_all_each_like(from_user_name)
    if others is None:
        return mk_text_msg(from_user_name, gl.MY_WX_ID, '亲，还没有和你互相Like的，再等下哦。')
    title = []
    description = []
    picurl = []
    url = []
    for o in others:
        if user['sex'] == 1:
            u = get_my_all_db_info(o[1])
            o_id = o[1]
        else:
            u = get_my_all_db_info(o[0])
            o_id = o[0]
        title.append(u['name']+"("+o[2].__str__()+"分)"+"的个人信息")
        description.append(u['song'])
        picurl.append(u['face'])
        url.append('http://wangdongxing.tech/user_info?x_id={0}&viewer_id={1}'.format(u['open_id'], o_id))

    return mk_full_list_text_msg(from_user_name, gl.MY_WX_ID, others.__len__(), title, description, picurl, url)


def do_question_0(step, open_id, content):
    msg = None
    if content == '是':
        next_user_question(step + 1, open_id)
        msg = gl.questions[step+1]
    elif content == '否':
        msg = '不是单身，瞎玩什么!'
        update_user_question_status(open_id, 0)
    else:
        msg = gl.questions[step]

    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_1(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'name', content)
    next_user_question(step + 1, open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_2(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'wechatId', content)
    next_user_question(step + 1, open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_3(step, open_id, content):
    # msg = None
    if content == '男':
        next_user_question(step + 1, open_id)
        update_user(open_id, 'sex', 1)
        msg = gl.questions[step+1]
    elif content == '女':
        next_user_question(step + 1, open_id)
        update_user(open_id, 'sex', 0)
        msg = gl.questions[step+1]
    else:
        msg = gl.questions[step]

    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_4(step, open_id, content):
    msg = gl.questions[step + 1]
    if content.__len__() == 8:
        age = get_now_year() - int(content.__getslice__(0, 4))
        update_user(open_id, 'birthday', content)
        update_user(open_id, 'age', age)
        next_user_question(step + 1, open_id)
    else:
        msg = '请按照格式填写哦'
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_5(step, open_id, content):
    arr = content.split("+")
    if arr.__len__() == 2:
        update_user(open_id, 'province', arr[0])
        update_user(open_id, 'city', arr[1])
        msg = gl.questions[step + 1]
        next_user_question(step + 1, open_id)
    else:
        msg = '请按照格式填写哦'

    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_6(step, open_id, content):
    arr = content.split("+")
    if arr.__len__() == 2:
        update_user(open_id, 'work_province', arr[0])
        update_user(open_id, 'work_city', arr[1])
        msg = gl.questions[step + 1]
        next_user_question(step + 1, open_id)
    else:
        msg = '请按照格式填写哦'
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_7(step, open_id, content):
    arr = content.split("+")
    if arr.__len__() == 3:
        update_user(open_id, 'colleage_province', arr[0])
        update_user(open_id, 'colleage_city', arr[1])
        update_user(open_id, 'colleage_name', arr[1])
        msg = gl.questions[step + 1]
        next_user_question(step + 1, open_id)
    else:
        msg = '请按照格式填写哦'
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_8(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'industry', content)
    next_user_question(step + 1, open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_9(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'hobby', content)
    next_user_question(step + 1, open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_10(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'song', content)
    next_user_question(step + 1, open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_11(step, open_id, content):
    msg = gl.questions[step + 1]
    update_user(open_id, 'face', content)
    next_user_question(step + 1, open_id)
    over_user_question(open_id)
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def do_question_12(step, open_id, content):
    msg = None
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def count_my_relation(open_id):
    user = get_my_all_db_info(open_id)
    if user is None:
        return mk_text_msg(open_id,gl.MY_WX_ID, '亲，还没有你的信息，回复【1】开始收集你的信息。')
    step, status = get_user_status(open_id)
    if status == 1:
        return mk_text_msg(open_id, gl.MY_WX_ID, '亲，你的信息不完整,'+gl.questions[step])
    if user['sex'] == 1:
        other = get_users_by_sex(0)
        if other is not None:
            count = 0
            for o in other:
                score = count_score(user, o)
                has = get_relation(user['open_id'], o['open_id'])
                if has is not None:
                    print 'update one ...'
                    count += 1
                    update_user_relation(user['open_id'], o['open_id'], score)
                else:
                    if score >= 10:
                        print 'insert one ...'
                        count += 1
                        insert_user_relation(user['open_id'], o['open_id'], score)
            msg = '亲，计算成功'+count.__str__()+'条匹配,回复【3】查看你的匹配。'
        else:
            msg = '亲，暂时还没有异性朋友加入，请稍后重新回复【2】计算匹配。'
    else:
        other = get_users_by_sex(1)
        if other is not None:
            count = 0
            for o in other:
                score = count_score(o, user)
                has = get_relation(o['open_id'], user['open_id'])
                if has is not None:
                    print 'update one ...'
                    count += 1
                    update_user_relation(o['open_id'], user['open_id'], score)
                else:
                    if score >= 50:
                        print 'insert one ...'
                        count += 1
                        insert_user_relation(o['open_id'], user['open_id'], score)
            msg = '亲，计算成功'+count.__str__()+'条匹配,回复【3】查看你的匹配。'
        else:
            msg = '亲，暂时还没有异性朋友加入，请稍后重新回复【2】计算匹配。'
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def count_user_relation():
    print 'begin to count ...'
    men = get_users_by_sex(1)
    women = get_users_by_sex(0)
    if men is not None and women is not None:
        for man in men:
            for woman in women:
                score = count_score(man, woman)
                has = get_relation(man['open_id'], woman['open_id'])
                if has is not None:
                    print 'update one ...'
                    update_user_relation(man['open_id'], woman['open_id'], score)
                else:
                    if score >= 50:
                        print 'insert one ...'
                        insert_user_relation(man['open_id'], woman['open_id'], score)
    print 'over to count ...'


def count_score(man, woman):
    score = 0
    if abs(man['age'] - woman['age']) <= 3:
        score += 10
    if man['province'] == woman['province']:
        score += 10
    if man['city'] == woman['city']:
        score += 20
    if man['work_province'] == woman['work_province']:
        score += 10
    if man['work_city'] == woman['work_city']:
        score += 10
    if man['colleage_province'] == woman['colleage_province']:
        score += 5
    if man['colleage_city'] == woman['colleage_city']:
        score += 5
    if man['colleage_name'] == woman['colleage_name']:
        score += 20
    if man['industry'] == woman['industry']:
        score += 20

    return score


def get_robot_reply(open_id, content):
    url = "http://www.tuling123.com/openapi/api"
    data = {}
    data['key'] = '177f9cdd745563bb37b5b4aa156b7de2'
    data['info'] = content
    data['userid'] = open_id
    ret_str = http_post(url, data)
    ret = json.loads(ret_str)
    if ret['code'] == 100000:
        msg = ret['text']
    else:
        msg = '亲爱的，不明白你说的什么意思！'
    return mk_text_msg(open_id, gl.MY_WX_ID, msg)


def da_shang(open_id):
    description = '维护域名不需要成本么？\n' \
                  '维护服务器不需要成本么？\n' \
                  '为了开发周末不能出去玩要痛苦么？\n' \
                  '要！要！要！\n' \
                  '求各位小主捐赠打赏一下本宝宝哈！'
    return mk_full_text_msg(open_id, gl.MY_WX_ID, '捐赠打赏作者', description, gl.da_shang,gl.da_shang_html)