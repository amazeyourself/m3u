import urllib3
import json
from datetime import datetime, date
import time
import gzip
import xml.etree.ElementTree as ET

root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself')

t = date.today()
startEpoch = int(datetime(t.year, t.month, t.day, t.hour, 0, 0).timestamp() * 1000)
endEpoch = int(datetime(t.year, t.month, t.day, t.hour+4, 0, 0).timestamp() * 1000)

resp = urllib3.request("GET",
                       "https://livetv.airtel.tv/v1/livechannel")

json = resp.json()
channellist = json['data']
for i in channellist:
    if "DISTROTV" not in i['id'] and "AAJTAK" not in i['id'] and "HOTSTAR" not in i['id'] and "RUNNTV" not in i['id']:
        if 'LOGO_HD' in i['images']:
            ico = i['images']['LOGO_HD']
        elif 'LOGO' in i['images']:
            ico = i['images']['LOGO']
        chnl = ET.SubElement(root, 'channel')
        chnl.set('id', i['id'])
        dspl = ET.SubElement(chnl, 'display-name')
        icon = ET.SubElement(chnl, 'icon')
        dspl.text = i['title']
        if 'LOGO_HD' in i['images'] or 'LOGO' in i['images']:
            icon.set('src', ico)
        lcn = ET.SubElement(chnl, 'lcn')
        if 'lcn' in i:
            lcn.text = i['lcn']
        epgid = i['id']
        print(dspl.text)
    
        resp = urllib3.request("GET",
                               f"https://epg.airtel.tv/app/v2/content/channel/epg?channelId={epgid}&startTime={startEpoch}&endTime={endEpoch}&appId=WEB")
        json = resp.json()
        programlist = json['programGuide']
        for prg in programlist[list(programlist.keys())[0]]:
            startepoch = prg['startTime'] / 1000
            start = datetime.fromtimestamp(startepoch)
            stopepoch = prg['endTime'] / 1000
            stop = datetime.fromtimestamp(stopepoch)
            prog = ET.SubElement(root, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start.strftime('%Y%m%d%H%M%S +0000'))
            prog.set('stop', stop.strftime('%Y%m%d%H%M%S +0000'))
            prog.set('catchup-id', prg['id'])
            title = prg['title']
            if 'desc' in prg:
                desc = prg['desc']
            else:
                desc = ""
            date = start.strftime("%Y%m%d")
            if 'LANDSCAPE_169_HD' in prg['images']:
                thumb = prg['images']['LANDSCAPE_169_HD']
            elif 'LANDSCAPE_169' in prg['images']:
                thumb = prg['images']['LANDSCAPE_169']
            prgtitle = ET.SubElement(prog, 'title')
            prgtitle.text = title
            prgdesc = ET.SubElement(prog, 'desc')
            prgdesc.text = desc
            prgdate = ET.SubElement(prog, 'date')
            prgdate.text = date
            prgico = ET.SubElement(prog, 'icon')
            prgico.set("src", thumb)
        

xml_data = ET.tostring(root)

with open('./epg/airtel.xml', 'wb') as f:
    f.write(xml_data)
    print("Exported!")
f.close()

with gzip.open('./epg/airtel.xml.gz', 'wb') as f:
    f.write(xml_data)
f.close()

newroot = ET.Element('tv')
newroot.set('generator-info-url', 'https://github.com/amazeyourself')

for i in channellist:
    if "RUNNTV" in i['id']:
        if 'LOGO_HD' in i['images']:
            ico = i['images']['LOGO_HD']
        elif 'LOGO' in i['images']:
            ico = i['images']['LOGO']
        chnl = ET.SubElement(newroot, 'channel')
        chnl.set('id', i['id'])
        dspl = ET.SubElement(chnl, 'display-name')
        icon = ET.SubElement(chnl, 'icon')
        dspl.text = i['title']
        icon.set('src', ico)
        lcn = ET.SubElement(chnl, 'lcn')
        if 'lcn' in i:
            lcn.text = i['lcn']
        epgid = i['id']
        print(dspl.text)
    
        resp = urllib3.request("GET",
                               f"https://epg.airtel.tv/app/v2/content/channel/epg?channelId={epgid}&startTime={startEpoch}&endTime={endEpoch}&appId=WEB")
        json = resp.json()
        programlist = json['programGuide']
        for prg in programlist[list(programlist.keys())[0]]:
            startepoch = prg['startTime'] / 1000
            start = datetime.fromtimestamp(startepoch)
            stopepoch = prg['endTime'] / 1000
            stop = datetime.fromtimestamp(stopepoch)
            prog = ET.SubElement(newroot, 'programme')
            prog.set('channel', epgid)
            prog.set('start', start.strftime('%Y%m%d%H%M%S +0000'))
            prog.set('stop', stop.strftime('%Y%m%d%H%M%S +0000'))
            prog.set('catchup-id', prg['id'])
            title = prg['title']
            if 'desc' in prg:
                desc = prg['desc']
            else:
                desc = ""
            date = start.strftime("%Y%m%d")
            if 'LANDSCAPE_169_HD' in prg['images']:
                thumb = prg['images']['LANDSCAPE_169_HD']
            elif 'LANDSCAPE_169' in prg['images']:
                thumb = prg['images']['LANDSCAPE_169']
            prgtitle = ET.SubElement(prog, 'title')
            prgtitle.text = title
            prgdesc = ET.SubElement(prog, 'desc')
            prgdesc.text = desc
            prgdate = ET.SubElement(prog, 'date')
            prgdate.text = date
            prgico = ET.SubElement(prog, 'icon')
            prgico.set("src", thumb)
        

xml_data2 = ET.tostring(newroot)

with open('./epg/runntv.xml', 'wb') as f:
    f.write(xml_data2)
    print("Exported!")
f.close()

with gzip.open('./epg/runntv.xml.gz', 'wb') as f:
    f.write(xml_data2)
f.close()
