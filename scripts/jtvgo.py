import requests

ip = "14.96.244.82:5001"

playlist = requests.get(f"http://{ip}/playlist.m3u")

print(playlist.text)

with open('./jtv.m3u', 'w', newline='') as f:
    for lines in playlist.text:
        f.write('%s\n' %lines)
    print("Exported!")

f.close()
