#imports
from helper import helper
from db_operations import db_operations

#global variables
db_ops = db_operations("playlist.db")

#functions
def startScreen():
    print("Welcome to your playlist!")
    #db_ops.create_songs_table()
    db_ops.populate_songs_table("songs.csv")

#show user menu options
def options():
    print('''Select from the following menu options: 
    1. Find songs by artist
    2. Find songs by genre
    3. Find songs by feature
    4. Load new songs
    5. Update a song
    6. Remove a song
    7. Exit''')
    return helper.get_choice([1,2,3,4,5,6,7])

#load new songs from filepath 
def load_new_songs():
    file_path = input("Please enter the file path of the file containing new songs: ").strip()
    db_ops.update_songs_table(file_path)
    print("New songs have been processed!")

#search for songs by artist
def search_by_artist():
    #get list of all artists in table
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist: ")
    artists = db_ops.single_attribute(query)

    #show all artists, create dictionary of options, and let user choose
    choices = {}
    for i in range(len(artists)):
        print(i, artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Artist =:artist 
    ORDER BY RANDOM()
    '''
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs by genre
def search_by_genre():
    #get list of genres
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    #show genres in table and create dictionary
    choices = {}
    for i in range(len(genres)):
        print(i, genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #print results
    query = '''SELECT DISTINCT name
    FROM songs
    WHERE Genre =:genre ORDER BY RANDOM()
    '''
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +="LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

#search songs table by features
def search_by_feature():
    #features we want to search by
    features = ['Danceability', 'Liveness', 'Loudness']
    choices = {}

    #show features in table and create dictionary
    choices = {}
    for i in range(len(features)):
        print(i, features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    #user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for", choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    #what order does the user want this returned in?
    print("Do you want results sorted in asc or desc order?")
    order = input("ASC or DESC: ")

    #print results
    query = "SELECT DISTINCT name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    results = db_ops.single_attribute_params(query, dictionary)
    helper.pretty_print(results)

# Update song information
def update_song():

    # get name of song to update
    song_name = input("Enter the name of the song you want to update: ").strip()

    # retrieve all the song details and store them in song details, a list of tuples.
    query = '''SELECT * FROM songs WHERE Name = ?'''
    song_details = db_ops.select_query_params(query, (song_name,))

    # check if theres anything in the list
    if len(song_details) == 0:
        print("No song found with that name.")
        return

    # take the first matching song record (hope songs r unique)
    # the first element is songID
    song = song_details[0]
    songID = song[0]

    # print from song_details
    print("Song details:")
    print(f"Song ID: {songID}")
    print(f"Name: {song[1]}")
    print(f"Artist: {song[2]}")
    print(f"Album: {song[3]}")
    print(f"Release Date: {song[4]}")
    print(f"Explicit: {song[6]}")

    # map the choices which are allowed to be modified 
    attributes = {
        1: "Name",
        2: "Artist",
        3: "Album",
        4: "releaseDate",
        5: "Explicit"
    }

    # choose what to update
    print("Which attribute would you like to update?")
    print("1. Name\n2. Artist\n3. Album\n4. Release Date\n5. Explicit")
    choice = helper.get_choice(attributes.keys()) # pass in 1-5


    # update the song
    db_ops.update_song_attribute(songID, attributes[choice])
    print("Song information has been updated successfully.")

def remove_song():
    # get name of song to update
    song_name = input("Enter the name of the song you want to remove: ").strip()

    # retrieve all the song details and store them in song details, a list of tuples.
    query = "SELECT * FROM songs WHERE Name = ?"
    song_details = db_ops.select_query_params(query, (song_name,))

    # check if theres anything in the list
    if len(song_details) == 0:
        print("No song found with that name.")
        return

    # take the first matching song record (hope songs r unique)
    # the first element is songID
    song = song_details[0]
    songID = song[0]

    # remove the song
    db_ops.remove_song(songID)


#main method
startScreen()

#program loop
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    if user_choice == 2:
        search_by_genre()
    if user_choice == 3:
        search_by_feature()
    if user_choice == 4:
        load_new_songs()
    if user_choice == 5:
        update_song()
    if user_choice == 6:
        remove_song()
    if user_choice == 7:
        print("Goodbye!")
        break

db_ops.destructor()