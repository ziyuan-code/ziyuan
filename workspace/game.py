#!/usr/bin/env python3
import random
import pymysql
import os
import time
import getpass

menu='''
1：登陆游戏
2：创建账号
3：退出游戏
请选择操作：'''

menu1='''
1：武将
2：建筑
3：内政
4：点将台
5：征伐
6：返回
请选择操作：'''

def yanzheng(conn, cur, cc, userlist):
    if cc == 0:
        print('请先注册账号。')
        return 500
    account = input('请输入你的账号：')
    passwd = getpass.getpass('请输入你的密码：')
    for i in range(cc):
        if userlist[i][0] == account and userlist[i][1] == passwd:
            os.system('clear')
            print('欢迎{}登陆游戏！'.format(account))
            time.sleep(0.5)
            return account
        else:
            pass
        if i == cc-1:
            print('账号或密码错误。')
            return 502

def zhuce(conn,cur, cc, userlist):
    zhuce_account = input('请输入注册账号：')
    if len(zhuce_account) < 3 or len(zhuce_account) > 16:
        print('账号长度应在【3-16】之间')
        return
    if cc == 0:
        pass
    else:
        for i in range(cc):
            if userlist[i][0] == zhuce_account:
                print('账号已存在！')
                return
    zhuce_passwd = getpass.getpass('请输入注册密码：')
    if len(zhuce_passwd) < 8 or len(zhuce_passwd) > 16:
        print('密码长度应在【8-16】之间')
        return
    sql_ce = "insert into account set user='%s', passwd='%s'" %(zhuce_account,zhuce_passwd)
    cur.execute(sql_ce)
    conn.commit()
    cur.close()
    conn.close()
    os.system("mysql -uroot -p123 -e 'create database %s'" %zhuce_account)
    os.system("mysql -uroot -p123 {} -e 'create table {}_jianshe (城主府 int(10) default 0, 校场 int(10) default 0, 兵营 int(10) default 0, 民居 int(10)default 0, 仓库 int(10) default 0, id int(10) default 1)'".format(zhuce_account, zhuce_account))
    os.system("mysql -uroot -p123 {} -e 'create table {}_ziyuan (石料 int(10)default 30000, 铁矿 int(10) default 30000, 木材 int(10) default 30000, 粮食 int(10) default 50000, id int(10) default 1, 金币 int(10) default 0, 征兵 int(10) default 0)'".format(zhuce_account, zhuce_account))
    os.system("mysql -uroot -p123 {} -e 'create table {}_wjlist (名字 char(20), 攻击距离 int(10) default 0, 攻击 int(10) default 0, 防御 int(10) default 0, 速度 int(10) default 0)'".format(zhuce_account, zhuce_account))
    os.system("mysql -uroot -p123 {} -e 'create table {}_budui (前锋 char(20), 中军 char(20), 大营 char(20), 前锋兵力 int(10) default 100, 中军兵力 int(10) default 100, 大营兵力 int(10) default 100, id int(10) primary key auto_increment)'".format(zhuce_account, zhuce_account))
    os.system('''mysql -uroot -p123 {} -e "insert into {}_wjlist set 名字='曹操', 攻击距离=2, 攻击=128, 防御=295, 速度=126"'''.format(zhuce_account,zhuce_account))
    os.system('''mysql -uroot -p123 {} -e "insert into {}_wjlist set 名字='刘备', 攻击距离=3, 攻击=154, 防御=185, 速度=92"'''.format(zhuce_account,zhuce_account))
    os.system('''mysql -uroot -p123 {} -e "insert into {}_wjlist set 名字='孙权', 攻击距离=4, 攻击=122, 防御=128, 速度=164"'''.format(zhuce_account,zhuce_account))
    os.system('''mysql -uroot -p123 {} -e "insert into {}_jianshe set id=1"'''.format(zhuce_account,zhuce_account))
    os.system('''mysql -uroot -p123 {} -e "insert into {}_ziyuan set id=1"'''.format(zhuce_account,zhuce_account))
    print('账号注册成功：%s' %zhuce_account)


def login():
    while True:
        anniu = input(menu)
        conn = pymysql.connect('127.0.0.1', 'root', '123', 'account_data', charset='utf8')
        cur = conn.cursor()
        sql = 'select * from account'
        cc = cur.execute(sql)
        userlist = cur.fetchall()
        if cc != 0:
            cur.scroll(0, 'absolute')
        if anniu == '1':
            qq = yanzheng(conn,cur,cc,userlist)
            if qq == 500:
                break
            if qq == 502:
                pass
            else:
                return qq,200
        elif anniu == '2':
            zhuce(conn,cur,cc,userlist)
        elif anniu == '3':
            exit()
        else:
            print('请输入正确选项')

def wujiang(zhu):
    menu = '''
1：我的武将
2：我的部队
3：武将图鉴
4：退出
请选择操作：'''
    while True:
        user = zhu[0]
        conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
        cur = conn.cursor()
        sql = 'select * from %s_wjlist' %user
        cc = cur.execute(sql)
        wjlist = cur.fetchall()
        cur.scroll(0, 'absolute')
        cur.close()
        conn.close()
        conne = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
        curs = conne.cursor()
        sq = 'select * from %s_budui' %user
        acc = curs.execute(sq)
        bdlist = curs.fetchall()
        if acc != 0:
            curs.scroll(0, 'absolute')
        curs.close()
        conne.close()
        con = pymysql.connect('127.0.0.1', 'root', '123', 'account_data')
        cu = con.cursor()
        s = 'select * from wujiang'
        c = cu.execute(s)
        wj = cu.fetchall()
        cu.scroll(0, 'absolute')
        cu.close()
        con.close()
        se = input(menu)
        if se == '1':
            for i in range(cc):
                time.sleep(0.2)
                print('武将：',wjlist[i][0],'\t攻距：',wjlist[i][1],'\t杀伤：',wjlist[i][2], '\t防御：',wjlist[i][3], '\t速度：',wjlist[i][4])
        elif se == '2':
            if acc == 0:
                print('没有配置的队伍。')
            else:
                for j in range(acc):
                    time.sleep(0.2)
                    print('第%d支部队' %(j+1))
                    print('前锋：',bdlist[j][0],'兵力：',bdlist[j][3])
                    print('中军：',bdlist[j][1],'兵力：',bdlist[j][4])
                    print('大营：',bdlist[j][2],'兵力：',bdlist[j][5])
        elif se == '3':
            for s in range(c):
                time.sleep(0.2)
                print('武将：',wj[s][0],'\t攻距：',wj[s][1],'\t杀伤：',wj[s][2], '\t防御：',wj[s][3], '\t速度：',wj[s][4])
        elif se == '4':
            return
        else:
            print('请输入正确选项。')
                
