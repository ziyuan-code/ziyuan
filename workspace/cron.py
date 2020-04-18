#!/usr/bin/env python3
import pymysql

conn = pymysql.connect('127.0.0.1', 'root', '123', 'account_data')
cur = conn.cursor()
sql = 'select * from account'
cc = cur.execute(sql)
user = cur.fetchall()
def user_data():
    for i in range(cc):
        userlist = user[i][0]
        conn = pymysql.connect('127.0.0.1', 'root', '123', '{}'.format(userlist))
        cur = conn.cursor()
        sql = 'select * from {}_ziyuan'.format(userlist)
        count = cur.execute(sql)
        data_ = cur.fetchall()
        cur.scroll(0, 'absolute')
        sql_jian = 'select * from {}_jianshe'.format(userlist)
        cur.execute(sql_jian)
        data_jian = cur.fetchall()
        minju = int(data_jian[0][3])
        cangku = int(data_jian[0][4])
        bingying = int(data_jian[0][2])
        shi = int(data_[0][0])
        tie = int(data_[0][1])
        liang = int(data_[0][3])
        mu = int(data_[0][2])
        jin = int(data_[0][5])
        zhengbing = int(data_[0][6])
        shi += 1000
        tie += 1000
        liang += 1000
        mu += 1000
        jin += 500
        zhengbing += 1000
        xian_shui = 30000 + minju*10240
        xian_cang = 30000 + cangku*10240
        xian_bing = 10000 + bingying*5000
        if shi < xian_cang:
            sql_up = 'update %s_ziyuan set 石料=%d where id=1' %(userlist,shi)
            cur.execute(sql_up)
        if tie < xian_cang:
            sql_up = 'update %s_ziyuan set 铁矿=%d where id=1' %(userlist,tie)
            cur.execute(sql_up)
        if liang < xian_cang:
            sql_up = 'update %s_ziyuan set 粮食=%d where id=1' %(userlist,liang)
            cur.execute(sql_up)
        if mu < xian_cang:
            sql_up = 'update %s_ziyuan set 木材=%d where id=1' %(userlist,mu)
            cur.execute(sql_up)
        if jin < xian_shui:
            sql_up = 'update %s_ziyuan set 金币=%d where id=1' %(userlist,jin)
            cur.execute(sql_up)
        if zhengbing < xian_bing:
            sql_up = 'update %s_ziyuan set 征兵=%d where id=1' %(userlist,zhengbing)
            cur.execute(sql_up)
        conn.commit()
        cur.close()
        conn.close()
def main():
    user_data()
if __name__ == '__main__': 
    main()


