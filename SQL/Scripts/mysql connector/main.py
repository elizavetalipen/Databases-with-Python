# -*- coding: utf-8 -*-

from task2 import *
from task1 import read_csv, write_csv, normal_csv


menu = '''
0. Exit
1. Read data from table
2. Update
3. Insert 
4. Delete
5. Create new table
6. Write table to csv-file
7. CSV synchronization
8. Change database'''

menu1 = '''
0. Exit
1. Get records as list
2. Get records as dataframe
3. Read from csv-file
'''


def main():
    
    try: 
        psw = input('Password: ')
        db_name = input('Database: ')
        layer = DAL(db_name, psw)
        
        while True:
            print(menu)
            ans = int(input('Choose action: '))
            
            if ans == 0:
                break
            
            # чтение данных
            elif ans == 1:
                print(menu1)
                ans1 = int(input('Choose action: '))
                
                if ans1 == 0:
                    break
                
                elif ans1 == 1:
                    
                    query = input('Enter select-query: ')
                    data_list = layer.get_table_list(query)
                    for data in data_list[0]:
                        for i in range(len(data)):
                            print(data_list[1][i],':',data[i])
                        print('\n')
                        
                elif ans1 == 2:
                    
                    query = input('Enter select-query: ')
                    data_pd = layer.get_table_dataframe(query)
                    print(data_pd)
                    
                elif ans1 == 3:
                    fname = input('File name: ')
                    data = read_csv(fname)
                    for record in data:
                        print(record)
           
            # обновление данных
            elif ans == 2:
                query = input('Enter update-query: ')
                layer.update_data(query)
    
             # вставить записи
            elif ans == 3:
                # пример запроса: insert into table values (val1, val2)
                 query = input('Enter insert-query: ')
                 layer.insert_data(query)   
            
            # удаление записей
            elif ans == 4:
                query = input('Enter delete-query: ')
                layer.delete_save_csv(query)
            
            # создание новой таблицы
            elif ans == 5:
                tablename = input('Enter table name: ')
                n = int(input('How many columns: '))
                cols = []
                for i in range(n):
                    col = input('Enter column name and datatype with , : ')
                    cols.append(col)
                    
                layer.create_table(tablename,cols)
            
            # запись данных в файл
            elif ans == 6:
                query = input('Enter select-query: ')
                fname = input('Enter file name: ')
                
                write_csv(query, fname)
            
            # синхронизация с файлом
            elif ans == 7:
                fname = input('Enter file name: ')
                tablename = input('Related table name: ')
                layer.csv_changed(tablename,fname)
                
            # переключаемся на другую бд
            elif ans == 8:
                db_name = input('Enter database name: ')
                layer = DAL(db_name)
            
            else:
                print('Input error')
                break
            
    except Exception as e:
            print(e)
        
        
if __name__ == '__main__':
    main()