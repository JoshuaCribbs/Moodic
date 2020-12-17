#creates an event that runs spSetAverageLoop every morning at 3:30
drop event if exists testEvent;
create event testEvent
	on schedule 
		#at '00:03:30'
        every 1 day
        starts '2020-12-03 08:30:00'
    DO
		call spSetAverageLoop();
 
#creates a trigger that runs spSetAverageLoop every time a user likes a song 
drop trigger if exists averageTrigger;
delimiter //
create trigger averageTrigger after insert on databaseModels_likedsongs
	for each row
		begin
			call spAverage(new.userID_id, new.moodID_id);
			#call spSetAverageLoop();
		end //
delimiter ;