# -*- coding: UTF-8 -*-
__author__ = 'wangdongxing'
import MySQLdb
import gl


def get_conn():
    if gl.conn is None:
        gl.conn = MySQLdb.connect(host='localhost', user='root', passwd='Hbuwdx123', db='xunmi', port=3306)


def create_table():
    get_conn()
    sql1 = 'CREATE TABLE user_question(' \
           'open_id varchar(255) NOT NULL,' \
           'step int(11) NOT NULL DEFAULT 0,' \
           'status int(11) NOT NULL DEFAULT 0)'
    sql2 = 'CREATE TABLE user_wx (' \
           'name varchar(10),' \
           'age int(11),' \
           'birthday varchar(8),' \
           'province varchar(128),' \
           'city varchar(128),' \
           'work_province varchar(128),' \
           'work_city varchar(128),' \
           'colleage_province varchar(128),' \
           'colleage_city varchar(128),' \
           'colleage_name varchar(128),' \
           'hobby varchar(256),' \
           'industry varchar(32),' \
           'face varchar(128),' \
           'wechatId varchar(32),' \
           'song varchar(256),' \
           'sex int(1),' \
           'open_id varchar(32)' \
           ')'

    sql3 = 'CREATE TABLE user_relation(' \
           'man_id varchar(32) not NULL ,' \
           'woman_id varchar(32) NOT NULL ,' \
           'score INT (11) not NULL ,' \
           'man_like int(1) DEFAULT 0, ' \
           'woman_like int(1) DEFAULT 0)'

    execute_sql(gl.conn, sql1)
    execute_sql(gl.conn, sql2)
    execute_sql(gl.conn, sql3)


