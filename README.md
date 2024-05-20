# Game Analysis Project By Gian-Marco Caramelli & Angelo Beleno

Objectives:  
Successfully pull data using APIs from  Steam.  
Generate and validate 10,000 Steam Ids using APIs and HTML extraction.   
Collect data to display:
1. Most popular games based user base.
2. Games genres with the most playtime.
3. Games genres with the highest user base.
4. Most popular games based on playtime.
Successfully utilises SQL in Bigquery to analyse the data collected.  
Successfully import the data analysed through Bigquery into Tableau to create insightful visualisations.

The project evolved from  3 Steam Ids and a total of 152 games to 7,000 Steam  Ids (see documentation) over 13,000 total games over 23 genres. 

The project included a pipeline that would call the Steam API, web-scrape relevant information, clean it then upload the data as a csv file. It also includes a script to generate random and valid steam ids.

Our code: Src Folder.

Once our extraction was completed and the clean data was onto a CSV file we uploaded it onto BigQuery for Data Analysis.

Our Queries and results: Src Folder -> SQL.

The data analysed in BigQuery was uploaded onto Tableau and we displayed the results in two dashboards:
Game Analysis by Playtime: https://public.tableau.com/app/profile/gian.marco.caramelli/viz/SteamGameAnalysisbyPlaytime/Dashboard32 
Game Analysis By User Base: https://public.tableau.com/app/profile/gian.marco.caramelli/viz/SteamGameAnalysisbyUsers/Dashboard2 

Overall the project successfully completed all objectives and delivered insightful visualisation from our data extraction and analysis. 

Our full Documentation on the project: https://docs.google.com/document/d/1uyJv3d-4-YOmVGQedSHJRH7YUnJfGT7mzZuFebG5-8c/edit 
