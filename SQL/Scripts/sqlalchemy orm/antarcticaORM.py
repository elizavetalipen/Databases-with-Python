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
import datetime
from tables_antarctica import *

class AntarcticaORM:
    
    def __init__(self):
        self.engine = None
        self.cur_session = None
        self.objects = {'Organisation': Organisation, 'Department':Department,\
        'LiveBlock':LiveBlock,'Worker': Worker, 'Medcard':Medcard,'Contract':Contract}
        
    def start_session(self):
        self.engine = create_engine("mysql+pymysql://root:studyBDordie34@localhost/antarctica", encoding="utf-8")
        session = sessionmaker(bind=self.engine)
        self.cur_session = session()
        
    def close_session(self):
        self.cur_session.close()
        
    def commit(self):
        self.cur_session.commit()
        
    def flush(self):
        self.cur_session.flush()
        
    def rollback(self):
        self.cur_session.rollback()
    
    ######################## QUERIES #########################################
    
    def write_query_sql(q:str):
        ''' Sql-query is an input argument''' 
        with self.engine.connect() as conn:
            result = conn.execute(text(q))
            return result.all()
    
    def objects_count(self, obj) -> int:
        count = self.cur_session.query(obj).count()
        return count
    
    def worker_by_letter(self, letter:str):
        selected = self.cur_session.query(Worker).filter(Worker.name.like(f'{letter}%')).all()
        return selected 
    
    def worker_joined(self, lim:int):
        ''' Select full worker profile'''
        query = self.cur_session.query(Worker, Contract, Medcard)
        query = query.join(Worker, Worker.idd == Contract.idd)
        query = query.join(Medcard, Worker.idd == Medcard.idd)
        query = query.limit(lim)
        return query
    
    def worker_partition(self):
        selected = self.cur_session.query(Worker,over(func.row_number(),\
		      partition_by=Worker.department))
            
        return selected.all()
    
    
    def load_data(self, obj_name, mode='eager')->list:
        ''' Loads data from table'''
        
        obj = self.objects[obj_name] 
        if mode == 'eager':
            if obj.__tablename__ == 'deps':
                obj_list = self.cur_session.query(Department).options(joinedload(Department.worker)).all()
                    
            elif obj.__tablename__ == 'live_blocks':
                obj_list = self.cur_session.query(LiveBlock).options(joinedload(LiveBlock.worker)).all()
                            
            else:
                obj_list = self.cur_session.query(obj)
                
        elif mode == 'lazy':
                obj_list = self.cur_session.query(obj)
                       
        return obj_list
    
   ######################  PROCEDURES #########################################
   
    def server_procedure(self, proc_name, params):
        raw_conn = self.engine.raw_connection()
        cur = raw_conn.cursor()
        cur.callproc(proc_name, params)
   
    def free_roomsQ_server(self, blockId:int)->bool:
         return self.cur_session.execute(func.free_roomQ(blockId)).scalar() 
    
    def free_roomsQ_client(self,blockId:int)->bool:
        block = self.cur_session.query(LiveBlock).filter(LiveBlock.idd == blockId).first()
        free_spaces = block.rooms*3 - block.people
        if free_spaces > 1:
            return True
        else:
            return False
   
    def presentQ_server(self, date)->bool:
       return self.cur_session.execute(func.worker_presentQ(date)).scalar() 
   
    def presentQ_client(self, date:str)->bool:
       cur_year_month = datetime.now().strftime('%Y-%m')
       if cur_year_month == date[:7]:
           return True
       else:
           return False
         
   ######################  CRUD  ##############################################
   
    def insert_data(self, obj_name:str):
        
        obj = self.objects[obj_name] 
        data = self.load_data(obj_name)
        ids = []
        
        for i in data:
            ids.append(int(i.idd))
        
        last_id = sorted(ids)[-1]
            
        colnames = [column.key for column in obj.__table__.columns]
        x = len(colnames)
        attrs = [attr for attr in list(vars(obj).keys()) if attr[0]!='_']
        
        try:
            q = obj_name + f'(idd = {last_id+1}, '
            for i in range(1,x-1):
                val = input(f'{attrs[i]} = ')
                q = q + f'{attrs[i]} = {val},'
            
            val_last = input(f'{attrs[x-1]} = ')
            q = q + f'{attrs[x-1]} = {val_last}' + ')'
            
            new_obj = eval(q)
            self.cur_session.add(new_obj)
            print(new_obj)
            
        except Exception as e:
            print(e)
            

    def delete_data(self, obj_name:str, ids:list):
        obj = self.objects[obj_name] 
        try:
            obj_list = self.cur_session.query(obj)
            
            for i in ids:
                cur_obj = obj_list.filter((obj).idd == i).first()
                self.cur_session.delete(cur_obj)
            print(f'{len(ids)} rows were deleted')
            
        except Exception as e:
            print(e)
        
        
    def update_data(self, obj_name:str, idd:int):
        
        obj = self.objects[obj_name] 
        colnames = [column.key for column in obj.__table__.columns]
        x = len(colnames)
        attrs = [attr for attr in list(vars(obj).keys()) if attr[0]!='_']
        
        try:
            cur_obj = self.cur_session.query(obj).filter(obj.idd == idd).first()
            print(cur_obj)
            
            for i in range(1,x):
                print(i,attrs[i])
            
            n = int(input('Choose attribute: '))
            val = input('Value: ')
            setattr(cur_obj,attrs[n],val)
            print(cur_obj) 
      
        except Exception as e:
            print(e)

    
    def print_data(self, obj_list, linked=True):
        
        for instance in obj_list:
            
            if str(type(instance))== "<class 'tables.Worker'>" and linked ==True:
                print(instance)
                print('')
                print(instance.contract)
                print('')
                
                print('')
                print(instance.supplies)
                print('')
                
                print(instance.rel_department)
                print('')
                    
                print(instance.rel_block)
                print('')
                print('--------------------'*2)
                    
            elif str(type(instance))== "<class 'tables.Contract'>" and linked ==True:
                print(instance)
                print('')
                print(instance.worker)
                print('--------------------'*2)
                print('')
                
            elif str(type(instance))== "<class 'tables.LiveBlock'>" and linked ==True:
                print(instance)
                print('')
                if instance.worker != []:
                    for w in instance.worker:
                        print(w)
                    print('--------------------'*2)
                    print('')
                    
            elif str(type(instance))== "<class 'tables.Department'>" and linked ==True:
                print(instance)
                print('')
                if instance.worker != []:
                    for w in instance.worker:
                        print(w)
                    print('--------------------'*2)
                    print('')
                
            else:
                print(instance)
                print('')
                

                
        


