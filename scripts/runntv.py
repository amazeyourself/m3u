import urllib3
import json
resp = urllib3.request(
    "GET",
    "https://prod-epg-sec.runn.tv/runtv/v4/schedule/getEpgByStreamingNow",
    headers={
        "Partner_code": "ALL",
        "Referer": "https://runn.tv/",
        "X-Tenant-Id": "runn",
        "Userid": "8C-EB-8C-42-E7-E2",
        "Runn-Api-Key": "pXh1VC0Asx9Wy+D7AaicqJruRZFJYulegB4SMSrvGM9G4veO0VZfpgFhR6sJkXaPAkkbIhg59Pq8vA7li0YZ"
    }
)
channeldata = resp.json()
playlist = ['#EXTM3U']
for i in channeldata:
    epgid = i['id']
    chnlname = i['title']
    stream = i['playUrl']
    imglocation = i['baseSourceLocation']
    img = imglocation + i['images']['logo']['tv']
    category = i['categories'][0]['name']
    playlist.append(f'#EXTINF:-1 tvg-id="{epgid}" tvg-name="{chnlname}" tvg-logo="{img}" group-title="{category}",{chnlname}')
    playlist.append(stream)

with open('runntv.m3u', 'w', newline='') as f:
    for lines in playlist:
        f.write(f'{lines}\n')

f.close()
