import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(
                                event_id INT IDENTITY(0,1) PRIMARY KEY,
                                artist_name VARCHAR,
                                auth VARCHAR,
                                user_first_name VARCHAR,
                                user_gender  VARCHAR,
                                item_in_session	INTEGER,
                                user_last_name VARCHAR,
                                song_length	DOUBLE PRECISION, 
                                user_level VARCHAR,
                                location VARCHAR,
                                method VARCHAR,
                                page VARCHAR,
                                registration VARCHAR,
                                session_id BIGINT,
                                song_title VARCHAR,
                                status INTEGER,  
                                ts VARCHAR,
                                user_agent TEXT,
                                user_id VARCHAR
                                )
""")

staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
                                song_id VARCHAR PRIMARY KEY,
                                num_songs INTEGER,
                                artist_id VARCHAR,
                                artist_latitude DOUBLE PRECISION,
                                artist_longitude DOUBLE PRECISION,
                                artist_location VARCHAR,
                                artist_name VARCHAR,
                                title VARCHAR,
                                duration DOUBLE PRECISION,
                                year INTEGER
                                )
""")

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplay(
                            songplay_id INT IDENTITY(0,1) PRIMARY KEY,  
                            start_time timestamp NOT NULL, 
                            user_id int NOT NULL, 
                            level varchar NOT NULL, 
                            song_id varchar, 
                            artist_id varchar, 
                            session_id int, 
                            location varchar, 
                            user_agent varchar
                                
                                )
                                
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users (
                        user_id int PRIMARY KEY,
                        first_name varchar, 
                        last_name varchar,
                        gender varchar,
                        level varchar NOT NULL
                                
                                )
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs (
                        song_id int PRIMARY KEY, 
                        title varchar, 
                        artist_id int, 
                        year int, 
                        duration float8
                                
                                )
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists (
                            artist_id varchar PRIMARY KEY, 
                            name varchar, 
                            location varchar, 
                            latitude float, 
                            longitude float
                                
                                )
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
                        start_time timestamp PRIMARY KEY, 
                        hour int, 
                        day int, 
                        week int, 
                        month int, 
                        year int, 
                        weekday int
                                
                                )
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from {}
    CREDENTIALS 'aws_iam_role={}'
    region 'us-west-2'
    COMPUPDATE OFF
    JSON {}""").format(config.get('S3','LOG_DATA'),
                        config.get('IAM_ROLE', 'ARN'),
                        config.get('S3','LOG_JSONPATH')
                        
)


staging_songs_copy = ("""copy staging_songs from {}
    CREDENTIALS 'aws_iam_role={}'
    region 'us-west-2'
    COMPUPDATE OFF 
    JSON 'auto'
    """).format(config.get('S3','SONG_DATA'), 
                config.get('IAM_ROLE', 'ARN')
)

# FINAL TABLES

songplay_table_insert = ("""INSERT INTO songplays (
                                songplay_id, 
                                start_time, 
                                user_id,
                                level, 
                                song_id, 
                                artist_id, 
                                session_id, 
                                location, 
                                user_agent
                                )
                                FROM staging_events e, staging_songs s
                                WHERE e.page = 'NextSong'
                                AND e.song_title = s.title
                                AND user_id NOT IN (SELECT DISTINCT s.user_id FROM songplays s WHERE s.user_id = user_id
                                AND s.start_time = start_time AND s.session_id = session_id 
                                ) 
""")

user_table_insert = ("""INSERT INTO users (
                            user_id, 
                            first_name, 
                            last_name, 
                            gender, 
                            level
                            )
                            FROM staging_events
                            WHERE page = 'NextSong'
                            AND user_id NOT IN (SELECT DISTINCT user_id FROM users
                            ) 
""")

song_table_insert = ("""INSERT INTO songs (
                            song_id, 
                            title, 
                            artist_id, 
                            year, 
                            duration
                            )
                            FROM staging_songs
                            WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs
                            ) 
""")

artist_table_insert = ("""INSERT INTO artists (
                            artist_id, 
                            name, 
                            location, 
                            latitude, 
                            longitude
                            )
                            FROM staging_songs
                            WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists
                            ) 
""")

time_table_insert = ("""INSERT INTO time (
                            start_time, 
                            hour, 
                            day, 
                            week, 
                            month, 
                            year, 
                            weekday
                            )
                            FROM staging_events s     
                            WHERE start_time NOT IN (SELECT DISTINCT start_time FROM time
                            )                   
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
