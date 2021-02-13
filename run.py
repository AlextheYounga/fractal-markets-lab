import os
import sys
from lab.core.output import printTabs
from dotenv import load_dotenv
load_dotenv()


def list_commands():
    headers = ['Command', 'Description']
    print("\n")
    print('Available Subcommands')
    print('No quotes required on [<ticker>] arguments, may be typed directly into the terminal.')
    print("\n\n")

    commands = [
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
        ['pricedingold [<ticker>][--timespan=5y][--test=False]', 'Graphs and assets price in gold.'],
        ['volume:chase', 'Scans all stocks and returns todays gainers with abnormally high volume.'],
        ['volume:anomaly', 'Scans all stocks and returns stocks who are accumulating extremely high volume over the last week. Finds market singularities.'],
        ['vix [<ticker>]', 'Runs the VIX volatility equation on a ticker'],
    ]
    printTabs(commands, headers, 'simple')
    print("\n\n")



def donchian_controller(args):
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>]. Optional args [--tweet]')
        return
    from lab.donchian.range import calculate
    ticker = args[0]
    try:
        tweet = True if (args[1] == '--tweet') else False
        print(calculate(ticker, tweet))
    except IndexError:
        print(calculate(ticker))



def inflation_controller(subroutine, args=[]):
    if (subroutine == 'graph'):
        from lab.inflation.measure import graph
        try:
            update = True if (args and args[0] == '--update') else False
            print(graph(update))
        except IndexError:
            print(graph())

    if (subroutine == 'calculate'):
        from lab.inflation.measure import annual
        try:
            update = True if (args[0] == '--update') else False
            print(annual(update))
        except IndexError:
            print(annual())


def financials_controller(args):
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>].')
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
        except IndexError:
            try:
                timeframe = args[0].split('--')[1]
                print(calculate_trends(timeframe))
            except IndexError:
                print(calculate_trends)
                return

    if (subroutine == 'gainers'):
        import lab.macro.gainers


def news_controller(subroutine, args=[]):
    if (subroutine == 'scrape'):
        from lab.news.scrape_headlines import scrape_news

        try:
            query = args[0].split('--')[1]
            print(scrape_news(query))
        except IndexError:
            print(scrape_news())
            return


def pricedingold_controller(args):
    from lab.pricedingold.compare import price_in_gold
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>]. Optional argument --timeframe')
        return
    try:
        ticker = args[0]
        timeframe = args[1].split('--')[1]
        print(price_in_gold(ticker, timeframe))
    except IndexError:
        try:
            ticker = args[0]
            print(price_in_gold(ticker))
        except IndexError:
            print(price_in_gold)
            return


def hurst_controller(args):
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>]. Optional argument --output')
        return

    from lab.rescaledrange.fractal_calculator import fractal_calculator
    ticker = args[0]

    try:
        output = args[1].split('--')[1]
        print(fractal_calculator(ticker, output))
    except IndexError:
        print(fractal_calculator(ticker))
        return


def range_controller(args):
    from lab.riskrange.lookup import rangeLookup
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>]. Optional argument --tweet')
        return
    ticker = args[0]
    try:
        tweet = True if (args[1] == '--tweet') else False
        print(rangeLookup(ticker, tweet))
    except IndexError:
        print(rangeLookup(ticker))
        return


def trend_controller(subroutine, args):
    if (args):
        if (subroutine == 'streak'):
            from lab.trend.streak.count import count_streak
            print(count_streak(args[0]))
        if (subroutine == 'search'):
            from lab.trend.chase.search import search
            print(search(args[0]))
        return

    if (subroutine == 'chase'):
        from lab.trend.chaser import chase_trends
        if (args):
            print(chase_trends(args[0]))
            return
        print(chase_trends())

    if (subroutine == 'earnings'):
        import lab.trend.chase.earnings

    if (subroutine == 'gainers'):
        import lab.trend.gainers


def volume_controller(subroutine, args):
    if (subroutine == 'chase'):
        import lab.volume.chase

    if (subroutine == 'anomaly'):
        import lab.volume.anomaly


def vix_controller(args):
    if (not args):
        print('FAILED: Requires arguments (string) [<ticker>]. Optional argument for debugging [--debug]')
        return
    from lab.vix.equation import vix_equation

    ticker = args[0]
    
    if (len(args) >= 2):
        debug = True if (args[1] == '--debug') else False
        print(vix_equation(ticker, debug))
        return
        
    print(vix_equation(ticker))        


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

    print("Error: your command did not match any known programs. Closing...")
    return


if __name__ == '__main__':
    main()