def jianshe(zhu):
    user = zhu[0]
    while True:
        conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
        cur = conn.cursor()
        sql = 'select * from %s_jianshe' %user
        cc = cur.execute(sql)
        jianzu = cur.fetchall()
        cur.scroll(0, 'absolute')
        sql_ziyuan = 'select * from %s_ziyuan' %user
        cur.execute(sql_ziyuan)
        ziyuan = cur.fetchall()
        cur.scroll(0, 'absolute')
        print('当前资源：\n','石料：',ziyuan[0][0],'\t铁矿：',ziyuan[0][1],'\t木材：',ziyuan[0][2],'\t粮食：',ziyuan[0][3])
        menu='''
1：城主府 %d/8
2：校场\t  %d/5
3：兵营\t  %d/20
4：民居\t  %d/20
5：仓库\t  %d/20
6：返回
请选择升级建筑：''' %(jianzu[0][0],jianzu[0][1],jianzu[0][2],jianzu[0][3],jianzu[0][4])
        select = input(menu)
        hao = 0
        if select == '1':
            a = int(jianzu[0][0])
            hao = 5000 + a*a*1024
            if int(ziyuan[0][0]) > hao and int(ziyuan[0][1]) > hao and int(ziyuan[0][2]) > hao:
                if int(jianzu[0][0]) <= 8:
                    yu_shi = int(ziyuan[0][0]) - hao
                    yu_tie = int(ziyuan[0][1]) - hao
                    yu_mu = int(ziyuan[0][2]) - hao
                    sql_ziyuan = 'update %s_ziyuan set 石料=%d where id = 1' %(user,yu_shi)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 铁矿=%d where id = 1' %(user,yu_tie)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 木材=%d where id = 1' %(user,yu_mu)
                    cur.execute(sql_ziyuan)
                    sql_jian = 'update %s_jianshe set 城主府=%d+1 where id=1' %(user,int(jianzu[0][0]))
                    cur.execute(sql_jian)
                    conn.commit()
                    print("\033[32;1m 升级成功！\033[0m")
                else:
                    print("\033[31;1m 不满足升级条件\033[0m")
            else:
                print('升级所需资源为：铁：%s' %hao, '石：%s' %hao, '木：%s' %hao)
                print("\033[31;1m 您的资源不足！\033[0m")

        elif select == '2':
            a = int(jianzu[0][1])
            hao = 5000 + a*a*1024
            if int(ziyuan[0][0]) > hao and int(ziyuan[0][1]) > hao and int(ziyuan[0][2]) > hao:
                if int(jianzu[0][0]) >=2 and int(jianzu[0][1]) <= 5:
                    yu_shi = int(ziyuan[0][0]) - hao
                    yu_tie = int(ziyuan[0][1]) - hao
                    yu_mu = int(ziyuan[0][2]) - hao
                    sql_ziyuan = 'update %s_ziyuan set 石料=%d where id = 1' %(user,yu_shi)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 铁矿=%d where id = 1' %(user,yu_tie)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 木材=%d where id = 1' %(user,yu_mu)
                    cur.execute(sql_ziyuan)
                    sql_jian = 'update %s_jianshe set 校场=%d+1 where id=1' %(user,int(jianzu[0][1]))
                    cur.execute(sql_jian)
                    conn.commit()
                    print("\033[32;1m 升级成功！\033[0m")
                else:
                    print("\033[31;1m 不满足升级条件\033[0m")
            else:
                print('升级所需资源为：铁：%s' %hao, '石：%s' %hao, '木：%s' %hao)
                print("\033[31;1m 您的资源不足！\033[0m")
            
        elif select == '3':
            a = int(jianzu[0][2])
            hao = 1000 + a*a*1024
            if int(ziyuan[0][0]) > hao and int(ziyuan[0][1]) > hao and int(ziyuan[0][2]) > hao:
                if int(jianzu[0][0]) >= 7 and int(jianzu[0][2]) <= 20:
                    yu_shi = int(ziyuan[0][0]) - hao
                    yu_tie = int(ziyuan[0][1]) - hao
                    yu_mu = int(ziyuan[0][2]) - hao
                    sql_ziyuan = 'update %s_ziyuan set 石料=%d where id = 1' %(user,yu_shi)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 铁矿=%d where id = 1' %(user,yu_tie)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 木材=%d where id = 1' %(user,yu_mu)
                    cur.execute(sql_ziyuan)
                    sql_jian = 'update %s_jianshe set 兵营=%d+1 where id=1' %(user,int(jianzu[0][2]))
                    cur.execute(sql_jian)
                    conn.commit()
                    print("\033[32;1m 升级成功！\033[0m")
                else:
                    print("\033[31;1m 不满足升级条件\033[0m")
            else:
                print('升级所需资源为：铁：%s' %hao, '石：%s' %hao, '木：%s' %hao)
                print("\033[31;1m 您的资源不足！\033[0m")
            
        elif select == '4':
            a = int(jianzu[0][3])
            hao = 500 + a*1024
            if int(ziyuan[0][0]) > hao and int(ziyuan[0][1]) > hao and int(ziyuan[0][2]) > hao:
                if int(jianzu[0][0]) >= 2 and int(jianzu[0][3]) <= 20:
                    yu_shi = int(ziyuan[0][0]) - hao
                    yu_tie = int(ziyuan[0][1]) - hao
                    yu_mu = int(ziyuan[0][2]) - hao
                    sql_ziyuan = 'update %s_ziyuan set 石料=%d where id = 1' %(user,yu_shi)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 铁矿=%d where id = 1' %(user,yu_tie)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 木材=%d where id = 1' %(user,yu_mu)
                    cur.execute(sql_ziyuan)
                    sql_jian = 'update %s_jianshe set 民居=%d+1 where id=1' %(user,int(jianzu[0][3]))
                    cur.execute(sql_jian)
                    conn.commit()
                    print("\033[32;1m 升级成功！\033[0m")
                else:
                    print("\033[31;1m 不满足升级条件\033[0m")
            else:
                print('升级所需资源为：铁：%s' %hao, '石：%s' %hao, '木：%s' %hao)
                print("\033[31;1m 您的资源不足！\033[0m")
            
        elif select == '5':
            a = int(jianzu[0][4])
            hao = 500 + a*1024
            if int(ziyuan[0][0]) > hao and int(ziyuan[0][1]) > hao and int(ziyuan[0][2]) > hao:
                if int(jianzu[0][0]) >= 2 and int(jianzu[0][4]) <= 20: 
                    yu_shi = int(ziyuan[0][0]) - hao
                    yu_tie = int(ziyuan[0][1]) - hao
                    yu_mu = int(ziyuan[0][2]) - hao
                    sql_ziyuan = 'update %s_ziyuan set 石料=%d where id = 1' %(user,yu_shi)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 铁矿=%d where id = 1' %(user,yu_tie)
                    cur.execute(sql_ziyuan)
                    sql_ziyuan = 'update %s_ziyuan set 木材=%d where id = 1' %(user,yu_mu)
                    cur.execute(sql_ziyuan)
                    sql_jian = 'update %s_jianshe set 仓库=%d+1 where id=1' %(user,int(jianzu[0][4]))
                    cur.execute(sql_jian)
                    conn.commit()
                    print("\033[32;1m 升级成功！\033[0m")
                else:
                    print("\033[31;1m 不满足升级条件\033[0m")
            else:
                print('升级所需资源为：铁：%s' %hao, '石：%s' %hao, '木：%s' %hao)
                print("\033[31;1m 您的资源不足！\033[0m")
            
        elif select == '6':
            cur.close()
            conn.close()
            return
            
        else:
            print('请选择正确操作。')

def budui(user):
    conne = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
    curs = conne.cursor()
    sq = 'select * from %s_budui' %user
    acc = curs.execute(sq)
    bdlist = curs.fetchall()
    if acc != 0:
        curs.scroll(0, 'absolute')
    curs.close()
    conne.close()
    if acc == 0:
        print('没有配置的队伍。')
        return 100
    else:
        for j in range(acc):
            time.sleep(0.2)
            print('第%d支部队' %(j+1))
            print('前锋：',bdlist[j][0],'兵力：',bdlist[j][3])
            print('中军：',bdlist[j][1],'兵力：',bdlist[j][4])
            print('大营：',bdlist[j][2],'兵力：',bdlist[j][5])
        return acc

