from configparser import ConfigParser
from email import header
from click import style
import httpx, requests, random, string, time, json
from colorama import Fore
from colorama import Style

url = "https://discord.com/api/v9/interactions"



with open("config.json", "r") as file:
    config = json.loads(file.read())

miscConfig = config["misc"]
commandsConfig = config["commands"]

headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "authorization": miscConfig["token"],
    "content-type": "application/json",
    "origin": "https://discord.com",
    "referer": "https://discord.com/channels/{}/{}".format(miscConfig["guild_id"], miscConfig["channel_id"]),
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "x-debug-options": "bugReporterEnabled",
    "x-discord-locale": "en-US",
    "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLUdCIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwMy4wLjUwNjAuMTE0IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIxMDMuMC41MDYwLjExNCIsIm9zX3ZlcnNpb24iOiIxMCIsInJlZmVycmVyIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluIjoid3d3Lmdvb2dsZS5jb20iLCJzZWFyY2hfZW5naW5lIjoiZ29vZ2xlIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vd3d3Lmdvb2dsZS5jb20vIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50Ijoid3d3Lmdvb2dsZS5jb20iLCJzZWFyY2hfZW5naW5lX2N1cnJlbnQiOiJnb29nbGUiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoxMzcwOTUsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
}

class Data():
    def __init__(self, guild_id, channel_id, message_id, application_id, session_id, component_type, custom_id):
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.application_id = application_id
        self.session_id = session_id
        self.component_type = component_type
        self.custom_id = custom_id

    def params(self):
        nonce = ''.join(random.choice(string.digits) for x in range(18))
        return {"type":3,"nonce":f"{nonce}","guild_id":f"{self.guild_id}","channel_id":f"{self.channel_id}","message_flags":0,"message_id":f"{self.message_id}","application_id":f"{self.application_id}","session_id":f"{self.session_id}","data":{"component_type":int(self.component_type),"custom_id":f"{self.custom_id}"}}


def execute(custom_id):
    resp = requests.post(url, json=Data(channel_id=miscConfig["channel_id"], guild_id=miscConfig["guild_id"], message_id=config["message_id"][custom_id], application_id=miscConfig["application_id"], session_id=miscConfig["session_id"], component_type=2, custom_id=custom_id).params(), headers=headers)
    return resp

def sendmsg(msg):
    msgUrl = f"https://discord.com/api/v9/channels/{config['misc']['channel_id']}/messages"
    nonce = ''.join(random.choice(string.digits) for x in range(18))
    resp = requests.post(msgUrl, json={"content":f"{msg}","nonce":f"{nonce}","tts":False}, headers=headers)
    return resp

def choosePlant():
    plants = ["carrot", "potato", "melon", "pumpkin", "beetroot"]
    plant = random.choice(plants)
    if plant in ["carrot"]:
        plantDelay = config["plants"]["carrot_delay"]
    if plant in ["potato"]:
        plantDelay = config["plants"]["potato_delay"]
    if plant in ['pumpkin']:
        plantDelay = config["plants"]["pumpkin_delay"]
    elif plant == "melon":
        plantDelay = config["plants"]["melon_delay"]
    elif plant == "beetroot":
        plantDelay = config["plants"]["beetroot_delay"]
    return plant, plantDelay

def getTime():
    thetime = time.localtime()
    thetime = f"{thetime.tm_year}/{thetime.tm_mon}/{thetime.tm_mday} {thetime.tm_hour}:{thetime.tm_min}:{thetime.tm_sec}"
    return f"{Fore.RESET}{thetime}"

last_fish = time.time() - config["delays"]["fish"]
last_hunt = time.time() - config["delays"]["hunt"]
last_claim = time.time() - config["delays"]["claimall"]
last_rebirth = time.time() - config["delays"]["rebirth"]
plant, plantDelay = choosePlant()
last_plant = time.time() - plantDelay
last_bonemeal = time.time() - config["plants"]["bonemeal_delay"]
last_wings = time.time() - config["delays"]["wings"]
last_rage = time.time() - config["delays"]["rage"]
last_earthquake = time.time() - config["delays"]["earthquake"]



time.sleep(2)


