import os
import sys
import colored
from colored import stylize
from lab.core.output import printTabs, printFullTable
from dotenv import load_dotenv
load_dotenv()


def list_commands():
    headers = ['Command', 'Description']
    print("\n")
    print('Available Subcommands')
    print('No quotes required on [<ticker>] arguments, may be typed directly into the terminal.')
    print("\n\n")

    commands = [
        ['correlations:scan', 'Runs correlations on all ETFs on the market, with *every other ETF on the market. (Takes about half an hour)'],
        ['correlations:lookup [t1, t2]', 'Fetches correlation between two tickers'],
        ['donchian [<ticker>]', 'Runs a donchian range calculation on a ticker'],
        ['financials [<ticker>]', 'Returns financials data for ticker, including some custom indicators not provided by IEX.'],
        ['macro:trends [--timeframe=1m] [--gain=20]', 'Scans all ETFs and returns the ETFs with the performance above an int (gain) within a timerange (5d, 1m, 3m, 1y)'],
        ['macro:gainers', 'Scans all ETFs and returns ETFs with highest day change.'],
        ['news:scrape [--query=insert+string]', 'Searches a query and searches first 10 articles for stocks mentioned in article'],
        ['hurst [<ticker>] [--output=table]', 'Runs a rescaled range analysis on a ticker. Output defaults to table.'],
        ['range [<ticker>] [--tweet]', 'Runs a volatility range analysis on a ticker.'],
        ['historicalprices:get [<ticker>]', 'Fetches historical prices for a ticker and saves them to db.'],
        ['inflation:calculate [--update]', 'Inflation index using etfs'],
        ['inflation:graph [--update]', 'Graph inflation index using etfs'],
        ['inflation:functions [--refresh]', 'Grabs max historical prices for all etfs in sectors list, updates with fresh data.'],
        ['trend:chase [--pennies]', 'Scans all stocks and returns todays gainers with above certain thresholds (weeds out the penny stocks).'],
        ['trend:search [--string=]', 'Scans stocks with string in stock name and looks for gainers'],
        ['trend:earnings', 'Scans all stocks and returns todays gainers who have consistently good earnings.'],
        ['trend:streak [<ticker>]', 'Determines the current winning/losing streak for a ticker'],
        ['trend:gainers', 'Grabs todays gainers and checks their earnings.'],
        ['trend:google', 'Searches google trends for search query interest'],
        ['pricedingold [<ticker>][--timespan=5y][--test=False]', 'Graphs and assets price in gold.'],
        ['vol:graph [<ticker>] [--ndays=30]', 'Graphs vol'],
        ['volume:chase', 'Scans all stocks and returns todays gainers with abnormally high volume.'],
        ['volume:anomaly', 'Scans all stocks and returns stocks who are accumulating extremely high volume over the last week. Finds market singularities.'],
        ['volume:graph [<ticker>][--timeframe=3m][--sandbox=false]', 'Scans all stocks and returns stocks who are accumulating extremely high volume over the last week. Finds market singularities.'],
        ['vix [<ticker>]', 'Runs the VIX volatility equation on a ticker'],
        ['output:last', 'Returns the last cached output, can resort by specific key.'],
        ['rdb:export', 'Exports redisdb to zipped json file'],
        ['rdb:import', 'Import redisdb from a zipped json file'],

    ]
    printTabs(commands, headers, 'simple')
    print("\n\n")


def command_error(required={}, opt=None):
    if(not (required or opt)):
        print(stylize("Error: your command did not match any known programs. Closing...", colored.fg("red")))
        print("\n")
        return

    if (required):
        print(stylize("FAILED: Requires arguments: ", colored.fg("red")))
        for typ, var in required.items():
            print(stylize("({}) [{}]".format(typ, var), colored.fg("red")))
        print("\n")
    if (opt):
        print(stylize("Optional arguments: ", colored.fg("yellow")))
        if (isinstance(opt, dict)):
            for typ, var in opt.items():
                print(stylize("({}) [{}]".format(typ, var), colored.fg("yellow")))
        if (isinstance(opt, list)):
            for var in opt.items():
                print(stylize("[{}]".format(var), colored.fg("yellow")))
            print("\n")


def correlations_controller(subroutine, args=[]):
    """
    """
    # if (subroutine == 'scan'):
    #TODO: Fix correlations
        # from lab.correlations.scanner import scanner
        # print(scanner())
    # if (subroutine == 'lookup'):
    #     from lab.correlations.analyze import lookup
    #     if (args and len(args) == 2):
    #         print(lookup(args[0], args[1]))


def donchian_controller(args):
    required = {"string": "ticker"}
    opt = ["--tweet"]

    if (not args):
        command_error(required, opt)
        return

    from lab.donchian.range import calculate
    ticker = args[0]
    try:
        tweet = True if (args[1] == '--tweet') else False
        print(calculate(ticker, tweet))
        return
    except IndexError:
        print(calculate(ticker))
        return
    command_error()

def historicalprices_controller(subroutine, args):
    """
    """
    #TODO Switch to redisdb here
    # if (subroutine == 'get'):
    #     if (args):
    #         from lab.database.hp.update_prices import refresh_one
    #         print(refresh_one(args[0]))


def inflation_controller(subroutine, args=[]):
    if (subroutine == 'graph'):
        from lab.inflation.measure import graph

        try:
            update = True if (args and args[0] == '--update') else False
            print(graph(update))
            return

        except IndexError:
            print(graph())
            return

    if (subroutine == 'calculate'):
        from lab.inflation.measure import annual

        try:
            update = True if (args[0] == '--update') else False
            print(annual(update))
            return

        except IndexError:
            print(annual())
            return

    command_error()


