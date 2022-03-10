import xmltodict

fin = open('map2.osm', 'r', encoding='utf8')
xml = fin.read()
fin.close()

parsedxml = xmltodict.parse(xml)
total_cnt = 0
for el in parsedxml['osm']['node']:
    if el.get('tag') is not None:
        d = el.get('tag')
        if isinstance(d, list):
            if d[0].get('@k') == 'amenity' and d[0].get('@v') == 'fuel':
                total_cnt += 1
        elif d.get('@k') == 'amenity' and d.get('@v') == 'fuel':
            total_cnt += 1
print(total_cnt)