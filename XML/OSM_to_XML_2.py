import xmltodict

fin = open('map2.osm', 'r', encoding='utf8')
xml = fin.read()
fin.close()

parsedxml = xmltodict.parse(xml)
total_cnt = 0
for el in (parsedxml['osm']['node'] + parsedxml['osm']['way']):
    # if el.get('@id') != "416170216":
    #     continue
    if el.get('tag') is not None:
        d = el.get('tag')
        if isinstance(d, list):
            for el2 in d:
                if el2.get('@k') == 'amenity' and el2.get('@v') == 'fuel':
                    total_cnt += 1
            # if d[0].get('@k') == 'amenity' and d[0].get('@v') == 'fuel':
            #     total_cnt += 1
            #     print(d)
        elif isinstance(d, dict):
            if d.get('@k') == 'amenity' and d.get('@v') == 'fuel':
                total_cnt += 1
                # print(d)
print(total_cnt)