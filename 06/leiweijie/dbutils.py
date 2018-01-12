#!/usr/bin/env python
# encoding: utf-8
'''
@author: leiweijie
Create on2018年1月6日
'''
import MySQLdb as mysql
import gconf
def execute_sql(sql,args=(),fetch=True):
    conn = None
    cur = None
    count = 0
    rt_list = []
    try:
        conn = mysql.connect(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT,
                             user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWORD,
                             db=gconf.MYSQL_DB, charset=gconf.CHARSET)
        cur = conn.cursor()
        count = cur.execute(sql, args)
        if fetch:
            rt_list = cur.fetchall()
        else:
            conn.commit()
    except Exception as e:
        print e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return count,rt_list
def executemany_sql(sql,args=(),fetch=True):
    conn = None
    cur = None
    count = 0
    rt_list = []
    try:
        conn = mysql.connect(host=gconf.MYSQL_HOST, port=gconf.MYSQL_PORT,
                             user=gconf.MYSQL_USER, passwd=gconf.MYSQL_PASSWORD,
                             db=gconf.MYSQL_DB, charset=gconf.CHARSET)
        cur = conn.cursor()
        count = cur.executemany(sql, args)
        if fetch:
            rt_list = cur.fetchall()
        else:
            conn.commit()
    except Exception as e:
        print e
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return count,rt_list

