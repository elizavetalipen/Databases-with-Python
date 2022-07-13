# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import validates
from sqlalchemy import inspect, over
from sqlalchemy import event
from sqlalchemy import func
from tables_antarctica import *
from antarcticaORM import *


def test_procedures():
    try:
        a = AntarcticaORM()
        a.start_session()
        
        print('\nCheck if worker is present\n')
        print(f'Client: {a.presentQ_client("2022-02-02")}')
        print(f'Server: {a.presentQ_server("2022-02-02")}')
        
        print('\nCheck if there are free rooms in the block\n')
        print(f'Client: {a.free_roomsQ_client(2)}')
        print(f'Server: {a.free_roomsQ_server(2)}')
        
        a.server_procdure('create_worker',['Alex K','Teacher',20000,'2022-06-01',\
                       '2022-09-10',4,'1990-10-31','m',1.84,80,4.6, 99,'chol'])
        print('New worker was created\n')
    
        a.close_session()
    except Exception as e:
        print(e)
        a.rollback()
        a.close_session()

                
def queries_examples():
    a = AntarcticaORM()
    a.start_session()
    
    # пример с count
    print('\nCount objects in tables\n')
    print(f'Organisations: {a.objects_count(Organisation)}')
    print(f'Live Blocks: {a.objects_count(LiveBlock)}')
    print(f'Workers: {a.objects_count(Worker)}')
    print(f'Contracts: {a.objects_count(Contract)}')
    
    # пример с join
    print('\nInner join query example\n')
    for w, c, m in a.worker_joined(5):
        print(f'Worker | Name: {w.name}, Position: {w.position}')
        print(f'Contract | Duration: {c.duration}, Salary: {c.salary}')
        print(f'Medcard | Gender: {m.gender}, Age: {m.age}')
        print('--'*10)
        
    # пример с partition
    print('\nPartition query example\n')
    for worker, row_number in a.worker_partition():
        print( "{0}# {1}".format(row_number, worker.name, worker.department))
        
    # пример на like
    print('Workers with name starting from A')
    for w in a.worker_by_letter('A'):
        print(f'Id: {w.idd}, Name: {w.name}')
        
    a.close_session()
    

def crud_menu():
    menu = '''
    0. Exit
    1. Read table data
    2. Update table data
    3. Insert table data
    4. Delete table data
    5. Cancel changes
    6. Commit all changes '''
    
    try: 
        a = AntarcticaORM()
        a.start_session()
        while True:
            print(menu)
            ans = int(input('Choose action: '))
            
            if ans == 0:
                break
            
            # чтение данных 
            elif ans == 1:
                obj_name = input('Object: ')
                data = a.load_data(obj_name, 'lazy')
                a.print_data(data)
           
            # обновление данных 
            elif ans == 2:
                obj_name = input('Object: ')
                i = input('id = ')
                a.update_data(obj_name,i)
    
             # вставить записи 
            elif ans == 3:
                 obj_name = input('Object: ')
                 a.insert_data(obj_name)
            
            # удаление записей 
            elif ans == 4:
                obj_name = input('Object: ')
                n = int(input('How many rows to delete: '))
                ids = []
                for i in range(n):
                    idd = int(input('row id: '))
                    ids.append(idd)
                a.delete_data(obj_name,ids)
                
            elif ans == 5:
                a.rollback()
                print('All changes cancelled')
           
            elif ans == 6:
                a.commit()
                print('All changes commited')
                break
                    
            else:
                print('Incorrect input')
                     
    except Exception as e:
            a.rollback()
            a.close_session()
            print(e)


if __name__ == "__main__":
    crud_menu()
    #queries_examples()
    #test_procedures()