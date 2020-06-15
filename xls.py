#!/usr/bin/env python
import pymysql
import xlwt
import getpass
import os

account = input("用户：")
passwd = getpass.getpass("密码：")
os.system('mysql -u{} -p{} -e "show databases" > ./db.txt'.format(account,passwd))
with open('./db.txt', 'r+') as fo:
    data = fo.readlines()
li = []
for i in data:
    li.append(i.split("\n")[0])
dic = {}
for i in range(len(li)):
    dic.setdefault('{}'.format(i+1),li[i])

def table(ke):
    os.system('mysql -u{} -p{} {} -e "show tables" > ./table.txt'.format(account,passwd,ke))
    with open('./table.txt','r+') as fo:
        data = fo.readlines()
    lis = []
    for i in data:
        lis.append(i.split("\n")[0])
    di = {}
    for i in range(len(lis)):
        di.setdefault('{}'.format(i+1),lis[i])
    txt = '表格'
    print(txt.center(20,"*"))
    for i in range(len(lis)):
        print('{}'.format(i+1), di['{}'.format(i+1)])
    print(txt.center(20,"*"))
    select = input('请选择表格：')
    for key in di:
        if select == key:
            k = di['{}'.format(key)]
            conn = pymysql.connect('127.0.0.1','{}'.format(account),'{}'.format(passwd),'{}'.format(ke))
            cur = conn.cursor()
            sql = 'select * from {}'.format(k)
            count = cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            conn.close()
            for i in data:
                print(i)
            sele = input("生成xlwt文件【y|n】：")
            if sele == 'y':
                fileds = cur.description
                workbook = xlwt.Workbook(encoding='UTF-8')
                worksheet = workbook.add_sheet('test')
                for item in range(len(fileds)):
                    worksheet.write(0, item, fileds[item][0])
                for row_number in range(1, count):
                    for col_number in range(0, len(fileds)):
                        worksheet.write(row_number, col_number, data[row_number-1][col_number])
                workbook.save('{}.xls'.format(k))
                print("已生成{}的xlwt文件".format(k))
    
while True:
    txt = '数据库'
    print(txt.center(20,"*"))
    for i in range(len(li)):
        print('{}'.format(i+1), dic['{}'.format(i+1)])
    print(txt.center(20,"*"))
    select = input('请选择数据库：')
    for key in dic:
        if select == key:
            ke = dic['{}'.format(key)]
            table(ke)
        elif select == 'q':
            exit()
