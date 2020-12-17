#sets the average of all of the liked songs by a user for a specific mood
drop procedure if exists spAverage;
delimiter //
create procedure spAverage(spUser int, spMood int)
begin
	if ((select count(*) from databaseModels_idealsongs where userID_id = spUser AND moodID_id = spMood) = 0) then
		insert into databaseModels_idealsongs (userID_id, moodID_id,
				acousticness, danceability, energy, instrumentalness, liveness, `mode`, speechiness, tempo, valence, duration, songKey, explicit, loudness, popularity, `year`, timeSignature) 
			values (spUser, spMood, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
	end if;
    
	update databaseModels_idealsongs
		set
			acousticness = (select avg(acousticness) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			danceability = (select avg(danceability) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			energy = (select avg(energy) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			instrumentalness = (select avg(instrumentalness) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			liveness = (select avg(liveness) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			`mode` = (select avg(`mode`) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			speechiness = (select avg(speechiness) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			tempo = (select avg(tempo) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			valence = (select avg(valence) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			duration = (select avg(duration) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			songKey = (select avg(songKey) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			explicit = (select avg(explicit) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			loudness = (select avg(loudness) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			popularity = (select avg(popularity) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood),
			`year` = (select avg(`year`) from databaseModels_likedsongs inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id where userID_id = spUser AND moodID_id = spMood)
		where userID_id = spUser AND moodID_id = spMood;
        
	#select avg(acousticness), avg(danceability), avg(energy), avg(instrumentalness), avg(liveness), avg(`mode`), avg(speechiness), avg(tempo), avg(valence) from databaseModels_likedsongs
	#	inner join databaseModels_songs on databaseModels_likedsongs.songID_id = databaseModels_songs.id
	#	where userID_id = spUser AND moodID_id = spMood;
end //
delimiter ;

#loops through all users;
drop procedure if exists spUserLoop;
delimiter //
create procedure spUserLoop()
begin
	declare userID int;
    declare userDone int default false;
    
    declare userCursor cursor for select id from auth_user;
    declare continue handler for not found set userDone = true;
    
    open userCursor;
    
    userLoop: loop
		fetch userCursor into userID;
        
        if userDone then
			leave userLoop;
		end if;
        
        call spMoodLoop(userID);
	end loop;
end //
delimiter ;

#loops through all moods that a user has liked a song for
drop procedure if exists spMoodLoop;
delimiter //
create procedure spMoodLoop(spUserID int)
begin
	declare moodID int;
    declare moodDone int default false;
    
    declare moodCursor cursor for select id from databaseModels_moods;
    declare continue handler for not found set moodDone = true;
    
    open moodCursor;
    
    moodLoop: loop
		fetch moodCursor into moodID;
        
        if moodDone then
			leave moodLoop;
		end if;
        
        if ((select count(*) from databaseModels_likedsongs where userID_id = spUserID AND moodID_id = moodID) > 0) then
			call spAverage(spUserID, moodID);
		end if;
	end loop;
end //
delimiter ;

//starts the process of calculating the average for all users and moods
drop procedure if exists spSetAverageLoop;
delimiter //
create procedure spSetAverageLoop()
begin
	call spUserLoop();    
end //
delimiter ;