while True:
    try:
        if commandsConfig["rebirth"] and time.time() - last_rebirth >= config["delays"]["rebirth"]:
            print("{}<{}>\n{}Rebirth:            {}{}{}".format(Fore.RESET, getTime(), Fore.YELLOW, Style.BRIGHT, Fore.GREEN, execute("rebirth").status_code))

            last_rebirth = time.time()
            time.sleep(2)

        if commandsConfig["hunt"] and time.time() - last_hunt >= config["delays"]["hunt"]:
            print("{}<{}>\n{}Hunt:               {}{}{}".format(Fore.RESET, getTime(), Fore.LIGHTBLACK_EX, Style.BRIGHT, Fore.GREEN, execute("hunt").status_code))

            last_hunt = time.time()
            time.sleep(2)

        if commandsConfig["fish"] and time.time() - last_fish >= config["delays"]["fish"]:
            print("{}<{}>\n{}Fish:               {}{}{}".format(Fore.RESET, getTime(), Fore.BLUE, Style.BRIGHT, Fore.GREEN, execute("fish").status_code))

            last_fish = time.time()
            time.sleep(2)

        if commandsConfig["claimall"] and time.time() - last_claim >= config["delays"]["claimall"]:
            print("{}<{}>\n{}Claim All:          {}{}{}".format(Fore.RESET, getTime(), Fore.RED, Style.BRIGHT, Fore.GREEN, execute("claimall").status_code))

            last_claim = time.time()
            time.sleep(2)

        if commandsConfig["plant"] and time.time() - last_plant >= plantDelay:
            print("{}<{}>\n{}Harvest:            {}{}{}".format(Fore.RESET, getTime(), Fore.LIGHTYELLOW_EX, Style.BRIGHT, Fore.GREEN, sendmsg(f"<@518759221098053634> harvest").status_code))

            plant, plantDelay = choosePlant()
            print("{}<{}>\n{}Plant:              {}{}{} | {}".format(Fore.RESET, getTime(), Fore.LIGHTGREEN_EX, Style.BRIGHT, Fore.GREEN, sendmsg(f"<@518759221098053634> plant all {plant}").status_code, plant))

            last_plant = time.time()
            time.sleep(2)

        if commandsConfig["bonemeal"] and time.time() - last_bonemeal >= config["plants"]["bonemeal_delay"]:
            for area in config["plants"]["bonemeal_area"]:
                print("{}<{}>\n{}Bonemeal:           {}{}{} | {}".format(Fore.RESET, getTime(), Fore.LIGHTWHITE_EX, Style.BRIGHT, Fore.GREEN, sendmsg(f"<@518759221098053634> bonemeal {area}").status_code, area))

            last_bonemeal = time.time()
            time.sleep(2)

        if commandsConfig["wings"] and time.time() - last_wings >= config["delays"]["wings"]:
            print("{}<{}>\n{}Wings:              {}{}{}".format(Fore.RESET, getTime(), Fore.MAGENTA, Style.BRIGHT, Fore.GREEN, execute("wings").status_code))

            last_wings = time.time()
            time.sleep(2)

        if commandsConfig["rage"] and time.time() - last_rage >= config["delays"]["rage"]:
            print("{}<{}>\n{}Rage:          {}{}{}".format(Fore.RESET, getTime(), Fore.RED, Style.BRIGHT, Fore.GREEN, execute("rage").status_code))

            last_rage = time.time()
            time.sleep(2)

        if commandsConfig["earthquake"] and time.time() - last_earthquake >= config["delays"]["earthquake"]:
            print("{}<{}>\n{}Earthquake:              {}{}{}".format(Fore.RESET, getTime(), Fore.LIGHTGREEN_EX, Style.BRIGHT, Fore.GREEN, execute("earthquake").status_code))

            last_earthquake = time.time()
            time.sleep(2)

        if commandsConfig["sell"]:
            print("{}<{}>\n{}Sell:               {}{}{}".format(Fore.RESET, getTime(), Fore.RED, Style.BRIGHT, Fore.GREEN, execute("sell").status_code))

        slep = random.randint(config["delays"]["min_sleep"], config["delays"]["max_sleep"])
        print(f"<{getTime()}>\n{Fore.WHITE}Sleep:              {Style.BRIGHT}{Fore.WHITE}" + str(slep) + " seconds")
        time.sleep(slep)

        do = random.choice(commandsConfig["chances"])
        if do and commandsConfig["upgradePickaxeAll"]:
            print("{}<{}>\n{}Upgrade Pick:       {}{}{}".format(Fore.RESET, getTime(), Fore.YELLOW, Style.BRIGHT, Fore.GREEN, execute("upgradePickaxeAll").status_code))
        elif do == False and commandsConfig["upgradeBackpackAll"]:
            print("{}<{}>\n{}Upgrade Backpack:   {}{}{}".format(Fore.RESET, getTime(), Fore.YELLOW, Style.BRIGHT, Fore.GREEN, execute("upgradeBackpackAll").status_code))
        else:
            print("{}<{}>\n{}Nothing:            ".format(Fore.RESET, getTime(), Fore.WHITE))
            pass
        

        time.sleep(2)
    except Exception as e:
        print(e) 
        pass