def shuishou(user):
    conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
    cur = conn.cursor()
    sql = 'select * from %s_ziyuan' %user
    cc = cur.execute(sql)
    ziyuan = cur.fetchall()
    cur.close()
    conn.close()
    return ziyuan

def select_ww(user, bd, menu1):  
    while True:
        conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
        cur = conn.cursor()
        sql = 'select * from %s_budui' %user
        count = cur.execute(sql)
        bd_data = cur.fetchall()
        sql_bing = 'select * from %s_ziyuan' %user
        cur.execute(sql_bing)
        bing_data = cur.fetchall()
        print('前锋：',bd_data[bd][3],'\n中军：',bd_data[bd][4],'\n大营：',bd_data[bd][5], '\n预备兵：', int(bing_data[0][6]))
        sebd = input(menu1)
        if sebd == '1':
            cz = int(bd_data[bd][3])             #武将带兵数量
            c1 = int(input('请输入征兵数量：'))  #添兵
            c2 = cz + c1                         #预期兵力
            c3 = int(bing_data[0][6]) - c1       #预备兵
            cx = 10000 - c2                      #单武将带兵上限
            if c1 < int(bing_data[0][6]):
                if cx >= 0:
                    sql_qian = 'update {}_budui set 前锋兵力={} where id={}'.format(user,c2,bd+1)
                    cur.execute(sql_qian)
                    yubei = 'update {}_ziyuan set 征兵={} where id=1'.format(user,c3)
                    cur.execute(yubei)
                    cur.close()
                    conn.commit()
                    print('征兵成功！')
            else:
                print('征兵数量不足。')
        elif sebd == '2':
            cz = int(bd_data[bd][4])             #武将带兵数量
            c1 = int(input('请输入征兵数量：'))  #添兵
            c2 = cz + c1                         #预期兵力
            c3 = int(bing_data[0][6]) - c1       #预备兵
            cx = 10000 - c2                      #单武将带兵上限
            if c1 < int(bing_data[0][6]):
                if cx >= 0:
                    sql_qian = 'update {}_budui set 中军兵力={} where id={}'.format(user,c2,bd+1)
                    cur.execute(sql_qian)
                    yubei = 'update {}_ziyuan set 征兵={} where id=1'.format(user,c3)
                    cur.execute(yubei)
                    cur.close()
                    conn.commit()
                    print('征兵成功！')
            else:
                print('征兵数量不足。')
          
        elif sebd == '3':
            cz = int(bd_data[bd][5])             #武将带兵数量
            c1 = int(input('请输入征兵数量：'))  #添兵
            c2 = cz + c1                         #预期兵力
            c3 = int(bing_data[0][6]) - c1       #预备兵
            cx = 10000 - c2                      #单武将带兵上限
            if c1 < int(bing_data[0][6]):
                if cx >= 0:
                    sql_qian = 'update {}_budui set 大营兵力={} where id={}'.format(user,c2,bd+1)
                    cur.execute(sql_qian)
                    yubei = 'update {}_ziyuan set 征兵={} where id=1'.format(user,c3)
                    cur.execute(yubei)
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('征兵成功！')
            else:
                print('征兵数量不足。')
            
        elif sebd == '4':
            return
        else:
            print('没有这个位置。')

def allwj(user):
    conn = pymysql.connect('127.0.0.1', 'root', '123', 'account_data')
    cur = conn.cursor()
    sql = 'select * from wujiang'
    count = cur.execute(sql)
    jiang = cur.fetchall()
    cur.close()
    conn.close()
    return jiang

def mwj(user):
    conn = pymysql.connect('127.0.0.1', 'root', '123', '{}'.format(user))
    cur = conn.cursor()
    sql = 'select * from {}_wjlist'.format(user)
    wjcount = cur.execute(sql)
    wj = cur.fetchall()
    sql = 'select * from {}_ziyuan'.format(user)
    cur.execute(sql)
    jinb = cur.fetchall()
    cur.close()
    conn.close()
    mwj = [wjcount,wj,jinb]
    return mwj

def tuntian(user):
    conn = pymysql.connect('127.0.0.1', 'root', '123', '{}'.format(user))
    cur = conn.cursor()
    sql = 'select * from {}_ziyuan'.format(user)
    cur.execute(sql)
    ziyuan = cur.fetchall()
    jin = ziyuan[0][5]
    shi = ziyuan[0][0]
    tie = ziyuan[0][1]
    mu = ziyuan[0][2]
    liang = ziyuan[0][3]
    menu = '''
1：石头
2：铁矿
3：木材
4：粮食
5：返回
请选择屯田种类：'''
    while True:
        print("石料：{}".format(shi), "\n铁矿：{}".format(tie), "\n木材：{}".format(mu), "\n粮食：{}".format(liang))
        tun = input(menu)
        if tun == '1':
            xu = input('屯田需要花费2000金币，换取30000石料，是否继续[y|n]：')
            if xu == 'y':
                jin = jin - 2000
                shi = shi + 30000
                sql_jin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_jin)
                conn.commit()
                sql_shi = 'update {}_ziyuan set 石料={} where id=1'.format(user,shi)
                cur.execute(sql_shi)
                conn.commit()
                time.sleep(1)
                print("恭喜你，屯田成功，获得30000石料！！")

        elif tun == '2':
            xu = input('屯田需要花费2000金币，换取30000铁矿，是否继续[y|n]：')
            if xu == 'y':
                jin = jin - 2000
                tie = tie + 30000
                sql_jin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_jin)
                conn.commit()
                sql_tie = 'update {}_ziyuan set 铁矿={} where id=1'.format(user,tie)
                cur.execute(sql_tie)
                conn.commit()
                time.sleep(1)
                print("恭喜你，屯田成功，获得30000铁矿！！")
            
        elif tun == '3':
            xu = input('屯田需要花费2000金币，换取30000木材，是否继续[y|n]：')
            if xu == 'y':
                jin = jin - 2000
                mu = mu + 30000
                sql_jin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_jin)
                conn.commit()
                sql_mu = 'update {}_ziyuan set 木材={} where id=1'.format(user,mu)
                cur.execute(sql_mu)
                conn.commit()
                time.sleep(1)
                print("恭喜你，屯田成功，获得30000木材！！")

        elif tun == '4':
            xu = input('屯田需要花费3000金币，换取50000粮食，是否继续[y|n]：')
            if xu == 'y':
                jin = jin - 2000
                liang = liang + 50000
                sql_jin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_jin)
                conn.commit()
                sql_liang = 'update {}_ziyuan set 粮食={} where id=1'.format(user,liang)
                cur.execute(sql_liang)
                conn.commit()
                time.sleep(1)
                print("恭喜你，屯田成功，获得50000粮食！！")

        elif tun == '5':
            cur.close()
            conn.close()
            return
        else:
            print('请选择正确操作')

