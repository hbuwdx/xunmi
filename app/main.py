# -*- coding: UTF-8 -*-
__author__ = 'wangdongxing'


from flask import Flask
from flask import request
from flask import render_template
from myxml import *
from service import *
import gl
import sys
from db import *

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


app = Flask(__name__)


@app.route('/user_info', methods=['GET'])
def user_info():
    my_open_id = request.args['x_id']
    view_open_id = request.args['viewer_id']
    if my_open_id == view_open_id:
        isme = 1
        all_like = 1
    else:
        isme = 0
        ret = get_relation(my_open_id, view_open_id)
        if ret is not None:
            if int(ret[3]) == 1 and int(ret[4]) == 1:
                all_like = 1
            else:
                all_like = 0
        else:
            return render_template('no_auth.html')

    me = get_my_all_db_info(my_open_id)
    return render_template('user_info.html', user=me, view_id=view_open_id, isme=isme, all_like=all_like)


@app.route('/dashang.html', methods=['GET'])
def da_shang_wo():
    return render_template('da_shang.html')


@app.route('/like', methods=['POST'])
def like():
    user_id = request.form['user_id']
    view_id = request.form['view_id']
    update_like(user_id, view_id)
    return render_template('like_yes.html')


@app.route('/mon.html')
def monitor():
    d = get_relation_monitor()
    return render_template('monitor.html', data=d)


@app.route('/to_reg.html', methods=['GET'])
def to_reg():
    open_id = request.args['open_id']
    return render_template('to_reg.html', open_id=open_id)


@app.route('/reg.html',methods=['POST'])
def reg():
    user = {}
    user['name'] = request.form['name']
    user['wechatId'] = request.form['wechatId']
    user['sex'] = request.form['sex']
    user['height'] = request.form['height']
    user['birthday'] = request.form['birthday']
    colleage_place = request.form['colleage_place']
    user['colleage_name'] = request.form['colleage_name']
    user['industry'] = request.form['industry']
    work_place = request.form['work_place']
    home_place = request.form['home_place']
    user['hobby'] = request.form['hobby']
    user['song'] = request.form['song']
    user['face'] = request.form['face']
    # insert_user_info(user)
    print user
    return render_template('like_yes.html')


@app.route('/dispatch.html')
def dispatch():
    if request.method == 'GET':
        signature = request.args['signature']
        timestamp = request.args['timestamp']
        nonce = request.args['nonce']
        echostr = request.args['echostr']
        return echostr
    elif request.args == 'POST':
        request.form['open_id']

    return ''


@app.route('/checkToken', methods=['GET', 'POST'])
def check_token():
    if request.method == 'GET':

        signature = request.args['signature']
        timestamp = request.args['timestamp']
        nonce = request.args['nonce']
        echostr = request.args['echostr']
        return echostr

    elif request.method == 'POST':

        msg = parse_xml_data(request.get_data())
        msg_type = msg.getElementsByTagName('MsgType')[0].firstChild.data
        to_user_name = msg.getElementsByTagName('ToUserName')[0].firstChild.data
        from_user_name = msg.getElementsByTagName('FromUserName')[0].firstChild.data
        try:
            if msg_type == 'text':
                content = msg.getElementsByTagName('Content')[0].firstChild.data
                if content == '1':
                    return collect_user_info(from_user_name, content)

                if content == '2':
                    return count_my_relation(from_user_name)

                if content == '3':
                    return begin_my_relation(from_user_name)

                if content == '4':
                    return get_my_info(from_user_name)

                if content == '5':
                    return get_all_like(from_user_name)

                if content == '6':
                    return da_shang(from_user_name)

                if content == '11':
                    return collect_user_info(from_user_name, content)

                if content == '101010':
                    clear_db()
                    return "success"

                if content == '101020':
                    init_db(from_user_name)
                    return "success"

                if content == '101030':
                    ret = get_db_info()
                    return mk_text_msg(from_user_name, to_user_name, ret.__str__())

                step, status = get_user_status(from_user_name)
                if status == 1:
                    return eval('do_question_{0}'.format(step))(step, from_user_name, content)
                elif status == 2:
                    return get_my_darling(from_user_name, content)
                else:
                    return get_robot_reply(from_user_name, content)

            if msg_type == 'image':
                pic_url = msg.getElementsByTagName('PicUrl')[0].firstChild.data
                step, status = get_user_status(from_user_name)
                if status == 1:
                    return eval('do_question_{0}'.format(step))(step, from_user_name, pic_url)
                else:
                    return mk_text_msg(from_user_name, to_user_name, '你给照片干嘛？')

            if msg_type == 'event':
                event = msg.getElementsByTagName('Event')[0].firstChild.data
                if event == 'subscribe':
                    return subscribe(from_user_name)
                elif event == 'unsubscribe':
                    return unsubscribe(from_user_name)
                elif event == 'CLICK':
                    event_key = msg.getElementsByTagName('EventKey')[0].firstChild.data
                    return menu_click(from_user_name, event_key)
                else:
                    return 'error'
        except:
            print '=== STEP ERROR INFO START'
            import traceback
            traceback.print_exc()
            print '=== STEP ERROR INFO END'
            return mk_text_msg(from_user_name, to_user_name, '额......我有点小崩溃')

    return 'success'

if __name__ == '__main__':
    # gl.conn = get_conn()
    app.run('0.0.0.0', 80, True)
