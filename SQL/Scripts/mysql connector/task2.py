# -*- coding: utf-8 -*-

import mysql.connector as sql 
import pandas as pd
import csv
from IPython.display import display
from task1 import read_csv, write_csv, normal_csv


class DAL:
    
    def __init__(self, db: str, psw):
        self.cur_con = sql.connect(user='root', password=psw, database=db)
        
    def close_con(self):
        if self.cur_con.is_connected():
            self.cur_con.close()
            
    def create_table(self, tablename:str,cols:list, reset=True):
        try:
            if reset:
                self.cur_con.reset_session()
                
            cursor = self.cur_con.cursor()
              
            query = f''' 
            CREATE TABLE {tablename}
                ( '''
                 
            for col in cols: 
                query = query + str(col)
                
            query = query + ');'
            print(query)
            cursor.execute(query)
            print('Table',tablename,'was created')
            
        except Exception as e:
            print(e)
        
            
    def get_table_list(self, query_text:str, reset=True):

        try:
            cur_con = self.cur_con
            if reset:
                cur_con.reset_session()
                
            cursor = cur_con.cursor()
            query = query_text
                
            cursor.execute(query)
            res = cursor.fetchall() 
            cols = cursor.column_names
        
        except Exception as e:
            print(e)
        return (res, cols)
    
    
    def get_table_dataframe(self, query_text: str, reset=True):
        if reset:
            self.cur_con.reset_session()
            
        cursor = self.cur_con.cursor()
        res = pd.read_sql(query_text,self.cur_con)
        return res
    
            
    def insert_data(self, insert_query:str,vals = [], reset=True):
        try:
            if reset:
                self.cur_con.reset_session()
              
            cursor = self.cur_con.cursor()
            if vals == []:
                cursor.execute(insert_query)
            else:
                cursor.executemany(insert_query, vals)
            self.cur_con.commit()

            print(cursor.rowcount, " rows inserted.")
            
        except Exception as e:
            print(e)
            
            
    def delete_data(self, del_query:str, reset=True):
        try:
            if reset:
                self.cur_con.reset_session()
              
            cursor = self.cur_con.cursor()
            cursor.execute(del_query)
            self.cur_con.commit()

            print(cursor.rowcount, " record(s) deleted.")
            
        except Exception as e:
            print(e)
      
            
    def update_data(self, upd_query:str, reset=True):
        try:
            if reset:
                self.cur_con.reset_session()
              
            cursor = self.cur_con.cursor()
            cursor.execute(upd_query)
            self.cur_con.commit()

            print(cursor.rowcount, " record(s) affected.")
            
        except Exception as e:
            print(e)
            
    
    def delete_save_csv(self, del_query:str,fname = 'mytable.csv', reset=True):
        try:
            cur_con = self.cur_con
            if reset:
                self.cur_con.reset_session()
            
            del_query = del_query.lower()
            query = del_query.replace('delete','select *')
            
            write_csv(query, fname)
            
            # удаление данных из таблицы
            cursor = self.cur_con.cursor()
            cursor.execute(del_query)
            self.cur_con.commit()

            print(cursor.rowcount, " record(s) deleted.")     
            
            # восстановление данных
            ans = int(input('Press 1 if you want to recover data or 0 if not: '))
            
            if ans == 1:
                tablename = del_query.split(' ')[2]
                new_records = read_csv(fname) # list
                vals_count = '('+'%s,'*(len(new_records[0])-1)+'%s);'
                
                insert_query = f'insert into {tablename} values ' + vals_count
                self.insert_data(insert_query, new_records)
                print('Data recovered')
                
        except Exception as e:
            print(e)
    
            
    def csv_changed(self,tablename:str, fname = 'edited.csv'):
        
        query1 = 'select * from ' + tablename
        table_db1 = self.get_table_list(query1)
        col_names = table_db1[1]
        table_db = list(table_db1[0]) 
        table_csv = normal_csv(fname)
        changed_vals, del_records = [], [] 
        
        
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
            
            self.delete_data(del_query)
                
        # вставка новых строк
        elif len(table_db) < len(table_csv):
            print('\nSome records were added to file',fname)
            
            # данные добавлятся в конец
            new_records = table_csv[len(table_db):]
            #print(new_records)
            vals_count = '('+'%s,'*(len(new_records[0])-1)+'%s);'
            
            insert_query = f'insert ignore into {tablename} values ' + vals_count
            self.insert_data(insert_query, new_records)
            
            
        elif len(table_db) == len(table_csv):
            print('\nSome records were updated in file',fname)
            for i in range(len(table_csv)):
                
                # привести таблицу из бд к нормальному виду
                table_db[i] = list(table_db[i])
                
                # если строка была изменена
                if table_db[i] != table_csv[i]:
                    ind = table_db[i][0] # айдишник
                    # print('row ', i, 'was changed')
                    
                    # итерация по данным в строке
                    for j in range(len(table_csv[i])):
                        if str(table_db[i][j]) != table_csv[i][j]:
                            
                            colname = col_names[j]
                            val = str(table_csv[i][j])
                            if val != '':
                                changed_vals.append((colname,val, ind))
                              
            # обновление таблицы в бд
            for vals in changed_vals:
                colname, val, i = vals[0], vals[1], vals[2]
                upd_query = f'update {tablename} set {colname} = "{val}" where {col_names[0]} = {i}; '
                # print(upd_query)
                self.update_data(upd_query)
                