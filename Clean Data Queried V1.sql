#Calculated the total playtime across all genres, number of games per genere, average playtime per genre, genres with the highest and lowest playtimes.
SELECT 
Game_Genres,
count(distinct game_id) as total_games,
round(avg(Playtime_Minutes),1) as avg_playtime,
sum(Playtime_Minutes) as total_playtime,
max(Playtime_Minutes) as Max_Playtime,
min(Playtime_Minutes) as Min_Playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.V2_Game_Data_Extraction`
group by Game_Genres
order by total_playtime desc

#calculate total playtime across all games,  average playtime per game, games with the highest and lowest playtimes
SELECT
Game_Name,
round(avg(Playtime_Minutes),1) as avg_playtime,
SUM(Playtime_Minutes) AS Total_Playtime,
max(Playtime_Minutes) as Max_Playtime,
min(Playtime_Minutes) as Min_Playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.V2_Game_Data_Extraction`
GROUP BY Game_Name
ORDER BY Total_Playtime DESC

#total games and total playtime
select
count(distinct Game_id) as total_games,
sum(Playtime_Minutes) as total_Playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.V2_Game_Data_Extraction`

#simple game analysis
SELECT
Game_Name,
Game_Genres,
max(Playtime_Minutes) as Max_Playtime,
min(Playtime_Minutes) as Min_Playtime
FROM `chrome-folio-405910.Steam_Game_Analysis.V2_Game_Data_Extraction`
group by Game_Name, Game_Genres
order by 3 desc

#Segment users based on playtime behavior considering only distinct games.
SELECT
CASE
WHEN Playtime_Minutes < 600 THEN 'Casual'
WHEN Playtime_Minutes >= 600 AND Playtime_Minutes < 6000 THEN 'Moderate'
ELSE 'Heavy'
END AS UserSegment,
COUNT(DISTINCT game_Id) AS game_distribution
FROM `chrome-folio-405910.Steam_Game_Analysis.V2_Game_Data_Extraction`
GROUP BY UserSegment
