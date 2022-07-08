use world;

-- 1. how many cities wth population over 1000000 people there are on each continent
select country.Continent, COUNT(*) as Big_cities from country
inner join city on country.Code=city.CountryCode
where city.Population > 1000000
group by continent;

 -- 30 biggest Russian cities
select AVG(city.Population) as pop from city
inner join country on country.Code=city.CountryCode
where country.Name = 'Russian Federation'
order by city.Population DESC limit 30;

-- 2. select Asian countries, where average population is greater than 
-- population of 30 biggest Russian cities
select country.Name, country.Population, tb_rus.* from country,
(select AVG(city.Population) as pop from city
inner join country on country.Code=city.CountryCode
where country.Name = 'Russian Federation'
order by city.Population DESC limit 30) as tb_rus
where country.Continent='Asia' and country.Population> tb_rus.pop;

-- 3. how many different languages can be found in countries with different goverment forms
select country.GovernmentForm, count(distinct countrylanguage.Language) as N_Langs from country 
inner join countrylanguage on country.Code=countrylanguage.CountryCode
group by GovernmentForm;

-- 4. count regions in Europe
select distinct country.Region from country
where country.Continent='Europe';

select count(distinct country.Region) from country
group by country.Continent
having country.Continent='Europe';

-- 5. Select the countries where the number of even digits in their independence year 
-- is greater than the number of official languages
select country.Name, IndepYear, langs.* from country
inner join countrylanguage on country.Code=countrylanguage.CountryCode,
(select count(Language) as N from countrylanguage
where IsOfficial='T' group by CountryCode) as langs
where IndepYear is not null and 
length(regexp_replace(cast(IndepYear as char(4)),'0|1|3|5|7|9',''))>langs.N
group by country.Name;

-- 6. Select four big cities with population over 1 000 000 o each continent
select country.Continent as Cont,
substring_index(group_concat(city.Name order by city.Population desc),',',4) as Big_cities from country
inner join city on country.Code=city.CountryCode
where city.Population > 1000000
group by country.Continent;

-- MERGE
create or replace algorithm= merge 
view Info_merge as
select city.Name as Название_Города, city.Population as Население,
city.District as Район, country.Name as Страна, country.Region as Регион,
group_concat(countrylanguage.Language) as Языки,
country.GovernmentForm as Форма_Правления
 from city
inner join country on country.Code=city.CountryCode
inner join countrylanguage on country.Code=countrylanguage.CountryCode
where city.Population between 11002 and 120009999 
group by country.Name;
