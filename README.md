# iMessage to Spotify Scraper

The main purpose of this tool is to take spotify songs sent through iMessage, using the library _imessage-reader_, and add them into a playlist owned by me (or the person who changes the code for themself). However, I also implemented a spreadsheet uploader, supported by a google API, in order to keep track of who sent every song. 

Essentially all code in **main.py**

#### (1) Reason - The overall purpose behind creating this project
#### (2) Limitations - The limitations for the project
#### (3) Functionality - The implementations for the project
#### (4) Future - Where I might go with this project in the future
          
## (1) Reason

A group of friends and I occasionally like to do this sort of "song challenge" in which a prompt is sent to a group chat where every person would reply with a song that fits the prompt accurately. For example, "Day 11: A song for walking in the rain." Then, everybody would send a song to the group chat--more often than not a song that person just likes--and it is added to a playlist.

However, the, albeit minor, problem arose with the frustration of running the challenge. The person who hosts the challenge must keep track of every song each person sends (sometimes upwards of 10 people) in order to prevent duplicate songs being added. This took a lot of time. Moreover, actually adding the song to the playlist is a bit of a hassle too, which is why I set out to create this program. 

Thus, the program scans every message sent to me from certain numbers (the ones participating) and checks if it is a spotify link. If it is, it will check if its a valid link. WARNING: The program is currently set up so that it only checks the messages sent the day you run the program, but its an easy fix if it not what you want. Then, it checks if its been sent before (check for dupicates which is kept in a txt file), and if it hasn't, it will be added to a spreadsheet aligning with the day and name.
                         
## (2) Limitations

There are some unfortunate limitations for the project.

~~(1) **OAuth** - The access token for spotify expires every 60 minutes. So, if I need to run the program, more often than not I need a new OAuth code.~~

(2) **Group Chats** - imessage-reader does not really support group chats, but instead it reads every text as either sent to you or sent by you. For example, if there is a group chat where all the messages are being sent, the imessage-reader will just interpret them as if they were sent to you. This creates the possibility for an error, as if a participant of the challenge sends a song to the group chat, and one to you personally, the program will take whichever song was sent last (even if its not for the challenge).

Another group chat error: because of the lack of support for group chats from imessage-reader, it will not detect the messages that you send to a group chat as proper messages, only ones that you send to individual people. My loophole is just sending my song to the group chat and to myself.

(3) **Have to manually run** - Because of the OAuth and because I haven't set it up yet, the program will not run at a set time to perform its purpose. However, clicking run is much faster than the original process, so this is still a W in my book.

  
## (3) Functionality

Here are some overlying implementations I used in the project that is dedicated toward my use of it.

(1) **Takes last song of today** - I have it set up where it takes the **last song** sent by each person, only for the **day that the program is ran**. It's just how I need it for my use, and its a quick fix.
  
(2) **Adds to spreadsheet** - I need it to keep track of every song sent. Obviously unnecessary to the overall code, and an easy fix.

(3) **Prevents duplicates** - I can't have duplicates, so I used a txt file to keep track of every song added. Once again, quick fix.

(4) **Makefile** - Since it's in python, its unnecesary to have a Makefile, but I'm personally just a big Makefile kinda guy 😁
  
  
## (4) Future

Here are some of my ideas for the future.

~~(1) **Refresh Token** - Obviously, creating a refresh token would solve the OAuth problem, but I have pretty limited knowledge on APIs. I am very interested in creating a function to do this for me, but I do not believe I have enough time to do so before this challenge begins (Dec 1st), so I am going to put this project aside until I have the time/must fix it.~~

(2) **AWS** - Similar to the refresh token, I also plan on looking into AWS to run this program at a certain time, but the same reasons for the refresh token is why I will hold off for the time being.

(3) **App** - I am very interested in possibly marketing this into an app/addon for others to use, but that is a down the road idea. 



## Thanks
Thank you for checking out my project. If you have any comments/questions I will try to answer them.
