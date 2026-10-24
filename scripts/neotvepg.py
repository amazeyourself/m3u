import urllib3
import urllib
import json
import xml.etree.ElementTree as ET
import pathlib
import html
from lxml import etree
import gzip

test = urllib3.request("GET",
                       "https://livetv.neotvapp.com/wp-admin/admin-ajax.php?action=livetv_get_channels")

resp = test.json()
root = ET.Element('tv')
root.set('generator-info-url', 'https://github.com/amazeyourself/m3u')
epgs = []
titles = []
logos = []
for i in resp['data']['items']:
    stringdata = json.dumps(i, indent=4)
    channel_data = json.loads(stringdata)
    if channel_data['epg'] != None:
        if ".php" not in channel_data['epg']:
            epg = channel_data['epg']
        elif "oli" in channel_data['epg']:
            epg = channel_data['epg']
        else:
            epg = ""
    else:
        epg = ""
    epgs.append(epg)
    chno = channel_data['sort_value']
    name = channel_data['channel_name']
    titles.append(name)
    logo = channel_data['image']
    logos.append(logo)
    genre = channel_data['genre']
for i in epgs:
    if ".php" not in i:
        epgid = i.replace('https://epg.neotvapp.com/','').replace('https://test.legitpro.co.in/uploads/', '').replace('.xml','').replace('%20',' ').replace('%26', '&amp;')
        if i != "" and i !="https://api.bongo-solutions.com/roster/EpgXml?channel=bongo-movies&days=1":
            resp = urllib3.request("GET", i)
            with open(f'{epgid}.xml', 'wb') as f:
                f.write(resp.data)
            with open(f'{epgid}.xml', 'r', encoding="utf-8-sig") as f:
                raw = f.read()
            clean = html.unescape(raw)
            if resp.data != b'Channel not found':
                epgroot = ET.fromstring(clean, parser=etree.XMLParser(recover=True,encoding='utf-8'))
                chnl = ET.SubElement(root, 'channel')
                chnl.set('id',epgid)
                dspl = ET.SubElement(chnl, 'display-name')
                icon = ET.SubElement(chnl, 'icon')
                dspl.text = titles[epgs.index(i)]
                icon.set('src', logos[epgs.index(i)])

            for type_tag in epgroot.findall('programme'):
                title = type_tag.find('title').text
                desctag = type_tag.find('desc')
                if desctag != None:
                    desc = desctag.text
                else:
                    desc = ""
                icotag = type_tag.find('ThumbnailUrl')
                if icotag != None:
                    ico = icotag.text
                else:
                    ico = ""
                start = type_tag.get("start")
                stop = type_tag.get("stop")
                prog = ET.SubElement(root, 'programme')
                prog.set('channel', epgid)
                prog.set('start', start)
                prog.set('stop', stop)
                progtitle = ET.SubElement(prog, 'title')
                progtitle.text = title
                progdesc = ET.SubElement(prog, 'desc')
                progdesc.text = desc
                progico = ET.SubElement(prog, 'icon')
                progico.set('src', ico)

            xml = pathlib.Path(f"{epgid}.xml")
            xml.unlink()
    else:
        if "oli" in i:
            epgid = "OLI TV"
            resp = urllib3.request("GET", i)
            with open(f'{epgid}.xml', 'wb') as f:
                f.write(resp.data)
            with open(f'{epgid}.xml', 'r', encoding="utf-8-sig") as f:
                raw = f.read()
            clean = html.unescape(raw)
            epgroot = ET.fromstring(clean, parser=etree.XMLParser(recover=True,encoding='utf-8'))
            chnl = ET.SubElement(root, 'channel')
            chnl.set('id',epgid)
            dspl = ET.SubElement(chnl, 'display-name')
            icon = ET.SubElement(chnl, 'icon')
            dspl.text = titles[epgs.index(i)]
            icon.set('src', logos[epgs.index(i)])

            for type_tag in epgroot.findall('programme'):
                title = type_tag.find('title').text
                desctag = type_tag.find('desc')
                if desctag != None:
                    desc = desctag.text
                else:
                    desc = ""
                stop = type_tag.get("stop")
                prog = ET.SubElement(root, 'programme')
                prog.set('channel', epgid)
                prog.set('start', start)
                prog.set('stop', stop)
                progtitle = ET.SubElement(prog, 'title')
                progtitle.text = title
                progdesc = ET.SubElement(prog, 'desc')
                progdesc.text = desc

            xml = pathlib.Path(f"{epgid}.xml")
            xml.unlink()

xml_data = ET.tostring(root)

with open('./epg/neotv.xml', 'wb') as f:
    f.write(xml_data)
    print("Exported!")
f.close()

with gzip.open('./epg/neotv.xml.gz', 'wb') as g:
    g.write(xml_data)
g.close()
