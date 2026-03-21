def adjustTable(talbe, row, col):
    pivot = talbe[row][col]
    for i in range(len(talbe[row])):
        talbe[row][i] /= pivot
    for i in range(len(talbe)):
        if i != row:
            factor = talbe[i][col]
            for j in range(len(talbe[i])):
                talbe[i][j] -= factor * talbe[row][j]

def getRowToChange(table, function, isMaxProblem, base):
    num = None
    pos = None
    for i in range(len(function)):
        total = 0
        for j in range(len(base)):
            total += base[j]*table[j][i]
        if not num or (total > 0 and total > num)if isMaxProblem else (total < 0 and total < num):
            num = total
            pos = i
    return pos

def getColumnOut(table, pos):
    num = None
    pos = None
    for i in range(len(table)):
        row = table[i]
        total = row[-1] / row[pos]
        if total > 0 and total < num:
            num = total
            pos = i
    return pos
