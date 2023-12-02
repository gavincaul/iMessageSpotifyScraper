import os
from imessage_reader import fetch_data
from datetime import date
from dataclasses import dataclass
import gspread
import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from datetime import timedelta
#The dataclass set up for each person playing, has their name, phone number and position on the spreadsheet (for uploading)
@dataclass
class Person:
    name: str
    num: str
    row: int
    song: [str]
    msg: tuple


print("\n")
#Formats the spotify song into a "SONG - ARTIST"
def formatSong(link):
    try:
        r = requests.get(link)

        page = BeautifulSoup(r.content, 'html.parser')
        title = page.title.get_text().split('-')[0]
        artist = page.find('meta', property='og:description')['content'].split(' · ')[0]
        if not title or not artist:
            print(f"Error receiving song and artist for {link}")
            return None
        return (f"{title}- {artist}").replace("&amp;", "&")
    except Exception as e:
        print(f"Unexpected error: {e}")

#Gets the cell to enter into the spreadsheet
def getCell(person: Person):
    day = date.today().day
    col = chr(65+day%25)
    if day > 24:
        col = "A"+col
    return col+str(person.row)

CLIENT_ID = os.environ.get('SP_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SP_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('SP_REDIRECT_URI')
USERNAME = os.environ.get('SP_USERNAME')
SCOPE = 'playlist-modify-public'


def getToken():
    try:
        sp_oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE, username=USERNAME)
        token_info = sp_oauth.get_cached_token()
        
        if token_info and sp_oauth.is_token_expired(token_info):
            refresh_token = token_info["refresh_token"]
            new_token_info = sp_oauth.refresh_access_token(refresh_token)
            return new_token_info["access_token"]
        
        return sp_oauth.get_access_token(code=None, as_dict=False)
    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"Error with spotipy OAuth: {e}")
        return None


TOKEN = getToken()

#add song to playlist
def addSong(person: Person):
    try:
        playlist_id = '4hTY6FrGjAl26aw9QzrUzM'
        track_id = person.song.split('?')
        track_id = [track_id[0].split('track/')[1]] 
        token = TOKEN
        
        if token is None:
            print("Error: Access token is not available.")
            return
        
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(USERNAME, playlist_id, track_id)
        # Check if the request was successful
        if 'snapshot_id' in results:
            print(f"Added {formatSong(person.song)} for {person.name}\n")
        else:
            print("Error: Unable to add song to the playlist.")

    except spotipy.oauth2.SpotifyOauthError as e:
        print(f"Error refreshing access token: {e}")
    except spotipy.SpotifyException as e:
        print(f"Error adding song to playlist: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


#Grabs every message from iMessage and puts them into a list
fd = fetch_data.FetchData()
messages  = fd.get_messages()


#Opens up the spreadsheet to allow updating

try:
    sa = gspread.service_account()
    sh = sa.open('Music Challenge')
    wks = sh.worksheet("2023")
except gspread.exceptions.GSpreadException as e:
    print(f"An error occured while working with the Google Sheets: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")



#List of all the people participating
X = Person("X", "+18888888888", 2, [""], ())
Y = Person("Y", "+19999999999", 3, [""], ())

#Obviously for privacy reasons, I won't share the real numbers, but feel free to replace

#List of every person playing
personList = [X, Y]
person_dict = {person.num: person for person in personList}
def keepTrackOfSong(song):
    if song == None:
        return
    with open('songlist.txt', "a+") as file_object:
       
        file_object.seek(0)
        
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(song)

#Reminder on the indexes for each message
SENDER_NUMBER_INDEX      = 0
MESSAGE_INDEX            = 1
DATE_INDEX               = 2
MESSAGE_TYPE_INDEX       = 3
YOUR_NUMBER_INDEX        = 4
WHO_SENT_THIS_TEXT_INDEX = 5

def removeOldDates(arr):
    newarr = []
    for x in arr:
        if str(x[2][:11]).strip() == str(date.today()) and x[1] != None:
            
            if "open.spotify.com/" in x[1]:
                z = x[1].split()

                for y in z:
                    if "open.spotify.com/" in y and "…" not in y:
                        newarr.append(x)
    return newarr
messages = removeOldDates(messages)

#The loop that will check each message
for m in messages:

    #the loop that will check each person
    if m[0] in person_dict:
        x = person_dict[m[0]]

        # (1) The phone number with current message (m) sent matches any of the players
        # (2) if that message was sent by me or not (if it is sent by me, it would have a 1 in m[5], it protects from doubling -- I'm sure I could fix that, but this method works too 

        
        if m[0] == x.num:

            
            # (4) Checks to see if the message sent is a spotify link, but you have to check every 'word' of the message as humans are unpredictable
       
            for p in m[1].split():
      
                if "open.spotify.com/" in p and "…" not in p:
                    chk = False
     
                    song = formatSong(p)
                    if song == None:
                        continue
                    with open('songlist.txt') as f:

                        if song in f.read():
                            chk = True

                    if chk == False:
                        if x.msg == ():
                            x.song = p

                        elif x.msg[2] < m[2]:
                            x.song = p

                    else:
                        print(song + " has already been added, " + x.name + " needs a new song")
for i in personList:
    if i.song != [""]:
        p = i.song
        cell = getCell(i)
        addSong(i)
        wks.update(cell, formatSong(p))
        keepTrackOfSong(formatSong(p))

