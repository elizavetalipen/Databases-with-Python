# -*- coding: utf-8 -*-

from pymongo import MongoClient
from pprint import pprint
import json
from bson import ObjectId
import os
from bson import DBRef
import gridfs
from datetime import datetime, timezone
from datetime import timedelta

class MongoFurnitureCRUD:
    
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client.furniture
        self.orders_collection = self.db.shop.orders
        self.items_collection = self.db.shop.items
        self.suppliers_collection = self.db.suppliers
        self.materials_collection = self.db.materials
        self.fs = gridfs.GridFS(self.db) #для работы с картинками
        
        self.collections = {"orders":self.orders_collection,"items":self.items_collection,\
                            "materials":self.materials_collection,"suppliers":self.suppliers_collection}
            
    # find returns cursor
    def get_records(self,colname, *docs):
        if colname not in list(self.collections.keys()):
            raise NameError("No such collection in the database")
        coll = self.collections[colname]
        return [elem for elem in coll.find(*docs)]
    
    
    def get_by_id(self,colname, id):
       if colname not in list(self.collections.keys()):
           raise NameError("No such collection in the database")
       coll = self.collections[colname]
       document = coll.find_one({'_id': ObjectId(id)})
       return document
   
    def update_records(self,colname, *args, **kwargs):
        coll = self.collections[colname]
        response = coll.update_many(*args, **kwargs)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output
   
    # insert one
    def add_record(self,colname, docs:list):
      if colname not in list(self.collections.keys()):
          raise NameError("No such collection in the database")
      coll = self.collections[colname]
      for doc in docs:
          if colname == "orders":
              if not ("Name" in doc.keys() and "Items" in doc.keys()):
                  raise KeyError
          if colname == "items":
              if not ("Name" in doc.keys() and "Type" in doc.keys()):
                  raise KeyError        
          if colname == "materials":
               if not ("Name" in doc.keys() and "Cost" in doc.keys()):
                   raise KeyError
          if colname == "suppliers":
               if not ("Name" in doc.keys() and "Address" in doc.keys()):
                   raise KeyError  
      if len(docs)==1:
          response = coll.insert_one(docs[0])
      else:
          response = coll.insert_many(docs)
      output = {'Status': 'Successfully Inserted',
                'Document_ID': str(response.inserted_id)}
      return output
  
    def delete_records(self, colname, query, safemode = True, many = False):
        ''' Deleting with backup'''
        
        if colname not in list(self.collections.keys()):
            raise NameError("No such collection in the database")
            
        coll = self.collections[colname]
        out = self.get_records(colname, query)
        if many:
            docs = coll.find(query)
            response = coll.delete_many(query)
        else:
            docs = coll.find_one(query)
            response = coll.delete_one(query)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        
        if safemode:
            path = colname + 'backup'+ '.json'
            qua = len(out)
            with open(path, 'w') as json_out_file:
                json_out_file.write('[')
                for i, document in enumerate(out):
                    json_out_file.write(json.dumps(document, default=str))
                    if i != qua - 1:
                        json_out_file.write(',')
                    json_out_file.write(']')
            print("Json was saved")
        return output
    
####################### WORK WITH FILES #######################################
    
    def import_from_file(self,colname, path: str):
        if colname not in list(self.collections.keys()):
            raise NameError("No such collection in the database")
         
        with open(path) as json_inp_file:
            data = json.load(json_inp_file)
        for doc in data:
            if "_id" in doc:
                doc["_id"] = ObjectId(doc["_id"])
            else:
                pass
        self.add_record(colname,[doc])
        print("Record from file added")
     
     
    def export_to_file(self,colname,  path="test.json"):
         if colname not in list(self.collections.keys()):
             raise NameError("No such collection in the database")
             
         docs = self.get_records(colname)
         qua = len(docs)
         with open(path, 'w') as json_out_file:
             json_out_file.write('[')
             for i, document in enumerate(docs):
                 json_out_file.write(json.dumps(document, default=str))
                 if i != qua - 1:
                     json_out_file.write(',')
                 json_out_file.write(']')
         print("Json was saved")
         
######################## QUERIES AND BUSINESS LOGIC ###########################

    def days_back(self, d:int, datename="Start_date"):
        ''' Получить заказы, с момента оформления или доставки которых прошло больше d дней'''
        today = datetime.today()
        days_back = today - timedelta(days=d)
        criteria = {"$and": [{datename: {"$gte": days_back}}]}
        document = self.orders_collection.find(criteria)
        return document
    
    def create_order(self):
        startDate = datetime.now()
        endDate = startDate + timedelta(days=5)
        name = input("Your name: ")
        email = input("Your email: ")
        adr = input("Your adress: ")
        
        items_ = self.get_records("items")
        item_names = []
        for i in items_:
            item_names.append(i["Name"])
            
        print("\nAvailable items")
        for it in item_names:
            print(it)
        
        # choosing items 
        n = int(input("How many items you order? "))
        items = []
        for i in range(n):
            itemName = input("Item name: ")
            if itemName not in item_names:
                raise NameError("No such item")
            item = self.items_collection.find_one({"Name":itemName})
            items.append(item)
            
        doc = {"Start_date":startDate,"Delivery_date": endDate,
               "Name":name,"Personal_info": 
            {"email":email,"adress":adr,"membership":"unknown"},"Items": items}
            
        self.orders_collection.insert_one(doc)
        print("Order was created")

                 
######################## AGREGATION ###########################################
    def materials_avg_cost(self):
        ''' Средняя цена материалов в заказе'''
        document = self.orders_collection.aggregate([{ "$unwind": "$Items.Material" },
        {"$group": {"_id": "$_id","avgcost": { "$avg": "$Items.Material.Cost" }}}])
        return document
    
    def min_and_max(self):
        ''' Минимальная и максимальная цены товаров'''
        document = self.items_collection.aggregate([{"$group":{"_id":"$Items.Name",
        "min": {"$min":"$Cost"},
        "max":{"$max":"$Cost"}}}])
        return document
    
    def suppliers_materials(self):
        ''' Поставщик и список поставляемых материалов'''
        document = self.suppliers_collection.aggregate([{"$lookup": {"from": "materials",
                                                 "localField": "_id",
                                                 "foreignField": "Supplier.$id",
                                                 "as": "Sold_materials"}}])
        return document
    
    def convert_json_supplier(doc):
         """"converts json format dict to lists of names and values"""
         try:
             data = []
             data.append(doc["_id"])
             data.append(doc["Name"] + " " + doc["Manager"])
             if "Address" in doc:
                 data.append(doc["Address"])
             else:
                 data.append(None)
             if "Start_date" in doc:
                 data.append(doc["Start_date"])
             else:
                 data.append(None)
             if "End_date" in doc:
                 data.append(doc["End_date"])
             else:
                 data.append(None)
           
             return data
         except KeyError as e:
             print(e)
    

