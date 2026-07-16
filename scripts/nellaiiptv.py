import json
import urllib3
f = urllib3.request("GET", "https://api.nellaiiptv.com/public/api/channels?limit=-1",
                    headers={
                        "X-Api-Key": "xkey_for_local_dev_only_12345",
                        "X-Client-Platform": "web",
                        "X-Device-Id": "6ea24383-9c2b-4b34-9c8a-1ccc4a744bc9"
                        })
data = f.json()
print(data)
playlist = []
playlist.append("#EXTM3U")
for i in data['data']:
    stringdata = json.dumps(i, indent=4)
    channel_data = json.loads(stringdata)
    chno = channel_data['channel_number']
    epg = channel_data['id']
    name = channel_data['name']
    logo = channel_data['logo_url']
    if channel_data['category'] != None:
        category = channel_data['category']['name']
    else:
        category = ""
    hls = channel_data['hls_url']
    if channel_data['rtmp_url'] != None or channel_data['rtmp_url'] != "null":
        rtmp = channel_data['rtmp_url']
    else:
        rtmp = ""
    playlist.append(f'#EXTINF:-1 tvg-chno="{chno}" tvg-id="{epg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{chno} {name}')
    playlist.append(hls)
    if channel_data['rtmp_url'] != None or channel_data['rtmp_url'] != "null" or channel_data['rtmp_url'] != "":
        playlist.append(f'#EXTINF:-1 tvg-chno="{chno}" tvg-id="{epg}" tvg-name="{name}" tvg-logo="{logo}" group-title="{category}",{chno} {name} [RTMP]')
        playlist.append(rtmp)
f.close()

with open('./nellaiiptv.m3u', 'w', newline='') as g:
    for lines in playlist:
        g.write('%s\n' %lines)
    print("Exported!")
