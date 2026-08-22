import urllib3
import json
import urllib

ottlist = ['jayamott', 'vinayagaott', 'ratchagarott', 'joshuaott']
for ott in ottlist:
    playlist = ['#EXTM3U']
    resp = urllib3.request("GET", f"https://phoenixcreations.online/ott/{ott}/channels.php")
    respjson = resp.json()

    for i in respjson[0]['channeldata']:
        stringdata = json.dumps(i, indent=4)
        channel_data = json.loads(stringdata)
        tvg_id = channel_data['chno']
        tvg_name = channel_data['channelname']
        tvg_region = channel_data['area']
        tvg_logo = urllib.parse.quote_plus(channel_data['logo'])
        playlist.append(f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-name="{tvg_name}" tvg-logo="{tvg_logo}" tvg-name="{tvg_region}",{tvg_name}')
        playlist.append(channel_data['playbackurl'])

    with open(f'{ott}.m3u', 'w', newline='', encoding="utf-8") as f:
        for lines in playlist:
            f.write(f'{lines}\n')

    print(f"{ott}: Exported!")

    f.close()
