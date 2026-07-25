import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import json
import urllib3
import urllib
playlist = ["#EXTM3U"]

SECRET = "YTWGLe6t2HLwvyraOhUxAZwERzQdjF"

def decode_stream_url(encoded_url: str) -> str:
    try:
        # Generate AES key
        key = hashlib.sha256(SECRET.encode()).digest()

        # Decode Base64 payload
        data = base64.b64decode(encoded_url)

        # Extract IV and ciphertext
        iv = data[:16]
        ciphertext = data[16:]

        # Decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        return plaintext.decode("utf-8")

    except Exception as e:
        print(f"Decryption error: {e}")
        return ""

resp = urllib3.request("GET", "https://livetv.ashokadigital.net/api/.php?get_all_channels&api_key=cda11bx8aITlKsXdsfafadskljasldfjoierKLrteaadfjalM%3C")
jsonresp = resp.json()
channels = jsonresp['posts']

for i in channels:
    stringdata = json.dumps(i, indent=4)
    channel_data = json.loads(stringdata)
    epg = channel_data['channel_id']
    name = channel_data['channel_name']
    logo = channel_data['channel_image'].replace(" ","%20")
    group = channel_data['category_name']
    playlist.append(f'#EXTINF:-1 tvg-id="{epg}" tvg-chno="{epg}" tvg-name="{name}" tvg-logo="https://livetv.ashokadigital.net/upload/logo/{logo}" group-title"{group}",{epg} {name}')
    if channel_data['channel_url'] != "":
        encoded = channel_data['channel_url'].strip()

        result = decode_stream_url(encoded)

        if result:
            playlist.append(result)
        else:
            playlist.append("")
    else:
        playlist.append("")

with open('ashokadigital.m3u', 'w', newline='') as f:
    for lines in playlist:
        f.write(f'{lines}\n')

f.close()
