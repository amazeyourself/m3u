import requests

ip = "223.25.71.211:5001"

playlist = requests.get(f"http://{ip}/playlist.m3u")

print(playlist.text)

with open('./jtv.m3u', 'w', newline='') as f:
    f.write(playlist.text)
    print("Exported!")

f.close()
