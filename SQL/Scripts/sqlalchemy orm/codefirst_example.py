import random
import string
import sqlalchemy
from sqlalchemy import create_engine, insert, update, text, ForeignKeyConstraint, PrimaryKeyConstraint
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload, contains_eager
from datetime import datetime
from sqlalchemy_utils import database_exists, create_database, drop_database
import pymysql


Base = declarative_base()

# association table            
class Sell(Base):
    __tablename__ = 'sells'
    
    seller_id = Column(ForeignKey('sellers.seller_id'), primary_key = True)
    product_id = Column(ForeignKey('products.prod_id'), primary_key = True)
    date = Column("sell_date", DateTime, nullable=False)
    child = relationship("Product")
   
    def __repr__(self):
        return "<Sell(seller='%s', product='%s', date ='%s')>"\
            % (self.seller_id, self.product_id, self.date)

class Product(Base):
     __tablename__ = 'products'
     
     idd = Column("prod_id", Integer, primary_key=True)
     name = Column("prod_name", String(40), nullable=False)
     category = Column("prod_category", String(20), nullable=False)
     price = Column("prod_price",Float)
     
     def __repr__(self):
         return "<Product(id ='%s', name='%s', category='%s', price='%s')>" \
             % (self.idd, self.name, self.category, self.price)
             
# parent            
class Seller(Base):
    __tablename__ = 'sellers'
    
    idd = Column("seller_id", Integer,primary_key=True)
    
    ref_contr_id = Column(Integer, ForeignKey("contracts.contr_id"))
    insurance_id = Column(Integer, ForeignKey("contracts.contr_id"))
    
    name = Column("seller_name", String(30))
    position = Column("seller_position", String(30))
    
    # один-к-одному
    '''contract = relationship("Contract", back_populates='seller',\
                             cascade="all, delete, delete-orphan", uselist=False)'''
        
    ref_contr = relationship("Contract", foreign_keys=[ref_contr_id], cascade="all, delete, delete-orphan", single_parent=True)
    insurance = relationship("Contract", foreign_keys=[insurance_id], cascade="all, delete, delete-orphan", single_parent=True)
        
    children = relationship("Sell")  

    def __repr__(self):
        return "<Seller(id ='%s', name='%s', position='%s')>"\
            % (self.idd, self.name, self.position)

            
class Contract(Base):
     __tablename__ = 'contracts'
     
     idd = Column("contr_id", Integer,primary_key=True)
     #seller_id = Column("seller_id", ForeignKey(Seller.ref_contr),Integer,primary_key=True)
     start_date = Column("start_date", DateTime)
     duration = Column("duration", Integer)
     salary = Column("salary",Integer)
     
     # relationships
     '''seller = relationship("Seller",back_populates="contract",\
                           cascade="all, delete, delete-orphan",single_parent=True)'''
     # representation
     def __repr__(self):
         return '''<Contract(id ='%s', start_date='%s', duration='%s',salary='%s')>'''\
             % (self.idd, self.start_date,self.duration,self.salary)
    
   
#############################################################################

''' Создание бд
Доп задание: если запускаем программу второй раз, код проверяет если в каждой таблице на данный момент 
меньше 100 записейБ то дозаполнять до 100 '''  
  
objects = {'Product':Product,'Seller':Seller,'Sell':Sell, 'Contract':Contract}
engine = create_engine("mysql+pymysql://root:studyBDordie34@localhost/testshop", encoding="utf-8")
Session = sessionmaker(bind=engine)
cur_session = Session()

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def create_db(engine, cur_session):

    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(engine)
        
        # заполнение таблиц
        new_prod1 = Product(idd=1, name = 'oat milk', category = 'food',price=4.5)
        new_prod2 = Product(idd=2, name = 'shower gel', category = 'beauty',price=5)
        
        new_seller1 = Seller(idd=1,ref_contr_id=101,insurance_id =101, name = 'Masha', position = 'Manager')
        new_seller2 = Seller(idd=2,ref_contr_id=102,insurance_id =102 ,name = 'Sasha', position = 'Assistant')
        new_cont1 = Contract(idd = 101, start_date = '2021-10-11',duration = 3, salary = 1000)
        new_cont2 = Contract(idd = 102, start_date = '2022-01-01',duration = 2, salary = 800)
        
        new_sell = Sell(seller_id =2, product_id =1, date = '2022-04-04')
       
        cur_session.add(new_prod1)
        cur_session.add(new_prod2)
        cur_session.add(new_seller1)
        cur_session.add(new_seller2)
        cur_session.add(new_cont1)
        cur_session.add(new_cont2)
        cur_session.add(new_sell)
        cur_session.commit()
        print('New database created!')
        
    else:
        print('Database already exists')
        product_count = int(cur_session.query(Product).count())
        if product_count < 100:
        
            prod_dict = {'food':['chocolate','soda','avocado','beer','candy',\
            'yogurt','coffee','grains','water','ice cream','cheesecake','brownies',\
            'chicken nuggets','cereals'], 'beauty': ['lipstick','nail polish','facial cleaner'\
            'hair dryier', 'spray', 'sculpting cream','face roller','sunscreen','scrub','rose oil'\
            'curling iron', 'hand cream', 'lip balm','eyeliner','concealer'],\
            'toys':['teddy bear', 'robot','Iron Man figure','Barbie','dollhouse','pokemon','DIY set',\
            'UNO','Spiderman','My Little Pony','transformer','dinosaur','Baby Yoda','Batman figure'],\
            'clothes':['sneakers','black dress','skirt','red shoes','hoodie','trench','Hawaiian shirt',\
            'socks','swimsuit','flip flops','mittens','blazer','jumper','long-sleeve top']}
            
            kys = list(prod_dict.keys())   
            
            # генерация айдишника
            ids, i  = [], 0
            data = load_data(Product) 
            for d in data:
                ids.append(int(d.idd))
            # если промежуточные записи были удалены это не имеет значения
            last_id = sorted(ids)[-1]
            
            while product_count < 100:
                i += 1
                prodId = last_id + i
                prodCategory = kys[random.randint(0, len(kys)-1)]
                vals = prod_dict[prodCategory]
                prodName = vals[random.randint(0, len(vals)-1)]
                prodPrice = random.uniform(2, 100)
                
                new_prod = Product(idd=prodId, name = prodName, category = prodCategory,price=prodPrice)
                cur_session.add(new_prod)
                cur_session.commit()
                
                product_count += 1
              
###############################################################################

def load_data(obj)->list:
    obj_list = cur_session.query(obj)
    return obj_list

  
def main():
    create_db(engine, cur_session)
 

if __name__ == "__main__":
    main()
    
    
