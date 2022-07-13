from MongoFurnitureCRUD import *
from pprint import pprint
import json
import os
from datetime import datetime

class Console:

    def __init__(self):
        self.menu = '''
        0. Exit
        1. Insert
        2. Read
        3. Update
        4. Delete by name
        5. Work with files
        6. Agregation and query examples
        '''
        
        self.queries_menu = '''
        1. Get orders if more than d days passed
        2. Average cost of the materials in each order
        3. Supplier + list of supplied materials
        4. Min and max prices
        '''
        
    def make_document(self,colname):
        if colname == "suppliers":
            adr = input("Adress: ")
            name = input("Name: ")
            manager = input("Manager: ")
            startDate = input("Date format: 12/06/2021 09:15:32 \nStart Date: ")
            # "12/06/2021 09:15:32"
            #startDate =  datetime.strptime(startDate, "%d/%m/%Y %H:%M:%S")
            endDate = input("Date format: 12/06/2021 09:15:32 \nEnd Date: ")
            #endDate =  datetime.strptime(endDate, "%d/%m/%Y %H:%M:%S")
            
            doc = {"Name":name,"Address":adr,"Manager":manager,\
                  "Start_date": startDate,"End_date": endDate}
                
        elif colname == "materials":
            name = input("Name: ")
            cost = int(input("Cost: "))
            quality = input("Quality: ")
            color = input("Color: ")
            supID = input("Supplier ID: ")
            doc = {"Name":name,"Cost":cost,"Desc": {"quality":quality,"color":color},
                   "Supplier": DBRef("suppliers", supID)}
            
        else:
             raise NameError("Such collection does not exist")
        return doc
    
    def make_update_query(self,colname, recname):
        if colname == "suppliers":
            fields = ["Name", "Address","Manager"]
            for i in range(len(fields)):
                print(f'{i+1}. '+str(fields[i]))
                
            choise = int(input("\nChoose a field to update: "))
            if choise == 1:
                newval = input("New value: ")
                query = [{"Name":recname},{ "$set": {"Name": newval }}]
                
            elif choise == 2:
                 newval = input("New value: ")
                 query = [{"Name":recname},{ "$set": {"Address": newval }}]
                 
            elif choise == 3:
                 newval = input("New value: ")
                 query = [{"Name":recname},{ "$set": {"Manager": newval }}]
                 
            else:
                raise NameError("Wrong input")
        
        else:
            raise NameError("Such collection does not exist")
        return query
            
        
    
    def run(self):
        client = MongoFurnitureCRUD()
        while True:
            print(self.menu)
            ans = int(input("Choose option: "))
            
            if ans == 0:
                break
            # INSERT 
            elif ans == 1:
                try:
                    colname = input("Collection: ")
                    if colname == "orders":
                        client.create_order()
                    else:
                        doc = self.make_document(colname)
                        res = client.add_record(colname, [doc])
                        print(res)
                except Exception as e:
                    print(e)
                
            # READ 
            elif ans == 2:
                try:
                    colname = input("Collection: ")
                    print("1.Get all records\n2.Get record by objectID")
                    ans2 = int(input("Choose option: "))
                    if ans2 == 1:
                        docs = client.get_records(colname)
                        for doc in docs:
                            print("-"*50)
                            print('\n')
                            pprint(doc)
                            
                    elif ans2 == 2:
                        objid = input("Object Id: ")
                        doc = client. get_by_id(colname, objid)
                        print(doc)
                        
                except Exception as e:
                    print(e)
                    
            # UPDATE     
            elif ans == 3:
                try:
                    colname = input("Collection: ")
                    recname = input("Record name: ")
                    updq = self.make_update_query(colname, recname)
                    print(client.update_records(colname,updq[0], updq[1]))
                except Exception as e:
                    print(e)
            
            # DELETE
            elif ans == 4:
                try:
                    colname = input("Collection: ")
                    recname = input("Name: ")
                    query = {"Name": recname}
                    print("1.Save to json \n2.Without saving")
                    ans4 = int(input("Choose option: "))
                    safemode = True
                    if ans4 == 2:
                        safemode = False 
                    print(client.delete_records(colname, query, safemode))
                except Exception as e:
                    print(e)
            
            # JSON FILES 
            elif ans == 5:
                try:
                    print("1.From json file\n2.To json file")
                    ans5 =  int(input("Choose option: "))
                    if ans5 == 1:
                        path = input("Path to file: ")
                        colname = input("Collection: ")
                        client.import_from_file(colname, path)
                    
                    elif ans5 == 2:
                        colname = input("Collection: ")
                        client.export_to_file(colname)
                except Exception as e:
                    print(e)
                
            elif ans == 6:
                try:
                    print(self.queries_menu)
                    ans6 = int(input("Choose option: "))
                    if ans6 == 1:
                        days = int(input("Days: "))
                        docs = client.days_back(days)
                        for doc in docs:
                            print("-"*50)
                            print('\n')
                            pprint(doc)
                            
                    elif ans6 == 2:
                        docs = client.materials_avg_cost()
                        for doc in docs:
                            print("-"*50)
                            print('\n')
                            pprint(doc)
                            
                    elif ans6 == 3:
                        docs = client.suppliers_materials()
                        for doc in docs:
                            print('Name: ' + doc["Name"])
                            print('Materials: ')
                            print(doc["Sold_materials"])
                            
                    elif ans6 == 4:
                        docs = client.min_and_max()
                        for doc in docs:
                            pprint(doc)
                            
                except Exception as e:
                    print(e)
                
            elif ans == 7:
                pass
            else:
                print("Incorrect input")
                
if __name__ == '__main__':
    console = Console()
    console.run()
