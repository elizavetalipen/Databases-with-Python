# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, select, text, func
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, validates
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError, DataError
import datetime
import csv
from tables_world import *

def big_cities_on_each_continent_select(engine,population):
    
    with engine.connect() as conn:
        result = conn.execute(select(Country.continent, func.count(City.id).label("count")).
        group_by(Country.continent).join(Country, City.countrycode == Country.code).where(City.population>population))
    
    print(result.all())


# TODO сдeлать через select
# Сколько городов с населением выше 1000000 человек находится на каждом континенте
def big_cities_on_each_continent(cur_session, population):

    query = cur_session.query(func.count(City.id), Country.continent).group_by(Country.continent)
    query = query.join(Country, City.countrycode == Country.code)
    query = query.filter(City.population>population).all()
    for i in query:
        print('\n')
        print(i)
        
# Выведите страны Азии, среднее население в которых превышает среднее 
# население в первых 30 городах России по населению
def asian_countries_select(engine):
    with engine.connect() as conn:
        cities_pop = select(func.avg(City.population).label("pop")).\
        join(Country,City.countrycode == Country.code).where(Country.name=='Russian Federation').subquery()
        
        countries = select(Country.name, Country.population).\
            where(Country.continent=='Asia' and Country.population > cities_pop.c.pop)
        
        for row in conn.execute(countries).all():
            print(row)
        
        
# Выведите страны Азии, среднее население в которых превышает среднее 
# население в первых 30 городах России по населению
def asian_countries(cur_session):
    cities_pop = cur_session.query(func.avg(City.population))
    cities_pop = cities_pop.join(Country,City.countrycode == Country.code)
    rus_cities_pop = cities_pop.filter(Country.name=='Russian Federation').order_by(City.population.desc()).limit(30).scalar()
    print(f'Среднее население 30 самых больших городов России: {rus_cities_pop}')
    countries = cur_session.query(Country.name, Country.population)
    countries = countries.filter(Country.continent=='Asia' and Country.population > rus_cities_pop)
    for i in countries:
        print('\n')
        print(i)
    
# 3.Сколько всего различных языков можно встретить в странах с различными формами правления
def distinct_languages(cur_session):
    query = cur_session.query(func.count(CountryLanguage.language.distinct()), Country.governmentform).group_by(Country.governmentform)
    query = query.join(Country, CountryLanguage.countrycode == Country.code)
    
    for q in query:
        print('\n')
        print(q)
        
def distinct_languages_select(engine):
    with engine.connect() as conn:
        langs = select(func.count(CountryLanguage.language.distinct()),Country.governmentform).\
         group_by(Country.governmentform).join(Country, CountryLanguage.countrycode == Country.code)  
         
        for row in conn.execute(langs).all():
             print(row)

# сколько всего регионов в Европе?
def count_regions_in_europe(cur_session):
    regions = cur_session.query(func.count(Country.region.distinct()))
    regions = regions.filter(Country.continent=='Europe').scalar()
    print(f'В Европе {regions} регионов ')
    
def count_regions_in_europe_select(engine):
    with engine.connect() as conn:
        result = select(func.count(Country.region.distinct())).where(Country.continent=='Europe')
        for row in conn.execute(result).first():
             print(row)

# Вывести страны количество чётных цифр в году независимости которых превышает количество официальных языков.
def count_even_digits(x:str):
    try:
        x = int(x[:4])
        res = len([ y for y in str(x) if int(y) % 2 == 0])
    except Exception:
        res = 0
    finally:
        return res
            
def countries_and_languages_select(engine):
    with engine.connect() as conn:    
        l = select(func.count(CountryLanguage.language).label('langs'),\
            CountryLanguage.countrycode).group_by(CountryLanguage.countrycode).\
            where(CountryLanguage.isofficial == 'T').subquery()
            
        y = select(l.c.langs, Country.code, Country.name, Country.indepyear).\
            join(l, l.c.countrycode == Country.code)
            #where(int(count_even_digits(str(Country.indepyear)))>l.c.langs)
            
        for row in conn.execute(y).all():
            i = int(count_even_digits(str(row.indepyear)))
            if i < row.langs:
                print(row)
                
def progression(n, b1, q):
    ''' Вернет кортеж из суммы прогресии как числа и строки с записью прогрессии'''
    elems, s = str(b1)+', ', b1
    b_prev = b1
    for i in range(1,n):
        b_cur = b_prev*q
        s += b_cur
        elems = elems + str(b_cur) + ', '
        b_prev = b_cur
    return (elems, s)
      
# вывести страны количество букв в назваии которых может представлено как сумма членов некоторой геом прогресси
# вывести страну название и прогрессию
def progression_select(engine, n, b1, q):
    s = progression(n, b1, q)[1]
    with engine.connect() as conn:
        countries = select(Country.name)
        for row in conn.execute(countries):
            if len(str(row.name).replace(" ", "")) == s:
                print(row.name, progression(n,b1,q))


def main():
    engine = create_engine("mysql+pymysql://root:studyBDordie34@localhost/world", encoding="utf-8")
    #Session = sessionmaker(bind=engine, autoflush=False)
    #cur_session = Session()
    
    #asian_countries_select(engine)
    #asian_coutries(cur_session)
    #print('\nГорода-миллионники на каждом континенте')
    #big_cities_on_each_continent(cur_session, 1000000)
    big_cities_on_each_continent_select(engine,1000000)
    #print('\nСколько различных языков можно встретить в странах с разными формами правления')
    #distinct_languages(cur_session)
    distinct_languages_select(engine)
    print('\n')
    #count_regions_in_europe(cur_session)
    count_regions_in_europe_select(engine)
    print('\nСтраны, количество четных чисел в году независимости которых превышает кол-во офиц яз')
    countries_and_languages_select(engine)
    print('\n')
    #cur_session.close()
    progression_select(engine,3,2,2)
    
if __name__ == "__main__":
    main()