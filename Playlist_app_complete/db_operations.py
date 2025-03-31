import sqlite3
from helper import helper

class db_operations():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    def select_query(self, query):
        result = self.cursor.execute(query)
        return result.fetchall()
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    def select_query_params(self, query, dictionary):
        result = self.cursor.execute(query, dictionary)
        return result.fetchall()

    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    # function that creates table songs in our database
    def create_songs_table(self):
        query = '''
        CREATE TABLE songs(
            songID VARCHAR(22) NOT NULL PRIMARY KEY,
            Name VARCHAR(20),
            Artist VARCHAR(20),
            Album VARCHAR(20),
            releaseDate DATETIME,
            Genre VARCHAR(20),
            Explicit BOOLEAN,
            Duration DOUBLE,
            Energy DOUBLE,
            Danceability DOUBLE,
            Acousticness DOUBLE,
            Liveness DOUBLE,
            Loudness DOUBLE
        );
        '''
        self.cursor.execute(query)
        print('Table Created')

    # function that returns if table has records
    def is_songs_empty(self):
        #query to get count of songs in table
        query = '''
        SELECT COUNT(*)
        FROM songs;
        '''
        #run query and return value
        result = self.single_record(query)
        return result == 0

    # function to populate songs table given some path
    # to a CSV containing records
    def populate_songs_table(self, filepath):
        if self.is_songs_empty():
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = "INSERT INTO songs VALUES("+placeholders+")"
            self.bulk_insert(query, data)
        
    # function to update songs table given some path
    # same as populate_songs_table but doesn't
    # check if songs is empty. 
    def update_songs_table(self, filepath):
        data = helper.data_cleaner(filepath)
        attribute_count = len(data[0])
        placeholders = ("?,"*attribute_count)[:-1]
        # using INSERT OR IGNORE in order to skip any insert that violates the
        # unique contraint
        # https://www.geeksforgeeks.org/sql-insert-ignore-statement/
        query = "INSERT OR IGNORE INTO songs VALUES("+placeholders+")"
        self.bulk_insert(query, data)

    # function to update specific song attribute
    def update_song_attribute(self, songID, attribute):

        # inifite loop that way it goes until we get a valid input
        while True:

            #input new value to update old attribute
            new_value = input(f"Enter the new value for {attribute}: ").strip()
            
            # validate to make sure not null
            if attribute in ["Name", "Artist", "Album"]:
                if new_value == "":
                    print("Invalid input")
                    continue

            # validate to make sure true/false
            elif attribute == "Explicit":
                if new_value.lower() not in ["true", "false"]:
                    print("Invalid input")
                    continue

            # validate its a modifiable attribute
            else:
                print("Invalid attribute specified.")
                continue

            try:
                query = f"UPDATE songs SET {attribute} = ? WHERE songID = ?"
                self.cursor.execute(query, (new_value, songID))
                self.connection.commit()
                print(f"{attribute} updated successfully.")
                break  # exit after success
            except Exception as e:
                print(f"Error updating song: {e}")

    # function to remove songs from db given songID
    def remove_song(self, songID):
        try:
            query = "DELETE FROM songs WHERE songID = ?"
            self.cursor.execute(query, (songID,))
            self.connection.commit()
            print("Song removed successfully.")
        except Exception as e:
            print(f"Error removing song: {e}")


    # destructor that closes connection with DB
    def destructor(self):
        self.cursor.close()
        self.connection.close()