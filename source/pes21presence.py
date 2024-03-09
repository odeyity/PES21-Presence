import json
import time
import os
import pypresence
from pypresence import Presence
import psutil

client_id = "1034589205545889853"
RPC = Presence(client_id, pipe=0)

special_t = ""

home_team = "Unknown Home"
away_team = "Unknown Away"

# Define modules folder path
if os.path.exists("SiderAddons") == True:
    modules_folder = "SiderAddons/modules/"
else:
    modules_folder = "modules/"

# Settings init
settings = modules_folder + "PES21-Presence/settings.json"
try:
    settingsR = open(settings, "r")
except FileNotFoundError:
    open(settings, "x")
    settingsW = open(settings, "w")
    settingsW.write("{}")
    settingsW.close()

if settingsR.read() != "{}" or settingsR.read() != "{":
    settingsW = open(settings, "w")
    settingsW.write("{}")
    settingsW.close()
settingsR = open(settings, "r")
settingsJ = json.load(settingsR)

# Define log file path
logFile = modules_folder + "PES21-Presence/log.txt"

# Clear log on start

try:
    logWrite = open(logFile, "w")
except FileNotFoundError:
    open(logFile, "x")
    logWrite = open(logFile, "w")
logWrite.write("")
logWrite.close()

# Define log function
def log(msg):
    logWrite = open(logFile, "a")
    logWrite.write(str(msg) + "\n")
    logWrite.close()
    

while True:
    try:
        RPC.connect()
        break
    except pypresence.exceptions.DiscordNotFound:
        log("Error: Discord not running")
        print("Discord not running.")
        print("Waiting for Discord..")
        time.sleep(10)

comp_id = None
comp_t = ""

leg_t = ""
state_t = "Main menu"
details_t = "Currently in the menus"
info = modules_folder + "PES21-Presence/info/matchinfo.txt"
score = modules_folder + "PES21-Presence/info/matchscore.txt"
stateP = modules_folder + "PES21-Presence/info/matchstate.txt"

home_score = "0"
away_score = "0"


patch_c = modules_folder + "PES21-Presence/database/comps.json"
patch_t = modules_folder + "PES21-Presence/database/teams.json"

try:
    compR = open(patch_c, "r", encoding="utf8")
    compJ = json.load(compR)
except FileNotFoundError:
    error = "Error: Install comps.json from the GitHub (https://github.com/odeyity/PES21-Presence) into the modules/PES21-Presence/database folder"
    print(error)
    log(error)

try:
    teamR = open(patch_t, "r", encoding="utf8")
    teamJ = json.load(teamR)
except FileNotFoundError:
    error = "Error: Install teams.json from the Github (https://github.com/odeyity/PES21-Presence) into the modules/PES21-Presence/database folder"
    print(error)
    log(error)


while True:
    state = open(stateP, "r").read()
    infoR = open(info, "r")
    infoL = infoR.readlines()
    for x in range(len(infoL)):
        line = infoL[x]
        if "comp" in line:
            comp_id = line.split(": ", -1)[1].strip()
        if "hometeam" in line:
            hometeam_id = line.split(": ", -1)[1].strip()
        if "awayteam" in line:
            awayteam_id = line.split(": ", -1)[1].strip()
        if "leg" in line:
            leg = line.split(": ", -1)[1].strip()
            if leg == "1":
                leg_t = " (1st leg)"
            elif leg == "2":
                leg_t = " (2nd leg)"
            else:
                leg_t = ""
        if "special" in line:
            special_id = line.split(": ", -1)[1].strip()
            if special_id == "46":
                special_t = " - R. of 32"
            elif special_id == "47":
                special_t = "- R. of 16"
            elif special_id == "51":
                special_t = "- Quarter Finals"
            elif special_id == "52":
                special_t = "- Semi Finals"
            elif special_id == "53":
                special_t = "- Final"
            else:
                special_t = ""
        if "scoreboard" in line:
            if comp_id == "65535":
                comp_id = line.split(": ", -1)[1].strip()
            try:
                comp_t = compJ[comp_id]
            except KeyError:
                comp_t = "Friendly"
    
    scoreR = open(score, "r")
    scoreL = scoreR.readlines()
    for x in range(len(scoreL)):
        line = scoreL[x]
        if "homescore" in line:
            home_score = line.split(": ", -1)[1].strip()
        if "awayscore" in line:
            away_score = line.split(": ", -1)[1].strip()
    
    infoR.close()
    scoreR.close()
    
    if state == "game" or state == "training":
        try:
            home_team = teamJ[str(hometeam_id)]
        except KeyError:
            print("Error: Home team is unknown!")
            home_team = "Unknown Home"
    
        try:
            away_team = teamJ[str(awayteam_id)]
        except KeyError:
            print("Error: Away team is unknown!")
            away_team = "Unknown Away"

    if state == "game":
        state_t = comp_t + special_t + leg_t
        details_t = home_team + " " + home_score + "-" + away_score + " " + away_team
    elif state == "menu" or state == "":
        state_t = "Main menu"
        details_t = "Currently in the menus"
    elif state == "ml":
        state_t = "Master League"
        details_t = "Currently in the menus"
    elif state == "training":
        state_t = "Training"
        details_t = "Playing as " + home_team
    print(details_t)
    print(state_t)

    RPC.update(large_image="large", details=details_t, state=state_t)

    if "FL_" in (i.name() for i in psutil.process_iter()) == False and "PES2021.exe" in (i.name() for i in psutil.process_iter()) == False:
        break
    time.sleep(40)
RPC.close()
