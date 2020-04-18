#!/usr/bin/env python3
import pymysql
import os

def peizhi():
    os.system("mysql -uroot -e set password=password('123')")
    os.system("mysql -uroot -p123 -e 'create database account_data'")
    os.system("mysql -uroot -p123 account_data -e 'create table account(user char(20) not null, passwd char(20) not null)'")
    os.system("mysql -uroot -p123 account_data -e 'create table wujiang (武将 char(10) unique, 攻距 int(10), 攻击 int(10), 防御 int(10), 速度 int(10))'")
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('关羽',3,254,158,181)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('张辽',3,221,227,272)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('马超',3,278,184,154)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('张绣',1,213,172,142)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('马岱',3,203,177,141)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('曹操',2,128,295,126)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('荀彧',2,225,156,249)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('法正',2,218,136,146)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('马云禄',3,156,114,142)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('吕蒙',4,166,223,87)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('周瑜',4,230,134,93)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('陆逊',2,209,209,46)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('孙策',2,225,175,144)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('陆抗',2,205,177,56)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('曹丕',4,145,142,79)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('典韦',2,197,243,51)"''')
    os.system('''mysql -uroot -p123 account_data -e "insert into wujiang values('诸葛亮',2,286,167,35)"''')

def main():
    peizhi()

if __name__ == '__main__':
    main()