def financials_controller(args):
    required = {"string": "ticker"}

    if (not args):
        command_error(required)
        return

    ticker = args[0]
    from lab.financials.lookup import lookupFinancials
    print(lookupFinancials(ticker))


def macro_controller(subroutine, args=[]):
    if (subroutine == 'trends'):
        from lab.macro.trends import calculate_trends

        try:
            timeframe = args[0].split('--')[1]
            gain = args[1].split('--')[1]
            print(calculate_trends(timeframe, gain))
            return

        except IndexError:
            try:
                timeframe = args[0].split('--')[1]
                print(calculate_trends(timeframe))
                return
            except IndexError:
                print(calculate_trends)
                return

    if (subroutine == 'gainers'):
        import lab.macro.gainers

    command_error()


def news_controller(subroutine, args=[]):
    if (subroutine == 'scrape'):
        from lab.news.scrape_headlines import scrape_news

        try:
            query = args[0].split('--')[1]
            print(scrape_news(query))
            return
        except IndexError:
            print(scrape_news())
            return
    command_error()


def pricedingold_controller(args):
    from lab.pricedingold.compare import price_in_gold
    required = {"string": "ticker"}
    opt = {"string": "--timeframe"}

    if (not args):
        command_error(required, opt)
        return
    try:
        ticker = args[0]
        timeframe = args[1].split('--')[1]
        print(price_in_gold(ticker, timeframe))
        return
    except IndexError:
        try:
            ticker = args[0]
            print(price_in_gold(ticker))
            return
        except IndexError:
            print(price_in_gold)
            return


def hurst_controller(args):
    required = {"string": "ticker"}
    opt = {"string": "--output"}

    if (not args):
        command_error(required, opt)
        return

    from lab.rescaledrange.fractal_calculator import fractal_calculator
    ticker = args[0]

    try:
        output = args[1].split('--')[1]
        print(fractal_calculator(ticker, output))
        return
    except IndexError:
        print(fractal_calculator(ticker))
        return


def rdb_controller(subroutine, args=[]):
    if (subroutine == 'export'):
        from lab.redisdb.export import export_rdb
        export_rdb()
    if (subroutine == 'import'):
        from lab.redisdb.imports import import_rdb
        import_rdb()


def range_controller(args):
    from lab.riskrange.lookup import rangeLookup
    required = {"string": "ticker"}
    opt = ["--tweet"]

    if (not args):
        command_error(required, opt)
        return

    ticker = args[0]
    try:
        tweet = True if (args[1] == '--tweet') else False
        print(rangeLookup(ticker, tweet))
        return
    except IndexError:
        print(rangeLookup(ticker))
        return


def output_controller(subroutine, args):
    if (subroutine == 'last'):
        from lab.redisdb.controller import fetch_last_output

        try:
            filterKey = args[0].split('--')[1]
            results = fetch_last_output(filterKey)
            printFullTable(results, struct='dictlist')
            return
        except IndexError:
            results = fetch_last_output()
            printFullTable(results, struct='dictlist')
            return
    command_error()


def trend_controller(subroutine, args):
    # TODO: Finish price targets
    # if (subroutine == 'pricetarget'):        
    #     from lab.trend.pricetarget import lookup
    #     print(lookup(args[0]))

    if (subroutine == 'streak'):
        required = {"string": "ticker"}
        if (not args):
            command_error(required)
            return

        from lab.trend.streak.count import count_streak
        print(count_streak(args[0]))
        return

    if (subroutine == 'search'):
        required = {"string": "query"}
        if (not args):
            command_error(required)
            return
        from lab.trend.chase.search import search
        searchstring = args[0].split('=')[1]
        print(search(searchstring))
        return

    if (subroutine == 'chase'):
        from lab.trend.chaser import chase_trends
        if (args):
            print(chase_trends(args[0]))
            return
        print(chase_trends())

    if (subroutine == 'earnings'):
        import lab.trend.chase.earnings
        return

    if (subroutine == 'gainers'):
        import lab.trend.gainers
        return
    if (subroutine == 'google'):
        from lab.trend.googletrends.request import stock_search_trends
        print(stock_search_trends())
        return

    command_error()


def vol_controller(subroutine, args):
    required = {"string": "ticker"}
    opt = {"string": "--ndays="}

    if (not args):
        command_error(required, opt)
        return
    if (subroutine == 'graph'):
        from lab.vol.calculator import graphVol
        ticker = args[0]
        try:
            print(graphVol(ticker, ndays=args[1]))
        except IndexError:
            print(graphVol(ticker))
        return


def volume_controller(subroutine, args):
    if (subroutine == 'graph'):
        required = {"string": "ticker"}
        if (not args):
            command_error(required)
            return
        from lab.volume.graph import graph_volume
        print(graph_volume(args[0]))

    if (subroutine == 'chase'):
        import lab.volume.chase

    if (subroutine == 'anomaly'):
        import lab.volume.anomaly


def vix_controller(args):
    required = {"string": "ticker"}
    opt = {"string": "--debug"}

    if (not args):
        command_error(required, opt)
        return

    from lab.vix.equation import vix_equation

    ticker = args[0]

    if (len(args) >= 2):
        debug = True if (args[1] == '--debug') else False
        print(vix_equation(ticker, debug))
        return

    print('VIX: '+str(vix_equation(ticker)))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab.settings')
    sys.argv.pop(0)

    args = [arg.strip() for arg in sys.argv]

    if (args[0] == 'list'):
        list_commands()
        return

    if (':' in args[0]):
        command = args.pop(0)
        program = command.split(':')[0] + "_controller"
        subroutine = command.split(':')[1]

        globals()[program](subroutine, args)
        return
    else:
        program = args.pop(0) + "_controller"

        globals()[program](args)
        return


if __name__ == '__main__':
    main()
