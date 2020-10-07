import texttable


def setWidths(data):
    widths = []
    for word in data.keys():
        length = len(word)
        widths.append(length)
    return widths


def printTable(data):
    print("\n")
    headers = data.keys()
    table = texttable.Texttable()
    table.header(headers)
    table.set_cols_width(setWidths(data))
    table.add_rows(data.values(), header=False)

    print(table.draw())
    print("\n")
