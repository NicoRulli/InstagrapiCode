# Started on April 12th, 2023
# Packages
from instagrapi import Client
import time
import os
import datetime 
from instagrapi.exceptions import LoginRequired
import logging

credentialsPath = "/Users/Shared/InstagramAutomated/credentials.txt"

with open(credentialsPath, "r") as f:
    USERNAME, PASSWORD = f.read().splitlines()

cl = Client()
logger = logging.getLogger()

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    session = cl.load_settings("session.json")

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")


login_user()

start = time.time()
print("Code is running and being timed. Please wait....")

file_path = '/Users/Shared/InstagramAutomated/runFile.txt'
x = datetime.datetime.now()
with open(file_path, 'w') as file:
    content = f"File ran at {x}"
    file.write(content)
file.close()

usernames = [
    "hannesribbner",
    "teamlyonfish",
    "captnickstanczyk",
    "ariatunafishing",
    "fv_whiskeybusiness",
    "highlymigratoryfishing",
    "joevt_fishing",
    "reeladdictioniiisportfishing",
    "almcglashan",
    "dennis_verreet",
    "david_lassley",
    "high_seas_hawaii",
    "bhagz_fishing",

]
print('Successful Login')

ids = []
id_dict = {}


PKDict = {}
PKList = []
max_likes = 0

primaryKeysInFile = []

def create_user_id_list(usernames):
    for i in usernames:
        ids.append(cl.user_id_from_username(i))

def create_user_id_dict(usernames):
    for i in range(len(usernames)):
        id_dict[usernames[i]] = ids[i]

def collect_like_count():
    media = []
    for i in ids:
        media += cl.user_medias(i, 9)
        for i in range(len(media)):
            media_dict = media[i].dict()
            likeCount = media_dict['like_count']
            PKDict[media_dict['pk']] = likeCount
    

def most_liked_PK():
    max_likes = 0
    
    # print('Collecting max likes...')
    for i,v in PKDict.items():
        if v > max_likes:
            max_likes = v
    
    mostLikedPK = 0
    for i,v in PKDict.items():
        if max_likes == v:
            mostLikedPK = i
    
    return mostLikedPK

primaryKeyPath = "/Users/Shared/InstagramAutomated/primarykeys.txt"

def prevent_repost(mostLikedPK):
    with open(primaryKeyPath, "r") as f:
        primaryKeysInFile = f.read().splitlines()
    
    sorted_dict = {k: v for k, v in sorted(PKDict.items(), key=lambda item: item[1])}

    newDict = {}
    for i,v in sorted_dict.items():
        if i not in primaryKeysInFile:
            newDict[i] = v
    
    sorted_dict = {k: v for k, v in sorted(newDict.items(), key=lambda item: item[1])}

    mostLikedPK = list(newDict)[-1]

    with open(primaryKeyPath, "a") as f:
        f.write(str(mostLikedPK))
        f.write('\n')
        f.close()

    return mostLikedPK

create_user_id_list(usernames)
print('1')
create_user_id_dict(usernames)
print('2')
collect_like_count()
print('3')
Mlpk = most_liked_PK()
print('4')
Mlpk = prevent_repost(Mlpk)
print('5')


media_type = cl.media_info(Mlpk).dict()['media_type']

product_type = cl.media_info(Mlpk).dict()['product_type']

m = cl.media_info(Mlpk)

url = m.video_url

downloadPath = "/Users/Shared/InstagramAutomated/downloadedPosts"

print("media type: " + str(media_type))
print("Attempting to download...")
p = ''
files = os.listdir(downloadPath)

if media_type == 1:                                  #picture
    cl.photo_download(Mlpk, downloadPath)
    

if media_type == 2 and product_type == 'clips':
    p = cl.clip_download(Mlpk,downloadPath)          #Reel

if media_type == 2 and product_type == 'feed':       #Video
    # cl.video_download(MLPK, downloadPath)
    p = cl.video_download_by_url(m.video_url)

if media_type == 2 and product_type == 'igtv':       #IGTV
    # cl.igtv_download(MLPK,downloadPath)
    p = cl.igtv_download_by_url(m.video_url)

if media_type == 8:                                  #Album
    # cl.album_download(MLPK, downloadPath)
    p = downloadPath + '/' + files[1]
    cl.album_download(Mlpk,downloadPath)


poster = "@" + str(cl.media_user(Mlpk).dict()['username'])
location = cl.media_info(Mlpk).dict()['location']

if location != None:
    location = str(location['name'])
    caption = "Check out this post by " + poster + " out near " + location + "! \nTag your Friends and comment below! \n . \n . \n . \n . \n . \n . \n . \n . \n #billfish #bluemarlin #sailfish #centerconsole #simrad #furuno #sailfishing #fishing #gamefish #sportfishing #pelagicgirl #pelagicworldwide #fishingteam #tuna #bluefin #jigging #trolling #offshore #swordfish #panamafishing #spearfishing #bahamasfishing #catchandcook #saltlife #catchoftheday #pescasub #floridawildlife #floridakeys"

else:
    caption = f"Check out this post by {poster}! \nTag your Friends and comment below! \n . \n . \n . \n . \n . \n . \n . \n . \n #billfish #bluemarlin #sailfish #centerconsole #simrad #furuno #sailfishing #fishing #gamefish #sportfishing #pelagicgirl #pelagicworldwide #fishingteam #tuna #bluefin #jigging #trolling #offshore #swordfish #panamafishing #spearfishing #bahamasfishing #catchandcook #saltlife #catchoftheday #pescasub #floridawildlife #floridakeys"


print()
print("Attempting to Upload...")

if media_type == 1:                                  #picture
    p = downloadPath + '/' + files[1]
    print('pic',p)
    cl.photo_upload(p, caption)

if media_type == 2 and product_type == 'clips':      #Reel
    print('****clip****', p)
    cl.clip_upload(p, caption)

if media_type == 2 and product_type == 'feed':       #Video 
    print('video', p)
    cl.video_upload(p, caption)

if media_type == 2 and product_type == 'igtv':       #IGTV
    print('igtv', p)
    cl.igtv_upload(p, caption)
    
if media_type == 8:                                  #Album
    print('album',p)
    cl.album_upload(p, caption)

os.remove(p)

print("File Deleted")

cl.logout()
end = time.time()
t = end - start
print(f"Ran in: {t.__round__(2)} seconds")