def qiuxian(user):
    menu='''
1：万里访贤
2：千里访贤
3：百里访贤
4：返回
选择求贤模式：'''
    while True:
        conn = pymysql.connect('127.0.0.1', 'root', '123', '{}'.format(user))
        cur = conn.cursor()
        a = allwj(user)
        b = mwj(user)
        aa = set(a)
        bb = set(b[1])
        cc = aa - bb
        sql_jin = 'select * from {}_ziyuan'.format(user)
        cur.execute(sql_jin)
        jz = cur.fetchall()
        jin = jz[0][5]
        fang = input(menu)
        if fang == '1':
            if jin > 0 and len(cc) > 0:
                sel = random.choice(range(1,10,2))
                jin = int(jin) - 5000
                sql_upjin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_upjin)
                conn.commit()
                if sel == 3:
                    print('名将来投!!!')
                    cc = list(cc)
                    sewj = random.choice(cc)
                    sql = "insert into {}_wjlist set 名字='{}', 攻击距离='{}', 攻击='{}', 防御='{}', 速度='{}'".format(user,sewj[0],sewj[1],sewj[2],sewj[3],sewj[4])
                    cur.execute(sql)
                    conn.commit()
                    print('恭喜主公，招募到武将{}!!!'.format(sewj[0]))
                else:
                    print('空手而归')
            else:
                print('金币不足或武将全招募了！')
            cur.close()
            conn.close()
        elif fang == '2':
            if jin > 0 and len(cc):
                sel = random.choice(range(1,15,2))
                jin = int(jin) - 3000
                sql_upjin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_upjin)
                conn.commit()
                if sel == 3:
                    print('名将来投!!!')
                    cc = list(cc)
                    sewj = random.choice(cc)
                    sql = "insert into {}_wjlist set 名字='{}', 攻击距离='{}', 攻击='{}', 防御='{}', 速度='{}'".format(user,sewj[0],sewj[1],sewj[2],sewj[3],sewj[4])
                    cur.execute(sql)
                    conn.commit()
                    print('恭喜主公，招募到武将{}!!!'.format(sewj[0]))
                else:
                    print('空手而归')
            else:
                print('金币不足或武将全招募了')
            cur.close()
            conn.close()
        elif fang == '3':
            if jin > 0 and len(cc):
                sel = random.choice(range(1,20,2))
                jin = int(jin) - 2000
                sql_upjin = 'update {}_ziyuan set 金币={} where id=1'.format(user,jin)
                cur.execute(sql_upjin)
                conn.commit()
                if sel == 3:
                    print('名将来投!!!')
                    cc = list(cc)
                    sewj = random.choice(cc)
                    sql = "insert into {}_wjlist set 名字='{}', 攻击距离='{}', 攻击='{}', 防御='{}', 速度='{}'".format(user,sewj[0],sewj[1],sewj[2],sewj[3],sewj[4])
                    cur.execute(sql)
                    conn.commit()
                    print('恭喜主公，招募到武将{}!!!'.format(sewj[0]))
                else:
                    print('空手而归')
            else:
                print('金币不足或武将全招募了')
            cur.close()
            conn.close()
        elif fang == '4':
            return
        else:
            print('错误选项')

def neizheng(zhu):
    user = zhu[0]
    menu='''
1：税收
2：征兵
3：屯田
4：求贤
5：返回
请选择操作：'''
    menu1 = '''
1：前锋
2：中军
3：大营
4：返回
请选择征兵位置：'''
    while True:
        select = input(menu)
        if select == '1':
            ziyuan = shuishou(user)
            print('当前税收为：',ziyuan[0][5])
        elif select == '2':
            count = budui(user)
            count = int(count)
            if int(count) > 0:
                shang = input('请选择征兵队伍：')
                if shang == '1':
                    bd = 0
                    select_ww(user, bd, menu1)
                elif shang == '2' and count >= 2:
                    bd = 1
                    select_ww(user, bd, menu1)
                elif shang == '3' and count >= 3:
                    bd = 2
                    select_ww(user, bd, menu1)
                elif shang == '4' and count >= 4:
                    bd = 3
                    select_ww(user, bd, menu1)
                elif shang == '5' and count == 5:
                    bd = 4
                    select_ww(user, bd, menu1)
                else:
                    print('部队不存在')
        elif select == '3':
            tuntian(user)
        elif select == '4':
            qiuxian(user)
        elif select == '5':
            return
        else:
            print('请选择正确操作。')

def jiaarm(user,select):
    conn = pymysql.connect('127.0.0.1','root','123','{}'.format(user),charset='utf8')
    cur = conn.cursor()
    sql = 'select * from %s_jianshe' %user
    count = cur.execute(sql)
    jiaochang = cur.fetchall()
    sql_wj = 'select * from %s_wjlist' %user
    cc = cur.execute(sql_wj)
    wjlist = cur.fetchall()
    sql_budui = 'select * from %s_budui' %user
    shu = cur.execute(sql_budui)
    budui = cur.fetchall()
    if int(jiaochang[0][1]) == 0:
        print('当前可配置队伍数量为0队，请升级校场。')
    else:
        menu='''
1：前锋
2：中军
3：大营
4：保存配置
5：返回
请选择配置位置：'''
        zhi = {'前锋':'', '中军':'', '大营':''}
        xuan = {}
        for l in range(cc):
            ll = wjlist[l][0]
            xuan.setdefault('%d' %(l+1),'%s' %ll)
        while True:
            print('前锋：',zhi['前锋'],'\n中军：',zhi['中军'],'\n大营：',zhi['大营'])
            va = []
            sele = input(menu)
            for x,y in xuan.items():
                print(x,'：',y)
                va.append(x)
            if sele == '1':
                qian = input('请选择前锋武将：')
                if qian in va and not zhi['前锋']:
                    zhi['前锋']=xuan['{}'.format(qian)]
                    xuan.pop(qian)
                else:
                    print('没有这个武将')
            elif sele == '2': 
                zhong = input('请选择中军武将：')
                if zhong in va and not zhi['中军']:
                    zhi['中军']=xuan['{}'.format(zhong)]
                    xuan.pop(zhong)
                else:
                    print('没有这个武将')
            elif sele == '3': 
                ying = input('请选择大营武将：')
                if ying in va and not zhi['大营']:
                    zhi['大营']=xuan['{}'.format(ying)]
                    xuan.pop(ying)
                else:
                    print('没有这个武将')
            elif sele == '4':
                snlist = []              #已经配置的部队
                shu = int(shu)
                for sn in range(shu):
                    snlist.append(str(budui[sn][6]))  #append加添到列表后会变成整型？你麻痹坑劳资
                if select in snlist:                  #如果选择配置的队伍已经配置成功，则更新数据
                    sql_all = "update {}_budui set 前锋='{}' where id= {}".format(user,zhi['前锋'],int(select))
                    cur.execute(sql_all)
                    sql_all = "update {}_budui set 中军='{}' where id = {}".format(user,zhi['中军'],int(select))
                    cur.execute(sql_all)
                    sql_all = "update {}_budui set 大营='{}' where id = {}".format(user,zhi['大营'],int(select))
                    cur.execute(sql_all)
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('变更成功。')
                else:
                    sql_all = "insert into {}_budui set 前锋='{}',中军='{}',大营='{}'".format(user,zhi['前锋'],zhi['中军'],zhi['大营'])
                    cur.execute(sql_all)
                    conn.commit()
                    cur.close()
                    conn.close()
                    print('变更成功。')
                    
            else:
                break

