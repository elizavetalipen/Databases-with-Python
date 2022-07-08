use antarctica;

-- 100 points maximum, 75 points minimum
drop trigger if exists check_health;
DELIMITER //
create trigger check_health before insert on medcard
for each row begin
	declare p int;
    set p = 100;
    
    set new.age = timestampdiff(year, new.birthday, curdate());
    if new.age < 18 or new.age > 60 then
		signal sqlstate '45000'
		set message_text = 'Too young or too old';
	elseif new.age > 50 then
		set p = p - 5;
    end if;
    
    set new.imt = new.weight/(new.height*new.height);
	if new.imt < 18.5 or new.imt > 27 then
		signal sqlstate '45000'
		set message_text = 'Bad IMT';
	elseif new.imt between 18.5 and 20 or new.imt > 25 then
		set p = p - 10;
    end if;
    
    if new.satur < 97 then
		signal sqlstate '45000'
		set message_text = 'Bad saturation';
    elseif new.satur < 99 then
		set p = p - 5;
	end if;
    
     if new.sugar < 4.5 or new.sugar > 6 then
		signal sqlstate '45000'
		set message_text = 'Bad blood sugar';
    elseif new.sugar < 4.7 or new.sugar>5.5 then
		set p = p - 10;
	end if;
    if new.temper in ('chol','mel') then
		set p = p - 5;
	end if;
    
    set new.health_points = p;
end //
DELIMITER ;

drop function if exists worker_presentQ;
DELIMITER //
create function worker_presentQ(d date) returns bool
	deterministic
begin
	declare res bool;
	if month(now()) in (9,10,11,12,1,2,3) and month(d) in (9,10,11,12,1,2,3)
    or month(now()) in (4,5,6,7,8) and month(d) in (4,5,6,7,8) then
		set res = 1; 
	else set res = 0; end if;
    return res;
end //
DELIMITER ;

-- check if worker can apply
drop trigger if exists check_contr;
DELIMITER //
create trigger check_contr before insert on contracts
for each row begin
	if timestampdiff(day,now(),new.end_date)<=0 then set new.isOver = 1; end if;
    if new.contr_id in (select contr_id from contracts where year(end_date) = year(new.start_date) ) then
     		signal sqlstate '45000'
			set message_text = 'Already worked this year';
	end if;
    
		if not (new.ref_org_id = 0 ) and new.contr_type not in
		(select contr_type from organisations where org_id = new.ref_org_id) then
				signal sqlstate '45000'
				set message_text = 'Wrong contract type';
		end if;
        
	if month(new.start_date) in (9,10,11,12,1,2,3) then
		set new.contr_type = 'winter';
	else set new.contr_type = 'summer'; end if;
    
    set new.presentQ = worker_presentQ(new.start_date);
	set new.duration = timestampdiff(month, new.start_date, new.end_date);
end //
DELIMITER ;

drop trigger if exists set_dep_id;
DELIMITER //
create trigger set_dep_id before insert on workers
for each row begin
	declare depName enum('airport','lab','kitchen','outbuildings',
'meteostation','hospital','other');

if new.worker_position in ('Pilot','Operator') then
	set depName = 'airport'; 
elseif new.worker_position in ('Assistant','Geophysicist','Astronomer','Hydrologist','Ecologist') then
	set depName = 'lab'; 
elseif new.worker_position in ('Cook') then
	set depName = 'kitchen'; 
elseif new.worker_position in ('Disel engineer','Driver','Engineer','Systems Administrator') then
	set depName = 'outbuildings'; 
elseif new.worker_position in ('Meteorologist') then
	set depName = 'meteostation'; 
elseif new.worker_position in ('Surgeon','Traumatologist','Anesthesiologist','Nurse','Psycologist') then
	set depName = 'hospital'; 
else set depName = 'other'; end if;
set new.ref_dep_id = (select dep_id from deps where dep_name = depName);
end //
DELIMITER ;

drop trigger if exists add_supplies;
DELIMITER //
create trigger add_supplies after insert on workers
for each row begin
	insert into  worker_supplies(ref_worker_id, ref_block_id)
    values (new.worker_id, new.ref_block_id);
