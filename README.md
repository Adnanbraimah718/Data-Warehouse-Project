## **Project 3: Song Play Analysis With S3 and Redshift**
-----------------------------------------------------------------------------------------------------------------------------------

In this project we will use two Amazon Web Services, S3 (Data storage) 
and Redshift.
I will build an ETL pipeline using Python to load data from S3 to staging tables on Redshift.
Then load data from staging tables to analytics tables on Redshift.
Define fact and dimension tables for a star schema for song play analysis 

Data sources are provided by two public S3 buckets. One bucket contains 
info about songs and artists, the second has info concerning actions done 
by users.
The objects contained in both buckets are JSON files. 



## **Motivation**
-----------------------------------------------------------------------------------------------------------------------------------

A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team at Sparkify whats to know what songs users are listening to. In order to analyze songs and user activity they need to query certain data, however, the data they currently have is is JSON format.

## **Schema**
-----------------------------------------------------------------------------------------------------------------------------------

The schema will consist of four dimension tables and a fact table. The four dimension tables will be the users, songs, artists and time tables. The fact table will be the song plays table. 


### Schema for Song Play Analysis
Using the song and log datasets, you'll need to create a star schema optimized for queries on song play analysis. This includes the following tables. The columns and data for each table is listed below: 

### Fact Table
songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

users - users in the app
user_id, first_name, last_name, gender, level

songs - songs in music database
song_id, title, artist_id, year, duration

artists - artists in music database
artist_id, name, location, latitude, longitude

time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday


## **Files**
-----------------------------------------------------------------------------------------------------------------------------------

files included:


create_tables.py drops and creates your tables. You run this file to reset your tables before each time you run your ETL scripts.

etl.py reads and processes files from song_data and log_data and loads them into your tables. 

sql_queries.py contains all your sql queries, and is imported into the last three files above.

The song data contains data about a song and its artist. The log data is data generated from an event simulator.


## **Installation**
-----------------------------------------------------------------------------------------------------------------------------------


1. Run an AWS Redshift Cluster
2. Using a new terminal window the sql_queries and create_tables file should be ran first using the following commands
`python sql_queries.py`
`python create_tables.py`
`python etl.py`

*Notes:

In this example a Redshift dc2.large cluster with 4 nodes was used, (a cost of USD 0.25/hr per cluster)
Also in this example we will use IAM role authorization mechanism, with a AmazonS3ReadOnlyAccess policy 

*A new terminal must be ran for any changes made to the py files and the kernel for the ipynb files should be restarted to exit the connection