def dianjiangtai(zhu):
    user = zhu[0]
    conn = pymysql.connect('127.0.0.1','root','123','{}'.format(user),charset='utf8')
    cur = conn.cursor()
    sql = 'select * from %s_jianshe' %user
    count = cur.execute(sql)
    jiaochang = cur.fetchall()
    ji = jiaochang[0][1]
    print('当前部队：')
    print('*'*50)
    budui(user)
    print('*'*50)
    bian = input('是否变更队伍？')
    if bian == 'y':
        os.system('clear')
        ji = int(ji)
        print('当前可配置部队：')
        print('')
        print('#'*50)
        print('')
        for i in range(ji):
            print('第%d支部队\n' %(i+1))
        select = input('请选择配置队伍：')
        if select == '1' and ji >= 1:
            jiaarm(user,select)
        elif select == '2' and ji >= 2:
            jiaarm(user,select)
        elif select == '3' and ji >= 3:
            jiaarm(user,select)
        elif select == '4' and ji >= 4:
            jiaarm(user,select)
        elif select == '5' and ji >= 5:
            jiaarm(user,select)
        elif select == '6':
            return
        else:
            print('队伍未开放。')

def huihe(npc):
    return npc


def NPC(npc,zhan):
    if zhan == '山贼':
        npc = npc[0]
        npc = huihe(npc)
        print('大营：',npc['daying'],'大营兵力：',npc['ying'],'\n中军：',npc['zhongjun'],'中军兵力：',npc['zhong'],'\n前锋：',npc['qianfeng'],'前锋兵力：',npc['qian'])
        return npc
    if zhan == '流寇':
        npc = npc[2]
        npc = huihe(npc)
        print('大营：',npc['daying'],'大营兵力：',npc['ying'],'\n中军：',npc['zhongjun'],'中军兵力：',npc['zhong'],'\n前锋：',npc['qianfeng'],'前锋兵力：',npc['qian'])
        return npc
    if zhan == '悍匪':
        npc = npc[1]        
        npc = huihe(npc)
        print('大营：',npc['daying'],'大营兵力：',npc['ying'],'\n中军：',npc['zhongjun'],'中军兵力：',npc['zhong'],'\n前锋：',npc['qianfeng'],'前锋兵力：',npc['qian'])
        return npc


def dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist):
    conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
    cur = conn.cursor()
    for i in range(8):
        sulist = [int(qian_shuxing['su']),int(zhong_shuxing['su']),int(ying_shuxing['su']),npc['sujia'],npc['suyi'],npc['subing']]
        print('第%s回合' %(i+1))
        time.sleep(0.7)
        for j in range(6):  #一回合内，六个人，每人行动一次
            time.sleep(0.3)
            xian = max(sulist)
            sulist.remove(xian)
            mubiao1 = [npc['daying'], npc['zhongjun'], npc['qianfeng']] #大营攻击距离为5，中军为4，前锋为3的选取攻击目标
            mubiao2 = [npc['zhongjun'], npc['qianfeng']]                #大营攻击距离为4，中军为3，前锋为2的选取攻击目标
            mubiao3 = [qian_shuxing['jiang'], zhong_shuxing['jiang'], ying_shuxing['jiang']] #敌军选取我军为攻击目标
            if int(npc['qian']) > 0:
                pass
            else:
                mubiao1.remove(npc['qianfeng'])
                mubiao2.remove(npc['qianfeng'])
            if int(npc['zhong']) > 0:
                pass
            else:
                mubiao1.remove(npc['zhongjun'])
                mubiao2.remove(npc['zhongjun'])
                mubiao2.append(npc['daying'])
            if int(qian_shuxing['bing']) > 0:
                pass
            else:
                mubiao3.remove(qian_shuxing['jiang'])
            if int(zhong_shuxing['bing']) > 0:
                pass
            else:
                mubiao3.remove(zhong_shuxing['jiang'])
            if int(ying_shuxing['bing']) > 0:
                pass
            else:
                print('我军大营阵亡，挑战失败')
                return 

            if xian == int(ying_shuxing['su']) and int(ying_shuxing['bing']) > 0: #如果我军大营先手，并且剩余兵力大于0
                print('%s开始行动' %ying_shuxing['jiang'])
                if int(ying_shuxing['ju']) == 5:                            #如果我军大营的攻击距离为5
                    da = random.choice(mubiao1)
                    print('%s对%s发起进攻' %(ying_shuxing['jiang'], da))
                    shang = int(ying_shuxing['ji']) + 0.1*int(ying_shuxing['bing']) 
                    if da == npc['daying']:                                 #如果我军大营攻击敌军大营
                        npc['ying'] = int(npc['ying']) - shang
                        if int(npc['ying']) > 0:                                 #如果敌军大营挨这一下兵力还大于0
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利' %da)
                            npc['ying'] = 0
                            return
                    elif da == npc['zhongjun']:          #前面已经将敌军中军兵力为零时剔除攻击列表，当da选择中军时，说明它还有兵
                        npc['zhong'] = int(npc['zhong']) - shang
                        if npc['zhong'] > 0:
                            print('%s损失%d兵力' %(da, shang)) 
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0             #下一次行动时，将不会选择敌军中军作为攻击目标
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if npc['qian'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                elif int(ying_shuxing['ju']) == 4:  
                    da = random.choice(mubiao2)     #前面已经设置，当前锋死时，将大营加入攻击列表
                    print('%s对%s发起进攻' %(ying_shuxing['jiang'], da))
                    shang = int(ying_shuxing['ji']) + 0.1*int(ying_shuxing['bing']) 
                    if da == npc['zhongjun']:   
                        npc['zhong'] = int(npc['zhong']) - shang
                        if npc['zhong'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0           
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if npc['qian'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                    elif da == npc['daying']:
                        npc['ying'] = int(npc['ying']) - shang
                        if npc['ying'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利！' %da)
                            npc['ying'] = 0
                            return
                elif int(ying_shuxing['ju']) == 3 and npc['qian'] != 0:
                    da = npc['qianfeng']
                    print('%s对%s发起进攻' %(ying_shuxing['jiang'], da))
                    shang = int(ying_shuxing['ji']) + 0.1*int(ying_shuxing['bing']) 
                    npc['qian'] = int(npc['qian']) - shang
                    if npc['qian'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['qian'] = 0
                elif int(ying_shuxing['ju']) == 3 and npc['qian'] == 0 and npc['zhong'] != 0:
                    da = npc['zhongjun']
                    print('%s对%s发起进攻' %(ying_shuxing['jiang'], da))
                    shang = int(ying_shuxing['ji']) + 0.1*int(ying_shuxing['bing']) 
                    npc['zhong'] = int(npc['qian']) - shang
                    if npc['zhong'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['zhong'] = 0
                elif int(ying_shuxing['ju']) == 3 and npc['qian'] == 0 and npc['zhong'] == 0:
                    da = npc['daying']
                    print('%s对%s发起进攻' %(ying_shuxing['jiang'], da))
                    shang = int(ying_shuxing['ji']) + 0.1*int(ying_shuxing['bing']) 
                    npc['ying'] = int(npc['ying']) - shang
                    if npc['ying'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军大营%s阵亡，挑战胜利' %da)
                        npc['ying'] = 0
                        return
                else:
                    print('攻击距离不足，%s无法行动' %ying_shuxing['jiang'])
            elif xian == int(zhong_shuxing['su']) and int(zhong_shuxing['bing']) > 0:
                print('%s开始行动' %zhong_shuxing['jiang'])
                if int(zhong_shuxing['ju']) >= 4:                         
                    da = random.choice(mubiao1)
                    print('%s对%s发起进攻' %(zhong_shuxing['jiang'], da))
                    shang = int(zhong_shuxing['ji']) + 0.1*int(zhong_shuxing['bing']) 
                    if da == npc['daying']:                            
                        npc['ying'] = int(npc['ying']) - shang
                        if npc['ying'] > 0:                           
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利' %da)
                            npc['ying'] = 0
                            return
                    elif da == npc['zhongjun']:     
                        npc['zhong'] = int(npc['zhong']) - shang
                        if npc['zhong'] > 0:
                            print('%s损失%d兵力' %(da, shang)) 
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0             #下一次行动时，将不会选择敌军中军作为攻击目标
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if npc['qian'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                elif int(zhong_shuxing['ju']) == 3:  
                    da = random.choice(mubiao2)     #前面已经设置，当前锋死时，将大营加入攻击列表
                    print('%s对%s发起进攻' %(zhong_shuxing['jiang'], da))
                    shang = int(zhong_shuxing['ji']) + 0.1*int(zhong_shuxing['bing']) 
                    if da == npc['zhongjun']:   
                        npc['zhong'] = int(npc['zhong']) - shang
                        if npc['zhong'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0           
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if npc['qian'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                    elif da == npc['daying']:
                        npc['ying'] = int(npc['ying']) - shang
                        if npc['ying'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利！' %da)
                            npc['ying'] = 0
                            return
                elif int(zhong_shuxing['ju']) == 2 and npc['qian'] != 0:
                    da = npc['qianfeng']
                    print('%s对%s发起进攻' %(zhong_shuxing['jiang'], da))
                    shang = int(zhong_shuxing['ji']) + 0.1*int(zhong_shuxing['bing']) 
                    npc['qian'] = int(npc['qian']) - shang
                    if npc['qian'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['qian'] = 0
                elif int(zhong_shuxing['ju']) == 2 and npc['qian'] == 0 and npc['zhong'] != 0:
                    da = npc['zhongjun']
                    print('%s对%s发起进攻' %(zhong_shuxing['jiang'], da))
                    shang = int(zhong_shuxing['ji']) + 0.1*int(zhong_shuxing['bing']) 
                    npc['zhong'] = int(npc['qian']) - shang
                    if npc['zhong'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['zhong'] = 0
                elif int(zhong_shuxing['ju']) == 2 and npc['qian'] == 0 and npc['zhong'] == 0:
                    da = npc['daying']
                    print('%s对%s发起进攻' %(zhong_shuxing['jiang'], da))
                    shang = int(zhong_shuxing['ji']) + 0.1*int(zhong_shuxing['bing']) 
                    npc['ying'] = int(npc['ying']) - shang
                    if npc['ying'] > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军大营%s阵亡，挑战胜利' %da)
                        npc['ying'] = 0
                        return
                else:
                    print('攻击距离不足，%s无法行动' %zhong_shuxing['jiang'])
            elif xian == int(qian_shuxing['su']) and int(qian_shuxing['bing']) > 0:
                print('%s开始行动' %qian_shuxing['jiang'])
                if int(qian_shuxing['ju']) >= 3:                         
                    da = random.choice(mubiao1)
                    print('%s对%s发起进攻' %(qian_shuxing['jiang'], da))
                    shang = int(qian_shuxing['ji']) + 0.1*int(qian_shuxing['bing']) 
                    if da == npc['daying']:                            
                        npc['ying'] = int(npc['ying']) - shang
                        if int(npc['ying']) > 0:                           
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利' %da)
                            npc['ying'] = 0
                            return
                    elif da == npc['zhongjun']:     
                        npc['zhong'] = int(npc['zhong']) - shang
                        if npc['zhong'] > 0:
                            print('%s损失%d兵力' %(da, shang)) 
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0             #下一次行动时，将不会选择敌军中军作为攻击目标
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if int(npc['qian']) > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                elif int(qian_shuxing['ju']) == 2:  
                    da = random.choice(mubiao2)     #前面已经设置，当前锋死时，将大营加入攻击列表
                    print('%s对%s发起进攻' %(qian_shuxing['jiang'], da))
                    shang = int(qian_shuxing['ji']) + 0.1*int(qian_shuxing['bing']) 
                    if da == npc['zhongjun']:   
                        npc['zhong'] = int(npc['zhong']) - shang
                        if int(npc['zhong']) > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军%s阵亡' %da)
                            npc['zhong'] = 0           
                    elif da == npc['qianfeng']:
                        npc['qian'] = int(npc['qian']) - shang
                        if npc['qian'] > 0:
                            print('%s损失%d兵力' %(da, shang))
                        elif npc['qian'] <= 0:
                            print('敌军%s阵亡' %da)
                            npc['qian'] = 0
                    elif da == npc['daying']:
                        npc['ying'] = int(npc['ying']) - shang
                        if int(npc['ying']) > 0:
                            print('%s损失%d兵力' %(da, shang))
                        else:
                            print('敌军大营%s阵亡，挑战胜利！' %da)
                            npc['ying'] = 0
                            return
                elif int(qian_shuxing['ju']) == 1 and npc['qian'] != 0:
                    da = npc['qianfeng']
                    print('%s对%s发起进攻' %(qian_shuxing['jiang'], da))
                    shang = int(qian_shuxing['ji']) + 0.1*int(qian_shuxing['bing']) 
                    npc['qian'] = int(npc['qian']) - shang
                    if int(npc['qian']) > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['qian'] = 0
                elif int(qian_shuxing['ju']) == 1 and npc['qian'] == 0 and npc['zhong'] != 0:
                    da = npc['zhongjun']
                    print('%s对%s发起进攻' %(qian_shuxing['jiang'], da))
                    shang = int(qian_shuxing['ji']) + 0.1*int(qian_shuxing['bing']) 
                    npc['zhong'] = int(npc['qian']) - shang
                    if int(npc['zhong']) > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军%s阵亡' %da)
                        npc['zhong'] = 0
                elif int(qian_shuxing['ju']) == 1 and npc['qian'] == 0 and npc['zhong'] == 0:
                    da = npc['daying']
                    print('%s对%s发起进攻' %(qian_shuxing['jiang'], da))
                    shang = int(qian_shuxing['ji']) + 0.1*int(qian_shuxing['bing']) 
                    npc['ying'] = int(npc['ying']) - shang
                    if int(npc['ying']) > 0:
                        print('%s损失%d兵力' %(da, shang))
                    else:
                        print('敌军大营%s阵亡，挑战胜利' %da)
                        npc['ying'] = 0
                        return
                else:
                    print('攻击距离不足，%s无法行动' %qian_shuxing['jiang'])
            elif xian == npc['sujia'] and npc['ying'] > 0:
                print('%s开始行动' %npc['daying']) 
                da = random.choice(mubiao3)
                if da == ying_shuxing['jiang']:
                    shang = (500 - int(ying_shuxing['yu'])) + int(npc['ying'])*0.07 
                    print('%s对%s发起进攻' %(npc['daying'], ying_shuxing['jiang']))
                    ying_shuxing['bing'] = int(ying_shuxing['bing']) - shang                           
                    if int(ying_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(ying_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        ying_shuxing['bing'] = 100
                        print('我军大营%s阵亡，挑战失败' %ying_shuxing['jiang'])
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        ying_shuxing['bing'] = 0
                        return
                elif da == zhong_shuxing['jiang']:
                    shang = (500 - int(zhong_shuxing['yu'])) + int(npc['ying'])*0.07 
                    print('%s对%s发起进攻' %(npc['daying'], zhong_shuxing['jiang']))
                    zhong_shuxing['bing'] = int(zhong_shuxing['bing']) - shang                           
                    if int(zhong_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(zhong_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        zhong_shuxing['bing'] = 100
                        print('我军%s阵亡' %zhong_shuxing['jiang'])
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        zhong_shuxing['bing'] = 0
                        
                elif da == qian_shuxing['jiang']:
                    shang = (500 - int(qian_shuxing['yu'])) + int(npc['ying'])*0.07 
                    print('%s对%s发起进攻' %(npc['daying'], qian_shuxing['jiang']))
                    qian_shuxing['bing'] = int(qian_shuxing['bing']) - shang                           
                    if int(qian_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(qian_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        qian_shuxing['bing'] = 100
                        print('我军%s阵亡' %qian_shuxing['jiang'])
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        qian_shuxing['bing'] = 0
            elif xian == npc['suyi'] and npc['zhong'] > 0:
                print('%s开始行动' %npc['zhongjun']) 
                da = random.choice(mubiao3)
                if da == ying_shuxing['jiang']:
                    shang = (500 - int(ying_shuxing['yu'])) + int(npc['zhong'])*0.07 
                    print('%s对%s发起进攻' %(npc['zhongjun'], ying_shuxing['jiang']))
                    ying_shuxing['bing'] = int(ying_shuxing['bing']) - shang                           
                    if int(ying_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(ying_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        ying_shuxing['bing'] = 100
                        print('我军大营%s阵亡，挑战失败' %ying_shuxing['jiang'])
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        ying_shuxing['bing'] = 0
                    shang = (500 - int(zhong_shuxing['yu'])) + int(npc['zhong'])*0.07 
                    print('%s对%s发起进攻' %(npc['zhongjun'], zhong_shuxing['jiang']))
                    zhong_shuxing['bing'] = int(zhong_shuxing['bing']) - shang                           
                    if int(zhong_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(zhong_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        zhong_shuxing['bing'] = 100
                        print('我军%s阵亡' %zhong_shuxing['jiang'])
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        zhong_shuxing['bing'] = 0
                        
                elif da == qian_shuxing['jiang']:
                    shang = (500 - int(qian_shuxing['yu'])) + int(npc['zhong'])*0.07 
                    print('%s对%s发起进攻' %(npc['zhongjun'], qian_shuxing['jiang']))
                    qian_shuxing['bing'] = int(qian_shuxing['bing']) - shang                           
                    if int(qian_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(qian_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        qian_shuxing['bing'] = 100
                        print('我军%s阵亡' %qian_shuxing['jiang'])
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        qian_shuxing['bing'] = 0
            elif xian == npc['subing'] and npc['qian'] > 0:
                print('%s开始行动' %npc['qianfeng']) 
                da = random.choice(mubiao3)
                if da == ying_shuxing['jiang']:
                    shang = (500 - int(ying_shuxing['yu'])) + int(npc['qian'])*0.07 
                    print('%s对%s发起进攻' %(npc['qianfeng'], ying_shuxing['jiang']))
                    ying_shuxing['bing'] = int(ying_shuxing['bing']) - shang                           
                    if int(ying_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(ying_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        ying_shuxing['bing'] = 100
                        print('我军大营%s阵亡，挑战失败' %ying_shuxing['jiang'])
                        sql = 'update %s_budui set 大营兵力=%d where id = %d' %(user,ying_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        ying_shuxing['bing'] = 0
                        return
                elif da == zhong_shuxing['jiang']:
                    shang = (500 - int(zhong_shuxing['yu'])) + int(npc['qian'])*0.07 
                    print('%s对%s发起进攻' %(npc['qianfeng'], zhong_shuxing['jiang']))
                    zhong_shuxing['bing'] = int(zhong_shuxing['bing']) - shang                           
                    if int(zhong_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(zhong_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        zhong_shuxing['bing'] = 100
                        print('我军%s阵亡' %zhong_shuxing['jiang'])
                        sql = 'update %s_budui set 中军兵力=%d where id = %d' %(user,zhong_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        zhong_shuxing['bing'] = 0
                        
                elif da == qian_shuxing['jiang']:
                    shang = (500 - int(qian_shuxing['yu'])) + int(npc['qian'])*0.07 
                    print('%s对%s发起进攻' %(npc['qianfeng'], qian_shuxing['jiang']))
                    qian_shuxing['bing'] = int(qian_shuxing['bing']) - shang                           
                    if int(qian_shuxing['bing']) > 0:
                        print('%s损失%d兵力' %(qian_shuxing['jiang'], shang))
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                    else:
                        qian_shuxing['bing'] = 100
                        print('我军%s阵亡' %qian_shuxing['jiang'])
                        sql = 'update %s_budui set 前锋兵力=%d where id = %d' %(user,qian_shuxing['bing'], bdlist[6])
                        cur.execute(sql)
                        conn.commit()
                        qian_shuxing['bing'] = 0
        print('前锋--%s剩余兵力：%d' %(qian_shuxing['jiang'],int(qian_shuxing['bing'])))        
        print('中军--%s剩余兵力：%d' %(zhong_shuxing['jiang'],int(zhong_shuxing['bing'])))        
        print('大营--%s剩余兵力：%d' %(ying_shuxing['jiang'],int(ying_shuxing['bing'])))        
        print('前锋--%s剩余兵力：%d' %(npc['qianfeng'],int(npc['qian'])))        
        print('中军--%s剩余兵力：%d' %(npc['zhongjun'],int(npc['zhong'])))        
        print('大营--%s剩余兵力：%d' %(npc['daying'],int(npc['ying'])))        
    cur.close()
    conn.close()
    if int(npc['ying']) != 0:
        return 233
        

                

def zhandou(user, npc, zhan):
    conn = pymysql.connect('127.0.0.1', 'root', '123', '%s' %user)
    cur = conn.cursor()
    sql = 'select * from %s_budui' %user
    count = cur.execute(sql)
    bdlist = cur.fetchall()
    sql = 'select * from %s_wjlist' %user
    cc = cur.execute(sql)
    wjlist = cur.fetchall()
    cur.close()
    conn.close()
    count = int(count)
    bd = []
    for i in range(count):
        qian = bdlist[i][0]
        zhong = bdlist[i][1]
        ying = bdlist[i][2]
        qian_bing = bdlist[i][3]
        zhong_bing = bdlist[i][4]
        ying_bing = bdlist[i][5]
        i = {'前锋':'%s' %qian, '中军':'%s' %zhong, '大营':'%s' %ying, '前锋兵力':'%s' %qian_bing, '中军兵力':'%s' %zhong_bing, '大营兵力':'%s' %ying_bing}
        bd.append(i)
    time.sleep(0.5)
    os.system('clear')
    print('&'*50)
    print('我的部队：')
    budui(user)
    print('')
    print('&'*50)
    print('敌军部队：')
    npc = NPC(npc, zhan)
    select = input('请选择战斗部队：')
    if select == '1' and count >= 1:
        bd_1 = bd[0]
        print(bd_1)
        qian_shuxing = {}
        qian_shuxing.setdefault('bing','%s' %bd_1['前锋兵力'])
        zhong_shuxing = {}
        zhong_shuxing.setdefault('bing','%s' %bd_1['中军兵力'])
        ying_shuxing = {}
        ying_shuxing.setdefault('bing','%s' %bd_1['大营兵力'])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['前锋']:
                qian_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                qian_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                qian_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                qian_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                qian_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['中军']:
                zhong_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                zhong_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                zhong_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                zhong_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                zhong_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['大营']:
                ying_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                ying_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                ying_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                ying_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                ying_shuxing.setdefault('su','%s' %wjlist[wj][4])
        bdlist = bdlist[0]
        dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist)
    elif select == '2' and count >= 2:
        bd_1 = bd[1]
        print(bd_1)
        qian_shuxing = {}
        qian_shuxing.setdefault('bing','%s' %bd_1['前锋兵力'])
        zhong_shuxing = {}
        zhong_shuxing.setdefault('bing','%s' %bd_1['中军兵力'])
        ying_shuxing = {}
        ying_shuxing.setdefault('bing','%s' %bd_1['大营兵力'])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['前锋']:
                qian_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                qian_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                qian_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                qian_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                qian_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['中军']:
                zhong_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                zhong_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                zhong_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                zhong_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                zhong_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['大营']:
                ying_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                ying_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                ying_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                ying_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                ying_shuxing.setdefault('su','%s' %wjlist[wj][4])
        bdlist = bdlist[0]
        dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist)

    elif select == '3' and count >= 3:
        bd_1 = bd[2]
        print(bd_1)
        qian_shuxing = {}
        qian_shuxing.setdefault('bing','%s' %bd_1['前锋兵力'])
        zhong_shuxing = {}
        zhong_shuxing.setdefault('bing','%s' %bd_1['中军兵力'])
        ying_shuxing = {}
        ying_shuxing.setdefault('bing','%s' %bd_1['大营兵力'])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['前锋']:
                qian_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                qian_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                qian_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                qian_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                qian_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['中军']:
                zhong_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                zhong_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                zhong_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                zhong_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                zhong_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['大营']:
                ying_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                ying_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                ying_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                ying_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                ying_shuxing.setdefault('su','%s' %wjlist[wj][4])
        bdlist = bdlist[0]
        dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist)

    elif select == '4' and count >= 4:
        bd_1 = bd[3]
        print(bd_1)
        qian_shuxing = {}
        qian_shuxing.setdefault('bing','%s' %bd_1['前锋兵力'])
        zhong_shuxing = {}
        zhong_shuxing.setdefault('bing','%s' %bd_1['中军兵力'])
        ying_shuxing = {}
        ying_shuxing.setdefault('bing','%s' %bd_1['大营兵力'])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['前锋']:
                qian_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                qian_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                qian_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                qian_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                qian_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['中军']:
                zhong_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                zhong_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                zhong_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                zhong_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                zhong_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['大营']:
                ying_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                ying_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                ying_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                ying_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                ying_shuxing.setdefault('su','%s' %wjlist[wj][4])
        bdlist = bdlist[0]
        dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist)

    elif select == '5' and count >= 5:
        bd_1 = bd[4]
        print(bd_1)
        qian_shuxing = {}
        qian_shuxing.setdefault('bing','%s' %bd_1['前锋兵力'])
        zhong_shuxing = {}
        zhong_shuxing.setdefault('bing','%s' %bd_1['中军兵力'])
        ying_shuxing = {}
        ying_shuxing.setdefault('bing','%s' %bd_1['大营兵力'])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['前锋']:
                qian_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                qian_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                qian_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                qian_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                qian_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['中军']:
                zhong_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                zhong_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                zhong_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                zhong_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                zhong_shuxing.setdefault('su','%s' %wjlist[wj][4])
        for wj in range(cc):
            if wjlist[wj][0] == bd_1['大营']:
                ying_shuxing.setdefault('jiang','%s' %wjlist[wj][0])
                ying_shuxing.setdefault('ju','%s' %wjlist[wj][1])
                ying_shuxing.setdefault('ji','%s' %wjlist[wj][2])
                ying_shuxing.setdefault('yu','%s' %wjlist[wj][3])
                ying_shuxing.setdefault('su','%s' %wjlist[wj][4])
        bdlist = bdlist[0]
        dou(npc, qian_shuxing, zhong_shuxing, ying_shuxing, user,bdlist)
        
    else:
        print('部队未开放。')


def zhengfa(zhu):
    user = zhu[0]
    menu='''
1：荆州
2：益州
3：扬州
4：青州
5：徐州
6：冀州
7：并州
8：凉州
9：幽州
请选择出征目的：'''
    se = input(menu)
    if se == '1':
        os.system('clear')
        time.sleep(0.3)
        ti = '荆州蛮夷之地，南船北马，七省通达。蛮人多种，性不能教，联合党朋，失意则相攻，贪而勇战。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '2':
        os.system('clear')
        time.sleep(0.3)
        ti = '西南隅所，地险山俊，道成天堑，一夫当关，万夫莫开。偶有南蛮、芥廯。沃野千里，风调雨顺。锦官城外，蓉花胜海。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '3':
        os.system('clear')
        time.sleep(0.3)
        ti = '吴越兵烽归一，跨大江，涵太湖，水道如织，雨沛粮足。虽多矮山，但易安居，山越南傍，沿于海而达至淮泗。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '4':
        os.system('clear')
        time.sleep(0.3)
        ti = '禹王岁止，阔土东夷。泰山嫠北，齐侯故地。五行属木而色青，海岱唯青州。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '5':
        os.system('clear')
        time.sleep(0.3)
        ti = '济右之地，淮、沂其乂，蒙、羽其艺。赤土成壤，羽畎夏翟，临珠暨渔，是为徐。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '6':
        os.system('clear')
        time.sleep(0.3)
        ti = '夏之子，东临瀛海，南临河济，川原绕衍，控带燕齐。土平兵强，英杰所利，为南北要冲，戎马之场。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '7':
        os.system('clear')
        time.sleep(0.3)
        ti = '中原之北，南北纵列山峦，天燥少雨，凛冬时久，致生计不易，地广人稀，又处于两谷之间，曰并。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '8':
        os.system('clear')
        time.sleep(0.3)
        ti = '汉武骠骑西驰，通一线于广漠，秦川中，黄沙背，胡汉相接，军商混杂，朔风起，胡马踏。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)
    elif se == '9':
        os.system('clear')
        time.sleep(0.3)
        ti = '极北治所，舟橹循水而至。丽鲜之民，闻汉风居。散关夏，通贾如织而岁末不止。'
        for i in ti:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        print('*'*110)
        for i in range(5):
            print('第%d轮探索中...' %(i+1))
            yu = ['山贼', '流寇', '悍匪']
            zhan = random.choice(yu)
            time.sleep(0.5)
            zei = {'daying':'山贼甲', 'zhongjun':'山贼乙', 'qianfeng':'山贼丙', 'ying':5000, 'zhong':5000, 'qian':5000, 'sujia':79, 'suyi':89, 'subing':99}
            kou = {'daying':'流寇甲', 'zhongjun':'流寇乙', 'qianfeng':'流寇丙', 'ying':7000, 'zhong':7000, 'qian':7000, 'sujia':79, 'suyi':89, 'subing':99}
            fei = {'daying':'悍匪甲', 'zhongjun':'悍匪乙', 'qianfeng':'悍匪丙', 'ying':9000, 'zhong':9000, 'qian':9000, 'sujia':79, 'suyi':89, 'subing':99}
            npc = [zei, fei, kou]
            select = input('碰上新敌军：%s。是否战斗？' %zhan)
            if select == 'y':
                zhandou(user, npc, zhan)


def main():
    zhu = login()
    if 200 in zhu:
        while True:
            xuan = input(menu1)
            if xuan == '1':
                wujiang(zhu)
            elif xuan == '2':
                jianshe(zhu)
            elif xuan == '3':
                neizheng(zhu)
            elif xuan == '4':
                dianjiangtai(zhu)
            elif xuan == '5':
                zhengfa(zhu)
            elif xuan == '6':
                return
            else:
                print('请输入正确选项。')
    
if __name__ == '__main__':
    main()
