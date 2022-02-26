import xmltodict

fin = open('map1.osm', 'r', encoding='utf8')
xml = fin.read()
fin.close()

parsedxml = xmltodict.parse(xml)
total_with_tag = 0
total_wo_tag = 0
for el in parsedxml['osm']['node']:
    if el.get('tag') is None:
        total_wo_tag += 1
    else:
        total_with_tag += 1
print(total_with_tag, total_wo_tag, sep=' ')