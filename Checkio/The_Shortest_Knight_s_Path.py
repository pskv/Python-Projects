def checkio(cells):
    mov = [1,2,2,1,-1,-2,-2,-1,1,2]
    weights = {cells[:2]: 0}
    unchecked_cells = [cells[:2]]
    while True:
        src_adr = unchecked_cells.pop(0)

        for i in range(8):
            if not 97 <= ord(src_adr[0])+mov[i] <= 104 or not 1 <= int(src_adr[1])+mov[i+2] <= 8:
                continue
            tgt_adr = chr(ord(src_adr[0])+mov[i])+str((int(src_adr[1])+mov[i+2]))
            if tgt_adr == cells[3:5]:
                return weights[src_adr]+1
            if tgt_adr not in weights:
                weights[tgt_adr] = weights[src_adr]+1
                unchecked_cells.append(tgt_adr)

if __name__ == "__main__":
    #These "asserts" using only for self-checking and not necessary for auto-testing
    # print(checkio("b1-d5"))
    assert checkio("b1-d5") == 2, "1st example"
    assert checkio("a6-b8") == 1, "2nd example"
    assert checkio("h1-g2") == 4, "3rd example"
    assert checkio("h8-d7") == 3, "4th example"
    assert checkio("a1-h8") == 6, "5th example"