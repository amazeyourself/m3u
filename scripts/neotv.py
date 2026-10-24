import urllib3
import json

playlist = ['#EXTM3U x-tvg-url="https://raw.githubusercontent.com/amazeyourself/m3u/epg/neotv.xml.gz"','#EXTM3U x-tvg-url="https://raw.githubusercontent.com/amazeyourself/m3u/epg/olitv.xml.gz"']
test = urllib3.request("GET",
                       "https://livetv.neotvapp.com/wp-admin/admin-ajax.php?action=livetv_get_channels")

resp = test.json()
for i in resp['data']['items']:
    stringdata = json.dumps(i, indent=4)
    channel_data = json.loads(stringdata)
    if channel_data['epg'] != None:
        if ".php" not in channel_data['epg']:
            epg = channel_data['epg'].replace('https://epg.neotvapp.com/','').replace('https://test.legitpro.co.in/uploads/', '').replace('.xml','').replace('%20',' ').replace('%26', '&amp;')
        elif "oli" in channel_data['epg']:
            epg = "OLI TV"
        elif "https://api.bongo-solutions.com/roster/EpgXml?channel=bongo-movies&days=1 in channel_data['epg']":
            epg = "Bongo Movies"
    else:
        epg = ""
    chno = channel_data['sort_value']
    name = channel_data['channel_name']
    logo = channel_data['image']
    genre = channel_data['genre']
    url = channel_data['stream_url']
    playlist.append(f'#EXTINF:-1 tvg-id="{epg}" tvg-chno="{chno}" tvg-name="{name}" tvg-logo="{logo}" group-title="{genre}",{name}')
    playlist.append(url)

with open('./neotv.m3u', 'w', newline='') as f:
    for lines in playlist:
        f.write(f'{lines}\n')

f.close()
