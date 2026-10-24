import urllib3
import json

playlist = ['#EXTM3U']
resp = urllib3.request("GET", "https://fastv-v2.routez.cloud/api/v2/fastv2/api/getChannelList?app=0FIpP%2BH3RDgE%2BOc5uU7cmA%3D%3D")
respjson = resp.json()

for i in respjson['channels']:
    stringdata = json.dumps(i, indent=4)
    channel_data = json.loads(stringdata)
    tvg_id = channel_data['channel_id']
    tvg_name = channel_data['channel_name']
    tvg_logo = channel_data['channel_logo']
    playlist.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}",{tvg_name}')
    playlist.append(channel_data['channel_url'])

with open('./fastvjp.m3u', 'w', newline='', encoding="utf-8") as f:
    for lines in playlist:
        f.write(f'{lines}\n')

f.close()
