from imessage_reader import fetch_data
from datetime import date
from dataclasses import dataclass
import gspread
import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util

#The dataclass set up for each person playing, has their name, phone number, position on the spreadsheet (for uploading), and the song they chose (not necessary depending on situation)
@dataclass
class Person:
    name: str
    num: str
    row: int
    song: str


#Formats the spotify song into a "SONG - ARTIST"
def formatSong(link: str):
    r = requests.get(link)
    page = BeautifulSoup(r.content, 'html.parser')
    artist = page.find_all(class_= "Type__TypeElement-sc-goli3j-0 hGXzYa KTLC51kEESUNYgIAqtZb")
    artist = str((artist[0])).split("\"auto\">")
    artist = str((str(artist[-1]).split("</div>"))[0])
    song = page.find_all(class_="Type__TypeElement-sc-goli3j-0 ilmalU V4vPzzVtMpFh2ZLTRD6H")
    song = str((song[0])).split("title\">")
    song = str((str(song[-1]).split("</span>"))[0])
    return song + " - " + artist


#Gets the cell to enter into the spreadsheet
def getCell(person: Person):
    day = date.today().day
    col = chr(65+day%25)
    if day > 24:
        col = "A"+col
    return col+str(person.row)



#add song to playlist, uses spotipy
def addSong(person: Person):

    username = 'gavincaulfield'
    playlist_id = '4PW0Adw2cIr2QhzpnRLflS'
    track_id = [(link.split('?'))[0]]
    token = ''
    print(track_id)
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, track_id)
    print("Added " + formatSong(link) + " for " + person.name + "\n") 

#Grabs every message from iMessage and puts them into a list
fd = fetch_data.FetchData()
messages  = fd.get_messages()


#Opens up the spreadsheet to allow updating

sa = gspread.service_account()
sh = sa.open('SPREADSHEET-NAME')
wks = sh.worksheet("Sheet1")

#List of all the people participating
X = Person("X", "+1911", 2, "")
Y = Person("Y", "+18888888888", 3, "")
#Obviously, for the sake of privacy, I removed all real names and numbers in the project

#List of every person playing
personList = [X, Y]


#Dont want to allow duplicates, so checks if song has been sent before
def keepTrackOfSong(song):
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


#The loop that will check each message
for m in messages:
    #the loop that will check each person
    for x in personList:
        #super super long if statement, but it checks 
        # (1) The phone number with current message (m) sent matches any of the players
        # (2) if that song/message was sent today
        # (3) if that message was sent by me or not (if it is sent by me, it would have a 1 in m[5], it protects from doubling -- I'm sure I could fix that, but this method works too
        if m[0] == x.num and m[2][:11].strip() == str(date.today()) and m[5] != 1 or (m[5] == 1 and x == Gavin and m[2][:11].strip() == str(date.today())): 
            # (4) Checks to see if the message sent is a spotify link, but you have to check every 'word' of the message as humans are unpredictable
            for p in m[1].split():
                if "open.spotify.com/" in p:
                    chk = False
                    print(chk)
                    for q in open('/Users/gavincaulfield/Downloads/MusicChallenge/songlist.txt'):
                        if formatSong(p) == q:
                            chk = True
                    if chk == False:
                        x.song = p
                    else:
                        print(formatSong(p) + " has already been added, " + x.name + " needs a new song")
    #the reason I have a seperate for loop at the end is because people can send multiple songs a day (i.e. they change their mind on what song they want). If you want every song added, its an easy fix
    for i in personList:
        p = i.song
        cell = getCell(i) 
        addSong(p, i)
        wks.update(cell, formatSong(p))
        keepTrackOfSong(formatSong(p))

