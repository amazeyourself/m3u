import requests

ip = "http://103.82.157.88:5001/"

playlist = requests.get(f"http://{ip}/playlist.m3u")

print(playlist.text)

with open('./jtv.m3u', 'w', newline='') as f:
    f.write(playlist.text)
    print("Exported!")

f.close()
