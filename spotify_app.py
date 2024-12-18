from flask import Flask, jsonify
import spotify_analyze as spa
import json
app = Flask(__name__)


    # Defining the home page of our site
@app.route("/")  # this sets the route to this page
def home():
    # define source

    return f"<h1>LANDING PAGE</h1>"  # some basic inline html


@app.route("/topSong")  # this sets the route to this page
def top_song():

    spa.DATA_PATH = './Spotify Extended Streaming History/Streaming_History_Audio_*.json'

    years = spa.years_range

    data = spa.user_data

    end_data = []

    for year in years:
        data_filtered = spa.get_year_data(year,year,data)
        top_songs = spa.get_top_songs(data_filtered)
        album_data = spa.get_top_album(data_filtered)

        top_song_data = {
        year:{
            "top_songs":top_songs,
            "albums":album_data
        }
        
        }

        end_data.append(top_song_data)

    # final_json = json.dumps(end_data)

    return jsonify(end_data),200


if __name__ == "__main__":
    app.run()

