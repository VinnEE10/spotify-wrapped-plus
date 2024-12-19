// global variables making accessing 
const TIMESTAMP = 'ts';
const TIME_PLAYED = 'ms_played';
const SONG_NAME = 'master_metadata_track_name';
const ARTIST_NAME = 'master_metadata_album_artist_name';
const ALBUM_NAME = 'master_metadata_album_album_name';



async function get_songs(year) {
/* Basic structure from the data request
    {
        '2024': {
          top_songs: [
            {
            count: 343,
            master_metadata_album_artist_name: 'Post Malone',
            master_metadata_track_name: 'Sign Me Up'
            },
            {
            count: 326,
            master_metadata_album_artist_name: 'Noah Kahan',
            master_metadata_track_name: 'She Calls Me Back (with Kacey Musgraves)'
            },
          ]
        }
*/

// IMPORTANT CHANGE end_point not defined yet 
    const end_point = `http://127.0.0.1:5000/year-data/${year}`
    
    const response = await fetch(end_point)
    const data = await response.json()
    const inner_data = data[`${year}`]
    const song_data = inner_data["top_songs"]

    /**
    Example on how to itterate over the data
     */
    console.log(`--------------`);
    song_data.forEach((song_data,index) => {

        console.log(`Rank: ${index+1}`);
        console.log(`   Track Name: ${song_data[SONG_NAME]}`);
        console.log(`   Count: ${song_data.count}`);
        console.log(`--------------`);


    });


    // return data
}

get_songs(2024)