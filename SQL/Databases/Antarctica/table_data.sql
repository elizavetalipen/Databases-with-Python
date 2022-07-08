insert into organisations(org_name, org_purpose,
start_date, end_date, contr_type) values
('NASA','Astronomical observations','1999-10-11','2050-10-11','winter'),
('Antarctic Adventure','Tourism','2010-10-18','2022-10-18','summer'),
('GeoWeatherStation','Meteorology','2003-01-01','2025-01-01','winter'),
('EcoCare','Ozone layer research','1994-01-01','2040-01-01','summer');

insert into deps(dep_name)values
('airport'),('lab'),('kitchen'),('outbuildings'),('meteostation'),('hospital'),('other');
insert into live_blocks(block_rooms)values
(3),(5),(8),(10),(20),(10),(20),(10);

-- input agruments:
-- name, position, salary int, start date, end date, contract type,
-- organisation (0), birthdate, gender, height, weight, blood sugar, saturation, enum('sang','phleg','chol','mel')
call create_worker('Elizaveta Lipen','Administrator',1,750000,'2021-10-23','2022-03-05',
0,'2003-02-02','f',1.73,68,5,100,'mel');
call create_worker('Charles Hill','Pilot',1,940000,'2021-11-01','2022-03-01',
0,'1997-12-23','m',1.84,74, 5, 98,'chol');
call create_worker('Howard Jakeman','Operator',1,820000,'2021-11-02','2022-03-01',
0,'1993-03-01','m',1.8,70, 4.8, 99,'sang');
call create_worker('Tomas Dove','Cook',1,50000,'2021-10-05','2022-03-05',
0,'1988-03-17','m',1.8,70,5,99,'sang');
call create_worker('Anthony King','Assistant',1,600000,'2021-10-01','2022-03-30',
1,'2001-02-03','m',1.76,72,4.6, 99,'mel');
call create_worker('Emma Jacobson','Astronomer',1,900000,'2021-10-15','2022-03-15',
1,'1980-04-14','f',1.7,66,4.8, 98,'chol');
call create_worker('Julia Taylor','Nurse',1,720000,'2021-09-01','2022-03-01',
0,'2000-04-08','m',1.65,62, 5.5, 99,'mel');
call create_worker('Agnessa Barton','Astronomer',1,850000,'2021-10-15','2022-03-15',
1,'1985-12-12','f',1.68,60,5, 99,'phleg');
call create_worker('Jessie Lukas','Astronomer',2,850000,'2021-10-15','2022-03-11',
1,'1985-03-17','m',1.85,75, 4.6, 100,'phleg');
call create_worker('Charlie Morgan','Meteorologist',2,600000,'2022-09-01','2022-03-12',
3,'1985-12-12','m',1.67,58,4.9, 98,'mel');
call create_worker('Bill Bailey','Driver',70000,2,'2022-05-02','2022-08-15',
0,'1980-01-09','m',1.78,75,4.9, 100,'phleg');
call create_worker('Jessica Nolan','Tourism Manager',2,60000,'2022-05-04','2022-08-04',
2,'1999-10-14','f',1.63,55,4.6, 99,'sang');
call create_worker('Peter Duncan','Driver',2,50000,'2022-05-01','2022-09-15',
0,'1989-06-28','m',1.79,70, 5.6, 99,'sang');
call create_worker('Lewis Heil','Hydrologist',2,200000,'2022-05-01','2022-09-15',
4,'1997-08-20','m',1.73,68,5, 99,'mel');
call create_worker('Victoria Heil','Ecologist',2,210000,'2022-06-11','2022-08-15',
4,'1999-04-28','f',1.7,65,5, 100,'sang');
call create_worker('Chris Hardy','Geophysicist',2,225000,'2022-06-21','2022-07-30',
4,'1993-11-16','m',1.85,76, 4.75, 99,'sang');
call create_worker('Thomas Mayers','Hydrologist',2,200000,'2022-06-01','2022-09-10',
4,'1986-02-24','m',1.84,68,4.6, 99,'chol');
call create_worker('Angela Johnson','Assistant',2,180000,'2022-06-21','2022-09-10',
4,'2000-06-14','f',1.68,63,4.6, 99,'chol'); 
call create_worker('James Adams','Anesthesiologist',3,850000,'2021-10-01','2022-04-01',
0,'1984-05-23','m',1.77,70, 5.3, 100,'phleg');
call create_worker('Harold Austin','Surgeon',3,980000,'2021-10-01','2022-05-21',
0,'1984-05-23','m',1.81,76, 5.1, 100,'sang');
call create_worker('Adam Baker','Traumatologist',3,850000,'2021-10-01','2022-04-24',
0,'1989-03-08','m',1.74,70, 5.5, 98,'phleg');
call create_worker('Arthur Aston','Disel engineer',3,60000,'2021-09-10','2022-03-10',
0,'1975-12-23','m',1.81,75,5, 99,'chol');
call create_worker('Sarah Lynn','Systems Administrator',3,55000,'2021-09-10','2022-03-10',
0,'2000-12-24','f',1.66,59,4.7, 99,'phleg');
call create_worker('Polina Simonova','Psycologist',3,750000,'2022-06-01','2022-09-01',
0,'1989-03-08','f',1.74,63, 5.1, 99,'sang');
call create_worker('Alexander Bennet','Pilot',4,920000,'2022-06-02','2022-08-01',
0,'1995-03-03','m',1.78,69, 5.1, 99,'sang');
call create_worker('Carl Hart','Pilot',4,940000,'2022-05-02','2022-09-01',
0,'1997-10-15','m',1.8,76, 5.4, 99,'phleg');
call create_worker('Steven Peterson','Engineer',4,700000,'2021-10-20','2022-04-02',
1,'2001-12-23','m',1.79,67, 5, 100,'chol');
call create_worker('Logan Fell','Assistant',4,90000,'2021-09-10','2022-04-10',
0,'1978-02-04','m',1.88,78, 5.4, 99,'chol');
call create_worker('Steven Brooke','Meteorologist',4,85000,'2021-10-16','2022-05-01',
3,'1996-12-20','f',1.76,68, 5, 99,'sang');
call create_worker('Sheila Anderson','Cook',5,6500,'2021-09-02','2022-04-01',
0,'1996-12-20','f',1.60,52, 5.2, 100,'mel');
call create_worker('Kate Smith','Nurse',5, 5000,'2021-10-10','2022-05-10',
3,'1991-11-20','f',1.56,48, 4.6, 99,'sang');
call create_worker('August Brown','Driver',5,45000,'2021-09-01','2022-03-15',
0,'1998-07-28','m',1.84,76, 5.3, 99,'phleg');
call create_worker('Carol Jackson','Engineer',5,700000,'2021-10-20','2022-04-02',
0,'1990-12-23','f',1.69,57, 5, 100,'sang');
