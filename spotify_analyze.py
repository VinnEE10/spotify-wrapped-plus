#-------IMPORTANT-----------

import pandas as pd
import glob,json

# Specific to Mine
DATA_PATH = './Spotify Extended Streaming History/Streaming_History_Audio_*.json'

# data names made to constants to refer to easier
TIMESTAMP = 'ts'
TIME_PLAYED = 'ms_played'
SONG_NAME = 'master_metadata_track_name'
ARTIST_NAME = 'master_metadata_album_artist_name'
ALBUM_NAME = 'master_metadata_album_album_name'


#---------Data Cleaning/Manipulation-------------
json_files = glob.glob(f"{DATA_PATH}") 

json_files
# merge data
master_data = pd.DataFrame()

temp_data_hold = []

for file in json_files:
    data = pd.read_json(file)
    temp_data_hold.append(data)

master_data = pd.concat(temp_data_hold)
# merge data


# Standardize time
master_data[f'{TIMESTAMP}'] = pd.to_datetime(master_data[f'{TIMESTAMP}'])



user_data = master_data

# Based on the data get the years thats needed
years_range = master_data[f'{TIMESTAMP}'].dt.year.unique().tolist()
years_range.sort()




#---------Helper Function-----------
def get_top_album(data_set):
    top_albums_out = data_set[ALBUM_NAME].value_counts()[:10].to_string(header = True)
    top_albums = data_set[[ALBUM_NAME,ARTIST_NAME]].value_counts().reset_index()[:10]
    top_albums_dict = top_albums.to_dict(orient='records')

    dict_structure = {}
    



    # Here within the album add the top listened songs
    final_dict = []
    for albums in top_albums_dict:
        album_name  = albums.get(ALBUM_NAME)
        artist_name = albums.get(ARTIST_NAME)
        count = albums.get('count')
        filter_by_album =data_set[ALBUM_NAME]==f'{album_name}'
        most_listend_song = data_set[filter_by_album]
        # Top 3 Most listened Songs
        most_listend_song = most_listend_song[SONG_NAME].value_counts().reset_index()[:3]
        most_listend_song_dict = most_listend_song.to_dict(orient='records')

        dict_structure = {
            ALBUM_NAME:album_name,
            ARTIST_NAME:artist_name,
            "count":count,
            "top_songs":most_listend_song_dict,
        }

        most_listend_song_dict = most_listend_song_dict[:]
        dict_structure.update(albums)
        # dict_structure.update({"top_songs":most_listend_song_dict[:]})
        # albums.update(most_listend_song_dict[:])

        final_dict.append(dict_structure)


        # print(dict_structure)

    # print(top_albums_out)
    return final_dict



def get_year_data(year_min,year_max,data_set):
    # Filter for a specific year and month
    filtered_data = data_set[(data_set[TIMESTAMP].dt.year >= year_min) & (data_set[TIMESTAMP].dt.year <= year_max)]
    # print(filtered_data)
    return filtered_data

    

def get_top_songs(data_set):

    top_songs = data_set[[SONG_NAME,ARTIST_NAME]].value_counts()[0:10].reset_index()
    top_songs_dict = top_songs.to_dict(orient='records')[:10]

    # Returns a dictionart
    return top_songs_dict

    # Returns a json
    # return json.dumps(json_top_songs)



def get_top_songs_daytime(data_set,):
    '''
    Filters by different times of the day which songs are listend to the most
    '''

    # These are the hours of 8am-5pm filterd
    day_time_songs = data_set[(data_set[TIMESTAMP].dt.hour >= 8) & (data_set[TIMESTAMP].dt.hour <= 17 )]
    
    day_top_songs = get_top_songs(day_time_songs)


    return day_top_songs



def report_albums(list_albums,data_set):
    # Get Top Songs in an album
    for names in list_albums:
            print('-----------------')
            artist_name = data_set.loc[data_set[ALBUM_NAME] == names, ARTIST_NAME].iloc[0]
            print(f'Album: {names} | Arist: {artist_name}')
            print(f'|Top Songs|')
            filter_by_album =data_set[ALBUM_NAME]==f'{names}'

        # test_set[filter]
            most_listend_song = data_set[filter_by_album]
            most_listend_song = most_listend_song[SONG_NAME].value_counts()[:3].to_string(header=False)

            print(most_listend_song)
            print('-----------------\n')

    return


def json_out(list_dict,year):
    """ Structures the dictionaries to readable json"""
    top_songs_dict = list_dict[0]

    json_structure = {
    "year": year,
    "top_songs":top_songs_dict
    
    }


    final_json = json.dumps(json_structure)


    return final_json




#---------DATA RESPONSE/CLEANish JSON-----------

#DEV#
year = 2024
#DEV#

curr_data = get_year_data(year,year, user_data)
top_songs = get_top_songs(curr_data)

input_list = [top_songs]

final_json = json_out(input_list, year)

# print(final_json)

