import texttable
from ..shared.output import setWidths


def printTable(ticker, stats):
    print("\n")
    print(ticker, stats[ticker]['Signal'])
    del stats[ticker]['Signal']
    headers = stats[ticker].keys()
    table = texttable.Texttable()
    table.header(headers)
    table.set_cols_width(setWidths(stats[ticker]))
    table.add_rows([stats[ticker].values()], header=False)

    print(table.draw())
    print("\n")