end //
DELIMITER ;


drop function if exists free_roomQ;
DELIMITER //
create function free_roomQ(blockId int) returns bool
	deterministic
begin
	-- свободные места в жилом блоке?
	declare free_spaces int; declare res bool; 
    select (block_rooms*3)-block_people into free_spaces from live_blocks where block_id = blockId;
    if free_spaces > 0 then set res = 1; end if;
    if free_spaces <= 0 then set res = 0; end if;
    return res;
end //
DELIMITER ;

-- this transaction adds records to tables: workers, contract, medcard, supplies
drop procedure if exists create_worker;
DELIMITER //
create procedure create_worker(in wname varchar(65), in wpos varchar(30), in blockId int, in salary int,
in d1 date, in d2 date, in orgId int, in bday date, in g enum('m','f'), in wh double, in ww double, 
in sugar double, in satur int, in temper enum('sang','phleg','chol','mel'))
begin
start transaction;
    update live_blocks set block_people = block_people + 1 where block_id = blockId;

    if row_count()>0 then
    -- new worker
    insert ignore into workers(worker_name, worker_position, ref_block_id)values(wname, wpos, blockId);
        if row_count()>0 then
			insert ignore into contracts(start_date, end_date, salary,ref_org_id) values(d1, d2, salary, orgId);
            -- add contract
            if row_count()>0 then
				-- check health
				insert into medcard(gender, birthday, height, weight,sugar, satur, temper) values
				(g, bday, wh, ww, sugar, satur, temper);
			else rollback;
			end if;
        else rollback;
        end if;
        
    commit;
    else rollback;
    end if;
end //
DELIMITER ;

drop procedure if exists update_supplies;
DELIMITER //
create procedure update_supplies(in workId int)
begin
	update worker_supplies set shower_time = shower_time + 10,
    water_vol = water_vol + 15, food_portions = 21, gym = gym + 6
    where ref_worker_id in (select contr_id from contracts where presentQ = 1);
end //
DELIMITER ;

drop trigger if exists check_suppl;
DELIMITER //
create trigger check_suppl before update on worker_supplies
for each row begin

	if new.ref_worker_id not in (select contr_id from contracts where presentQ = 1) then
		signal sqlstate '45000'
		set message_text = 'This worker is not present';
	end if;
	if new.shower_time < 0 then
		signal sqlstate '45000'
		set message_text = 'No shower time left';
	end if;
    
	if new.gym < 0 then
		signal sqlstate '45000'
		set message_text = 'No gym hours left';
	end if;

end //
DELIMITER ;

drop procedure if exists go_to_shower;
DELIMITER //
create procedure go_to_shower(in workId int, in mins int)
begin
	update worker_supplies set shower_time = shower_time - mins
    where ref_worker_id = workId;
end //
DELIMITER ;

drop procedure if exists go_to_gym;
DELIMITER //
create procedure go_to_gym(in workId int, in mins int)
begin
	update worker_supplies set gym = gym - mins
    where ref_worker_id = workId;
end //
DELIMITER ;

drop procedure if exists upd_all_supplies;
DELIMITER //
create procedure upd_all_supplies()
begin
	declare id int; declare done bool default false; 
    declare cur cursor for (select ref_worker_id from worker_supplies);
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    open cur;
	read_loop: loop
    fetch cur into id;
    if done then
	leave read_loop;
    end if;
    call update_supplies(id);
    end loop;
	close cur;
end //
DELIMITER ;

drop procedure if exists happy_birthday;
DELIMITER //
create procedure happy_birthday()
begin
	update worker_supplies set shower_time = shower_time + 10,
    water_vol = water_vol + 10, gym = gym + 10
	where ref_worker_id in (select card_id from medcard where right(birthday,5) = right(date(now()),5))
    and ref_worker_id in (select contr_id from contracts where presentQ = 1);
end //
DELIMITER ;

/*set global event_scheduler= on;
create event updating_supplies
on schedule every 1 week do call upd_all_supplies();

create event celebrate
on schedule every 1 day do call happy_birthday();
show events;*/
