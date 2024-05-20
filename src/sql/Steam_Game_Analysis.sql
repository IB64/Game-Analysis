#user distribution by playtime
SELECT
UserSegment,
COUNT(*) AS UserCount
FROM ( SELECT
CASE
  WHEN SUM(Playtime_Minutes) < 6000 THEN 'Casual'#Lower than 100h
  WHEN SUM(Playtime_Minutes) >= 6001 AND SUM(Playtime_Minutes) <= 18000 #Between 100h and 300h
  THEN 'Moderate'
  ELSE 'Hardcore' #Anything above 300h
  END AS UserSegment,
  user_Id
FROM `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
GROUP BY user_Id
)
GROUP BY UserSegment;


#checking how many Ids and games we got
select
count(distinct user_id),
count(distinct game_id)
from `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`


#Top games based on owenrship
SELECT
Game_Name,
count(distinct User_Id) as Total_gamers,
sum(Playtime_Minutes) as total_playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
group by Game_Name
order by total_gamers desc
limit 15


#Top genres baased on owenrship
SELECT
Game_Genres,
count(distinct User_Id) as Total_gamers,
sum(Playtime_Minutes) as total_playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
group by Game_Genres
order by total_gamers desc
limit 15


#Frequency of users top game
WITH RankedGames AS (
    SELECT
        User_Id,
        Game_Name,
        SUM(Playtime_Minutes) AS Total_Playtime,
        ROW_NUMBER() OVER(PARTITION BY User_Id ORDER BY SUM(Playtime_Minutes) DESC, User_Id) AS Rank
    FROM
        `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
    GROUP BY
        User_Id, Game_Id, Game_Name
)
SELECT
    Game_Name,
    count(game_name) as frequency
FROM
    RankedGames
WHERE
    Rank <= 1 -- Change this number to get top N games
    group by 1
    order by 2 desc;

#top 10 genres based on playtime
Select
distinct game_genres,
sum(Playtime_Minutes) as Total_Playtime
from `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
group by 1
order by 2 desc
limit 10


#top games by playtime
Select
Game_Name,
sum(Playtime_Minutes) as Total_Playtime
From `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
group by 1
order by 2 desc
Limit 15

#total games and playtime
select
count(distinct Game_Id) as total_Games,
sum(Playtime_Minutes) as Total_Playtime_Minutes
from `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`


#Frequency of top 3 games based on genre
WITH RankedGames AS (
    SELECT
        Game_Genres,
        Game_Name,
        SUM(Playtime_Minutes) AS Total_Playtime,
        ROW_NUMBER() OVER(PARTITION BY Game_Genres ORDER BY SUM(Playtime_Minutes) DESC, Game_Genres) AS Rank
    FROM
        `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
    GROUP BY
        Game_Genres, Game_Id, Game_Name
)
SELECT
    Game_Name,
    Game_Genres,
    Total_Playtime
FROM
    RankedGames
WHERE
    Rank <= 3 -- Change this number to get top N games
    order by 2, 3 desc


#selecting games, generes and valuable aggreftions
SELECT
Game_Name,
Game_Genres,
count(distinct game_id) as total_games,
count (distinct User_Id) as total_users,
round(avg(Playtime_Minutes),1) as avg_playtime,
sum(Playtime_Minutes) as total_playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.The_Ultimate_Ultimate_Big_List`
group by 1,2
order by total_playtime desc