def execute_sql(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def query(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    results = []
    for row in cursor:
        results.append(row)
    return results


def close_conn(conn):
    conn.close()


def has_user(open_id):
    get_conn()
    sql = "select count(1) from user_wx where open_id='{0}'".format(open_id)
    ret = query(gl.conn, sql)
    if ret.__len__() > 0:
        return ret[0][0]
    return -1


def get_user_status(open_id):
    get_conn()
    sql = "select step,status from user_question where open_id='{0}'".format(open_id)
    ret = query(gl.conn, sql)
    if ret.__len__() > 0:
        return ret[0][0], ret[0][1]
    return -1, -1


def insert_user(open_id):
    get_conn()
    execute_sql(gl.conn, "insert into user_wx(open_id,face) values('{0}','{1}')".format(open_id, gl.no_face))
    execute_sql(gl.conn, "insert into user_question(open_id,step,status) values('{0}',{1},{2})".format(open_id, 0, 1))


def update_user(open_id, field, val):
    get_conn()
    if isinstance(val, basestring):
        execute_sql(gl.conn, "update user_wx set {0}='{1}' where open_id ='{2}'".format(field, val, open_id))
    else:
        execute_sql(gl.conn, "update user_wx set {0}={1} where open_id ='{2}'".format(field, val, open_id))


def get_my_db_info(open_id):
    get_conn()
    ret = query(gl.conn, "select name,song,face from user_wx where open_id='{0}'".format(open_id))
    return ret


def convert_to_user(db_ret):
    user = {}
    user['name'] = db_ret[0]
    user['age'] = db_ret[1]
    user['birthday'] = db_ret[2]
    user['province'] = db_ret[3]
    user['city'] = db_ret[4]
    user['work_province'] = db_ret[5]
    user['work_city'] = db_ret[6]
    user['colleage_province'] = db_ret[7]
    user['colleage_city'] = db_ret[8]
    user['colleage_name'] = db_ret[9]
    user['hobby'] = db_ret[10]
    user['industry'] = db_ret[11]
    user['face'] = db_ret[12]
    user['wechatId'] = db_ret[13]
    user['song'] = db_ret[14]
    user['sex'] = db_ret[15]
    user['open_id'] = db_ret[16]
    return user


def get_my_all_db_info(open_id):
    get_conn()
    ret = query(gl.conn, "select name,age,birthday,province,city,work_province,"
                         "work_city,colleage_province,colleage_city,colleage_name,hobby,"
                         "industry,face,wechatId,song,sex,open_id from user_wx where open_id='{0}'".format(open_id))
    if ret.__len__() == 0:
        return None
    return convert_to_user(ret[0])


def get_users_by_sex(sex):
    get_conn()
    ret = query(gl.conn, "select name,age,birthday,province,city,work_province,"
                         "work_city,colleage_province,colleage_city,colleage_name,hobby,"
                         "industry,face,wechatId,song,sex,open_id from user_wx where sex={0}".format(sex))
    if ret.__len__() == 0:
        return None
    users = []
    for r in ret:
        users.append(convert_to_user(r))
    return users


def get_my_relations(open_id, sex, score):
    get_conn()
    if sex == 1:
        ret = query(gl.conn, "select man_id,woman_id,score from user_relation "
                             "where score > {1} and  man_id='{0}'"
                             "  ORDER by score desc limit 0,100".format(open_id, score))
    else:
        ret = query(gl.conn, "select man_id,woman_id,score from user_relation "
                             "where score > {1} and  woman_id='{0}'"
                             "  ORDER by score desc limit 0,100".format(open_id, score))
    return ret


def clear_user(open_id):
    get_conn()
    execute_sql(gl.conn, "delete from user_wx where open_id='{0}'".format(open_id))
    execute_sql(gl.conn, "delete from user_question where open_id='{0}'".format(open_id))
    execute_sql(gl.conn, "delete from user_relation where man_id='{0}' or woman_id='{0}'".format(open_id))


def next_user_question(next, open_id):
    get_conn()
    execute_sql(gl.conn, "update user_question set step={0} where open_id='{1}'".format(next, open_id))


def over_user_question(open_id):
    get_conn()
    execute_sql(gl.conn, "update user_question set status=0 where open_id='{0}'".format(open_id))


def update_user_question_status(open_id, status):
    get_conn()
    execute_sql(gl.conn, "update user_question set status={0} where open_id='{1}'".format(status, open_id))


def insert_user_info(user):
    get_conn()
    sql = "insert into user_wx(name,age,birthday,province,city,work_province," \
          "work_city,colleage_province,colleage_city,colleage_name,hobby,industry,face,wechatId,song,sex,open_id) " \
          "VALUES('{0}',{1},{2},'{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}',{15},'{16}')"\
        .format(user['name'], user['age'], user['birthday'], user['province'], user['city'], user['work_province'],
                user['work_city'], user['colleage_province'], user['colleage_city'], user['colleage_name'],
                user['hobby'], user['industry'], user['face'], user['wechatId'], user['song'], user['sex'],
                user['open_id'])
    execute_sql(gl.conn, sql)


def insert_user_relation(man_id, woman_id, score):
    get_conn()
    execute_sql(gl.conn, "insert into user_relation(man_id,woman_id,score,man_like,woman_like) "
                         "values('{0}','{1}',{2},{3},{4})".format(man_id, woman_id, score, 0, 0))


def update_user_relation(man_id, woman_id, score):
    get_conn()
    execute_sql(gl.conn, "update user_relation set score = {0} where man_id ='{1}' and woman_id='{2}'"
                .format(score, man_id, woman_id))


def update_like(user_id, view_id):
    get_conn()
    user = get_my_all_db_info(user_id)
    if user['sex'] == 1:
        sql = "update user_relation set woman_like = 1 where man_id = '{0}' " \
              "and woman_id ='{1}' ".format(user_id, view_id)
    else:
        sql = "update user_relation set man_like = 1 where man_id = '{0}' and woman_id ='{1}' ".format(view_id, user_id)

    execute_sql(gl.conn, sql)


def get_relation(user_id, view_id):
    get_conn()
    ret = query(gl.conn, "select man_id,woman_id,score,man_like,woman_like from "
                         "user_relation where (man_id='{0}' and woman_id='{1}') "
                         "or (man_id='{1}' and woman_id='{0}')".format(user_id, view_id))
    if ret.__len__() > 0:
        return ret[0]


def get_all_each_like(user_id):
    get_conn()
    ret = query(gl.conn, "select man_id,woman_id,score,man_like,woman_like from "
                         "user_relation where (man_id='{0}' or woman_id='{0}') "
                         "and man_like = 1 and woman_like = 1 order by score desc ".format(user_id))
    if ret.__len__() > 0:
        return ret


def get_db_info():
    get_conn()
    a1 = query(gl.conn, 'select count(1) from user_relation where man_like = 1 and woman_like = 1')
    a2 = query(gl.conn, 'select count(1) from user_wx')
    a3 = query(gl.conn, 'select count(1) from user_relation')
    a4 = query(gl.conn, 'select count(1) from user_relation r left join user_wx w on r.man_id = w.open_id '
                        'where r.woman_like = 1 and w.wechatId = \"hbuwdx123\"')
    return a1, a2, a3, a4


def get_relation_monitor():
    get_conn()
    sql = "select m.name as mname,w.name as wname,m.wechatId as mwechatId,w.wechatId as wwechatId," \
          "r.man_like,r.woman_like,r.score from user_relation r " \
          "left join user_wx m on m.open_id = r.man_id " \
          "left join user_wx w on w.open_id = r.woman_id "
    return query(gl.conn, sql)


def clear_db():
    get_conn()
    execute_sql(gl.conn, 'drop table IF EXISTS user_wx')
    execute_sql(gl.conn, 'drop table IF EXISTS user_question')
    execute_sql(gl.conn, 'drop table IF EXISTS user_relation')
    create_table()


def init_db(open_id):
    for i in range(1, 4):
        user = {}
        user['name'] = '一个女人'+i.__str__()
        user['age'] = 24 + i
        user['birthday'] = '19901105'
        user['province'] = '河北'
        user['city'] = '石家庄'
        user['work_province'] = '北京'
        user['work_city'] = '北京'
        user['colleage_province'] = '河北'
        user['colleage_city'] = '保定'
        user['colleage_name'] = '河北大学'
        user['hobby'] = '预埋去'
        user['industry'] = 'IT'
        user['face'] = 'ddd'
        user['wechatId'] = 'hbuwdx'+i.__str__()
        user['song'] = 'love'
        user['sex'] = 0
        user['open_id'] = open_id+i.__str__()
        insert_user_info(user)




