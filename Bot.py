###############################################
#   Python code written by 4b75726169736859
###############################################

import os
import time
import requests
from discordwebhook import Discord
from os.path import exists


def sendToDiscord(pseudo):
    discord = Discord(url="<YOUR_WEBHOOK_URL>")
    discord.post(embeds=[{"title": "Nouveau live Twitch de " + pseudo + " 🎥",
        "description": "🔽   Rejoint nous en cliquant sur le lien   🔽 \n[Regarder le live]( https://www.twitch.tv/" + pseudo + ")",
        "thumbnail": {"url": "https://static-cdn.jtvnw.net/previews-ttv/live_user_" + pseudo + "-1000x600.jpg"}}],
        username="Twitch", avatar_url="https://www.freepnglogos.com/uploads/logo-twitch-ios-version-png-0.png")


def Check(userNameTwitch):
    Client_ID = "<YOUR_CLIENT_ID_TWITCH>"
    Secret = "<YOUR_SECRET_TWITCH>"
    AutParams = {'client_id': Client_ID, 'client_secret': Secret, 'grant_type': 'client_credentials'}
    head = {'Client-ID': Client_ID, 'Authorization': "Bearer <YOUR_TOKEN_TWITCH>"}
    r = requests.get('https://api.twitch.tv/helix/streams?user_login=' + userNameTwitch, headers=head).json()['data']
    if r:
        r = r[0]
        if r['type'] == 'live' and r['game_name'] == '<GAME_YOU_WANT_DETECT>' and ("<WORD_YOU_WANT_DETECT_IN_LIVE_TITLE>" in r['title'].lower()):
            return r['title'], r['started_at']
        else:
            return False
    else:
        return False


def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False


if __name__ == '__main__':
    user_twitch_live = ['<USER_TWITCH_TO_WATCH>', '<USER_TWITCH_TO_WATCH>', '<USER_TWITCH_TO_WATCH>'] # You can put as many as you want
    file_log_name = "twitchListLive.txt"

    while True:
        for name in user_twitch_live:
            gameCurrent = Check(name)
            if not isinstance(gameCurrent, bool):
                if exists(file_log_name):
                    if not check_if_string_in_file(file_log_name, name + '|' + gameCurrent[1]):
                        sendToDiscord(name)
                        text_file = open(file_log_name, "a")
                        n = text_file.write(name + '|' + gameCurrent[1])
                        text_file.close()
                else:
                    sendToDiscord(name)
                    text_file = open(file_log_name, "a")
                    n = text_file.write(name + '|' + gameCurrent[1])
                    text_file.close()
            else:
                if exists(file_log_name):
                    with open(file_log_name, "r") as input:
                        with open("temp.txt", "w") as output:
                            for line in input:
                                if not line.strip("\n").startswith(name):
                                    output.write(line)
                    os.replace('temp.txt', file_log_name)
        time.sleep(5)
