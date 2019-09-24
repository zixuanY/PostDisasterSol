import sqlite3
import pandas
import csv
import os

DBNAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'main.db'
)

# -*- coding: UTF-8 -*-
def insert_relative(id_,name,age,gender,height,weight,location,contact,health_cond,photo):
    con = sqlite3.connect(DBNAME)
    c=con.cursor()
    id_ = "'"+id_+"'"
    name = "'"+name+"'"
    gender = "'"+gender+"'"
    location = "'"+location+"'"
    contact = "'"+contact+"'"
    health_cond = "'"+health_cond+"'"
    photo = "'"+photo+"'"
    query = '''INSERT INTO relative_side_info(ID, NAME, AGE, GENDER, HEIGHT, WEIGHT, LOCATION, CONTACT, HEALTH_COND, PHOTO) VALUES ('''+id_+''', '''+name+''', '''+str(age)+''', '''+gender+''', '''+str(height)+''', '''+str(weight)+''', '''+location+''', '''+contact+''', '''+health_cond+''', '''+photo+''');'''
    c.execute(query)
    con.commit()
    con.close()

def insert_rescue(id_,name,age, gender, height, location, contact,condition,photo):
    con = sqlite3.connect(DBNAME)
    c=con.cursor()
    id_ = "'"+id_+"'"
    name = "'"+name+"'"
    gender = "'"+gender+"'"
    location = "'"+location+"'"
    contact = "'"+contact+"'"
    condition = "'"+condition+"'"
    photo = "'"+photo+"'"
    query = '''INSERT INTO rescue_side_info(ID, NAME, AGE, GENDER, HEIGHT, LOCATION, CONTACT, CONDITION, PHOTO) VALUES ('''+id_+''', '''+name+''', '''+str(age)+''', '''+gender+''', '''+str(height)+''', '''+location+''', '''+contact+''', '''+condition+''', '''+photo+''');'''
    #print(query)
    c.execute(query)
    con.commit()
    con.close()

def insert_coordinate(filename):
    conn= sqlite3.connect(DBNAME)
    df = pandas.read_csv('/home/linux-zixuan/Desktop/hackthon/coordinate.csv')
    df.to_sql('coordinate_info', conn, if_exists='append', index=False)
    print('ok')

if __name__=='__main__':
    # insert_coordinate("coordinate.csv")
    insert_relative("31010519991003224", "XiaoMing", 20, "male", 175, 70, "成都市", "131888888888", "None", "")
    insert_relative("310105199909032244", "XiaoHua", 20, "female", 171, 60, "绵阳市", "1318888889999", "Heart Disease", "")
    insert_relative("310105198809032254", "XiaoLi", 31, "female", 165, 50, "宜宾市", "1318888879999", "None", "")
    insert_relative("310105196809032254", "LaoWang", 51, "male", 178, 70, "成都市", "1318588879999", "None", "")
    insert_relative("310105196809032254", "LaoWang", 51, "male", 178, 70, "绵阳市", "1318588879999", "None", "")

    insert_rescue('310105196809032254',"LaoWang",50,"male",180,"成都市","","Seriously Hurt","")
    insert_rescue('',"",20,"male",175,"","","Not Hurt","")#XiaoMing
    insert_rescue('',"",20,"female",170,"绵阳市","","Not Hurt","")
    insert_rescue('',"",30,"female",165,"重庆市","","Not Hurt","")

