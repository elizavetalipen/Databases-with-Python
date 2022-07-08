drop database if exists antarctica;
create database antarctica;
use antarctica;

-- organisations wich cooperate with the station
create table organisations(
org_id int not null auto_increment primary key,
org_name varchar(50),
org_purpose varchar(50), 
start_date date,
end_date date,
contr_type enum('summer','winter'));

-- station departments
create table deps(
dep_id int not null primary key auto_increment,
dep_name enum('airport','lab','kitchen','outbuildings',
'meteostation','hospital','other'));

create table live_blocks
(block_id int not null primary key auto_increment,
 block_people int default 0, -- how many peple live in this block
 block_rooms int);

create table workers(
  worker_id int not null primary key auto_increment,
  worker_name varchar(50),
  worker_position varchar(65),
  ref_dep_id int,
  ref_block_id int,
  constraint worker_dep foreign key(ref_dep_id) references deps(dep_id)
  on update cascade on delete cascade,
  constraint worker_block foreign key(ref_block_id) references live_blocks(block_id)
  on update cascade on delete cascade);

create table medcard
(card_id int not null primary key auto_increment,
gender enum('m','f'),
birthday date,
age int, 
height double,
weight double, 
imt double, 
sugar double, 
satur int, 
temper enum('sang','phleg','chol','mel'),
health_points int, 
constraint card_worker foreign key(card_id) references workers(worker_id)
on update cascade on delete cascade);

-- one-time contract
create table contracts(
contr_id int not null primary key auto_increment,
start_date date,
end_date date,
duration int, 
contr_type enum('winter','summer'),
salary int,
ref_org_id int default 0, 
isOver bool default 0,
presentQ bool default 0,
constraint contr_worker foreign key(contr_id) references workers(worker_id)
on update cascade on delete cascade);

create table worker_supplies(
ref_worker_id int primary key,
ref_block_id int,
shower_time int default 10, -- minutes per week
water_vol int default 15, -- liters per week
food_portions int default 21,
gym int default 6, -- hours per week
constraint supplies_worker foreign key(ref_worker_id) references workers(worker_id)
on update cascade on delete cascade);


create or replace algorithm= merge view Сотрудники_организаций as
select org_name as Организация,org_purpose as Цель_пребывания, worker_position as Должность, 
 group_concat(worker_name) as Имя,
dep_name as Подразделение
from contracts 
inner join workers on worker_id = contr_id
inner join deps on ref_dep_id = dep_id 
inner join organisations on org_id = ref_org_id
group by worker_position;

create or replace algorithm= merge view Бытовуха as
select ref_block_id as Блок, count(ref_worker_id) as Проживают, sum(food_portions) as Приемов_пищи,
sum(shower_time)*9 + sum(water_vol) as Общий_расход_воды from worker_supplies
where ref_worker_id is not null and ref_block_id is not null
group by ref_block_id;

create or replace algorithm= merge view Научные_сотрудники as
select worker_name as Имя, worker_position as Должность ,
dep_name as Подразделение, salary as Зарплата from workers
inner join deps on ref_dep_id = dep_id 
inner join contracts on contr_id = worker_id
where ref_dep_id in (2,5) order by salary desc;
