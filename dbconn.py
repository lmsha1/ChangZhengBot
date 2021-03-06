'''
Descripttion: 
version: 
Author: Catop
Date: 2021-02-10 09:10:27
LastEditTime: 2021-02-14 23:24:05
'''
#coding:utf-8
import pymysql

'''连接数据库配置'''
conn = pymysql.connect(host='127.0.0.1',user = "qqbot",passwd = "0551dc3717",db = "qqbot")


def check_cmd(user_id):
    #获取最近一条命令
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    #结果返回dict
    sql = f"SELECT last_cmd FROM userinfo WHERE user_id={user_id} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    last_cmd = cursor.fetchone()['last_cmd']
    conn.commit()
    
    return last_cmd


def check_register(user_id):
    #检查用户是否注册
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT uid FROM userinfo WHERE user_id={user_id} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    user_info = cursor.fetchall()
    conn.commit()

    if(len(user_info)>=1):
        return 1
    else:
        return 0

def insert_img(user_id,file_name,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores):
    params = [file_name,user_id,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores]
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"INSERT INTO imginfo(file_name,user_id,upload_date,upload_time,ocr_err_code,ocr_times,ocr_scores) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    conn.commit()

    return 


def get_user(user_id):
    #获取用户姓名和班级
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT user_name,user_class FROM userinfo WHERE user_id={user_id} LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    user_info = cursor.fetchone()
    conn.commit()

    return user_info




def register_user(user_id,user_name,user_class):
    #注册新用户

    try:
        params = [user_id,user_name,user_class]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"INSERT INTO userinfo(user_id,user_name,user_class) VALUES(%s,%s,%s)"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        flag=0
    else:
        flag=1


    return flag

def re_register_user(user_id,user_name,user_class):
    #重新注册，更新用户信息
    try:
        params = [user_name,user_class,user_id]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"UPDATE userinfo SET user_name=%s,user_class=%s WHERE user_id=%s"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        flag=0
    else:
        flag=1
    
    return flag

def check_today_upload(user_id,upload_date):
    #检查用户当日是否已经上传过
    user_id = str(user_id)
    upload_date = str(upload_date)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT imgid FROM imginfo WHERE(user_id={user_id} AND upload_date='{upload_date}')"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    if(len(cursor.fetchall())>=1):
        return 1
        conn.commit()
    else:
        return 0
        conn.commit()

def check_status(user_id):
    #返回指定用户最新一条记录的时间
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT upload_date FROM imginfo WHERE user_id={user_id} ORDER BY upload_date DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    try:
        last_date = cursor.fetchone()['upload_date']
        conn.commit()
    except TypeError:
        last_date = '1970-01-01'
        
    return last_date

def get_class_members(user_class):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [user_class]
    sql = f"SELECT user_id FROM userinfo WHERE user_class=%s"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    sql_ret = cursor.fetchall()
    conn.commit()
    class_menbers = []

    for i in range(0,len(sql_ret)):
        class_menbers.append(sql_ret[i]['user_id'])
    return class_menbers


def get_latest_img_info(user_id,upload_date):
    """获取指定用户指定时间最新照片信息"""
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    params = [user_id,upload_date]
    sql = f"SELECT * FROM imginfo WHERE (user_id=%s AND upload_date=%s) ORDER BY imgid DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql,params)
    sql_ret = cursor.fetchall()
    conn.commit()

    return sql_ret
    
def manual_update(ocr_times,ocr_scores,imgid):
    #更新手动核对信息
    try:
        params = [ocr_times,ocr_scores,imgid]
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = f"UPDATE imginfo SET ocr_err_code=-1,ocr_times=%s,ocr_scores=%s WHERE imgid=%s"
        conn.ping(reconnect=True)
        cursor.execute(sql,params)
        conn.commit()
    except:
        flag=0
    else:
        flag=1
    
    return flag

def err_check(imgid):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT ocr_err_code FROM imginfo WHERE imgid={imgid} ORDER BY upload_date DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    try:
        ocr_err_code = cursor.fetchone()['ocr_err_code']
        conn.commit()
    except:
        flag = 0    
    else:
        flag = 1

    return ocr_err_code


def get_user_by_migid(imgid):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f"SELECT user_id FROM imginfo WHERE imgid={imgid} ORDER BY upload_date DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor.execute(sql)
    try:
        user_id = cursor.fetchone()['user_id']
        conn.commit()
    except:
        flag = 0    
    else:
        flag = 1
    cursor1 = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql1 = f"SELECT user_name FROM userinfo WHERE user_id={user_id} ORDER BY uid DESC LIMIT 1"
    conn.ping(reconnect=True)
    cursor1.execute(sql1)
    try:
        user_name = cursor1.fetchone()['user_name']
        conn.commit()
    except:
        flag = 0    
    else:
        flag = 1

    return user_name
    



if __name__=='__main__':
    #print(get_user(601179193))
    #insert_img('601179193','test.jpg','2021-02-10','09:47:49')
    #print(check_today_upload('601179193','2021-02-10'))
    #print(register_user('29242764','李四','信安20-1'))
    #print(check_status(601179193))
    #print(get_class_members('信安20-2'))
    print(get_latest_img_info('601179193','2021-02-13'))
    
