# -*- coding: utf-8 -*-

import mysql.connector as sql 
import pandas as pd
import csv
from IPython.display import display

# task 1. Реализуйте методы для получения данных

def get_connection(username='root', db='antarctica', psw="1234"):
    try:
        cnx = sql.connect(user=username, password=psw, database=db)
        return cnx
    except Exception as e:
        print(e)


def get_table_list(connection: sql.MySQLConnection, 
                   query_text:str,reset=True):
    ''' Get table records as list'''

    try:
        cur_con = connection
        if reset:
            cur_con.reset_session()
            
        cursor = cur_con.cursor()
        query = query_text
            
        cursor.execute(query)
        res = cursor.fetchall() 
        cols = cursor.column_names
            
        cursor.close()
        cur_con.close()
        return (res, cols)
    
    except Exception as e:
        print(e)
  
             
def get_table_dataframe(connection: sql.MySQLConnection, query_text: str, reset=True):
    cur_con = connection
    if reset:
        cur_con.reset_session()
        
    cursor = cur_con.cursor()
    res = pd.read_sql(query_text,cur_con)
    cursor.close()
    cur_con.close()
    return res


def write_csv(query_text:str, fname = 'test.csv'):
    ''' Save query result as csv-file'''
    try:
        cur_con = get_connection()
        cur_con.reset_session()
        data = get_table_list(cur_con, query_text)[0]
        
        with open(fname, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for tup in data:
                writer.writerow(tup)
                
        print('\nCSV file is written')
     
    except Exception as e:
        print(e)

        
def read_csv(fname='edited.csv')->list:
    ''' Get records from csv file as list'''
    res = []
    with open(fname, newline='') as csvfile:
        reader = csv.reader(csvfile)
        
        for data in reader:
            res.append(data)
            
    return res

# task 1.2
#  Реализовать методы для обновления, удаления и вставки данных.

def insert_data(connection: sql.MySQLConnection, insert_query:str,vals:list, reset=True):
    
    ''' An argument is a query or parameterized query + list of values'''
    
    try:
        cur_con = connection
        if reset:
            cur_con.reset_session()
          
        cursor = cur_con.cursor()
        cursor.executemany(insert_query, vals)
        cur_con.commit()

        print(cursor.rowcount, " rows inserted.")
            
        cursor.close()
        cur_con.close()
        
    except Exception as e:
        print(e)
        

def delete_data(connection: sql.MySQLConnection, del_query:str, reset=True):
    try:
        cur_con = connection
        if reset:
            cur_con.reset_session()
          
        cursor = cur_con.cursor()
        cursor.execute(del_query)
        cur_con.commit()

        print(cursor.rowcount, " record(s) deleted.")
            
        cursor.close()
        cur_con.close()
        
    except Exception as e:
        print(e)

       
def update_data(connection: sql.MySQLConnection, upd_query:str, reset=True):
    try:
        cur_con = connection
        if reset:
            cur_con.reset_session()
          
        cursor = cur_con.cursor()
        cursor.execute(upd_query)
        cur_con.commit()

        print(cursor.rowcount, " record(s) affected.")
            
        cursor.close()
        cur_con.close()
        
    except Exception as e:
        print(e)


def delete_save_csv(connection: sql.MySQLConnection, del_query:str,
                   fname = 'mytable.csv', reset=True):
    ''' Save deleted records to csv-file'''
    try:
        cur_con = connection
        if reset:
            cur_con.reset_session()
        
        del_query = del_query.lower()
        query = del_query.replace('delete','select *')
        
        write_csv(query, fname)
        cursor = cur_con.cursor()
        cursor.execute(del_query)
        cur_con.commit()

        print(cursor.rowcount, " record(s) deleted.")     
        cursor.close()
        cur_con.close()
        
        # data recovering
        ans = int(input('Press 1 if you want to recover data or 0 if not: '))
        
        if ans == 1:
            tablename = del_query.split(' ')[2]
            new_records = read_csv(fname) 
            vals_count = '('+'%s,'*(len(new_records[0])-1)+'%s);'
            
            insert_query = f'insert into {tablename} values ' + vals_count
            print(insert_query)
            insert_data(get_connection(), insert_query, new_records)
            print('Data recovered')
            
    except Exception as e:
        print(e)

# task 1.3. Реализовать синхронизацию базы данных с csv-файлом

def myFunc(l):
  return int(l[0])      

def normal_csv(fname):
    table_csv = read_csv(fname)
    # если были пустые строки, они игнорируются
    table_csv = [i for i in table_csv if i != []]
    table_csv.sort(key=myFunc) # если строки меняли местами их нужно упорядочить
    print(table_csv)
    return table_csv
         
         
def csv_changed(tablename:str, fname = 'edited.csv'):
    
    query1 = 'select * from ' + tablename
    table_db1 = get_table_list(get_connection(),query1)
    col_names = table_db1[1]
    table_db = list(table_db1[0]) 
    table_csv = normal_csv(fname)
    changed_vals, del_records = [], [] # elements are tuples (colname, value, row number)
    
    # если произошло удаление строк
    if len(table_db) > len(table_csv):
        print('\nSome records were deleted from file', fname)
        
        for i in range(len(table_db)):
            rec = list(table_db[i])
            for j in range(len(rec)):
                rec[j] = str(rec[j])
                
                if rec[j] == 'None':
                    rec[j] = ''
            if rec not in table_csv:
                del_records.append(rec)
                
        for rec in del_records:
            changed_vals.append(int(rec[0]))
                
        del_query = f'delete from {tablename} where {col_names[0]} in '
        del_query = del_query + str(tuple(changed_vals)) 
        
        delete_data(get_connection(),del_query)
            
    # вставка новых строк
    elif len(table_db) < len(table_csv):
        print('\nSome records were added to file',fname)
        
        # данные добавлятся в конец
        new_records = table_csv[len(table_db):]
        vals_count = '('+'%s,'*(len(new_records[0])-1)+'%s);'
        insert_query = f'insert ignore into {tablename} values ' + vals_count
        insert_data(get_connection(), insert_query, new_records)
        
        
    elif len(table_db) == len(table_csv):
        print('\nSome records were updated in file',fname)
        for i in range(len(table_csv)):
            # привести таблицу из бд к нормальному виду
            table_db[i] = list(table_db[i])
            # если строка была изменена
            if table_db[i] != table_csv[i]:
                ind = table_db[i][0] # id
                # итерация по данным в строке
                for j in range(len(table_csv[i])):
                    if str(table_db[i][j]) != table_csv[i][j]:
                        
                        colname = col_names[j]
                        val = str(table_csv[i][j])
                        if val != '':
                            changed_vals.append((colname,val, ind))
                            
  
    for vals in changed_vals:
        colname, val, i = vals[0], vals[1], vals[2]
        upd_query = f'update {tablename} set {colname} = "{val}" where {col_names[0]} = {i}; '
        update_data(get_connection(), upd_query)
        

# task 1.4 Реализовать транзакный метод
def transfer_salary(fromst: int, tost: int, money:int):
    ''' Transfer given sum from one account to another'''
    try:
        connection = get_connection()
        cur_con = connection
        cursor = cur_con.cursor()   
        command_str = f'select * from contracts where contr_id = {fromst} or contr_id = {tost}'
        cursor.execute(command_str) 
        row_number = cursor.rowcount
        res = cursor.fetchall() 
          
        if len(res) == 2: # проверяем что нашли нужных
            command_text = f'UPDATE contracts SET salary = salary - {money} where contr_id = {fromst}'
            cursor.execute(command_text)
            
            a=input()
            if cursor.rowcount == 1: # так проверим, что UPDATE состоялся!
                command_text = f'UPDATE contracts SET salary = salary + {money} where contr_id = {tost}'
                cursor.execute(command_text)
                
                if cursor.rowcount == 1:
                    cur_con.commit()
                    print('Successful transaction')
                else:
                    cur_con.rollback()
                    print('Roll back at step 1')
            else:
                cur_con.rollback()
                print('Roll back at step 2')
                        
    except Exception as e:
        print(e)
        
        
def change_organisation(pers_id:int, old:int, new:int):
    try:
        connection = get_connection()
        cur_con = connection
        
        cursor = cur_con.cursor() 
        command_str = f'select * from contracts where contr_id = {pers_id} and ref_org_id = {old}'
        cursor.execute(command_str) # уже стартовала транзакция
        res = cursor.fetchall() 
            
        if len(res) == 1: # проверяем что нашли такого человека из даннной организации
            command_text = f'update contracts set ref_org_id = {new} where contr_id = {pers_id}'
            cursor.execute(command_text)
            
            if cursor.rowcount == 1:
                cur_con.commit()
                print('Successful transaction.')
            else:
                cur_con.rollback()
                print('Roll back')
                
    except Exception as e:
        print(e)
        
        

def share_food(fromst:int, tost:int, amount:int):
    cur_con = get_connection()
    try:
        cursor = cur_con.cursor() 
        command_str = f'select * from worker_supplies where ref_worker_id = {fromst} and food_portions > {amount}'
        cursor.execute(command_str)
        res = cursor.fetchall() 
        
        if len(res) == 1:
            command_text = f'update worker_supplies\
                set food_portions = food_portions + {amount}\
                    where ref_worker_id = {tost}'
            cursor.execute(command_text)
            
            if cursor.rowcount == 1:
                command_text = f'update worker_supplies\
                    set food_portions = food_portions - {amount}\
                        where ref_worker_id = {fromst}'
                cursor.execute(command_text)
                
                if cursor.rowcount == 1:
                    cur_con.commit()
                    print(amount,'portions were shared')
                else:
                    cur_con.rollback()
            else:
                cur_con.rollback()
                print('Error!')
        else:
            cur_con.rollback()
            print('Error! Maybe not enough food')
            
        
        
    except Exception as e:
        print(e)
        cur_con.rollback()
    
   
def measure_imt(card_id:int, w:float, h:float):
    ''' After changing height and weight, IMT is recalculated'''
    
    imt = w / (h*h)
    connection = get_connection()
    cur_con = connection
    
    try:
        cursor = cur_con.cursor()
        query = f'update medcard set height = {h}, weight = {w}, imt = {imt} where card_id = {card_id}'
        cursor.execute(query)
        connection.commit()
        print('Medcard',card_id,'updated')
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(e)
        
        
def call_mysql_procedure(procname:str, *args):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        res = cursor.callproc(procname, args)
        print(res)
        print('Procedure',procname,'was called')

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()
        

def call_mysql_func(funcname:str, *args):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        n = len(args)
        vals_count = '%s,' *(n-1)
        query = 'select ' + funcname + '(' + vals_count + '%s);'
        cursor.execute(query,args)
        res = cursor.fetchall()
        print(res)
        
    except Exception as e:
        print(e)

    finally:
        cursor.close()
        connection.close()
