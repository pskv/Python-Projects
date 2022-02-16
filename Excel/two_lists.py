import openpyxl as xl

wb = xl.load_workbook('trekking3.xlsx')
ws = wb['Справочник']
dict1 = dict()
for i in range(37):
    dict1[ws.cell(row=i+2, column=1).value] = \
        tuple(ws.iter_rows(min_row=i+2, min_col=2, max_col=5, values_only=True))[0]

ws = wb['Раскладка']
res_dict = dict()
for i in range(99):
    day = ws['A'+str(i+2)].value
    res_dict[day] = list(map(sum, zip(res_dict.get(day, (0, 0, 0, 0)),
                                      map(lambda x: (ws['C' + str(i + 2)].value * x / 100) if x is not None else 0,
                                          dict1[ws['B' + str(i + 2)].value])
                                      )))
for now in res_dict:
    print(*list(map(int, res_dict[now])))