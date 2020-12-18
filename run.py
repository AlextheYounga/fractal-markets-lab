import os
import sys
from lab.core.output import printTabs
from dotenv import load_dotenv
load_dotenv()


def list_commands():
    headers = ['Command', 'Description']
    print("\n")
    print('Available Subcommands')
    print('No quotes required on [ticker] arguments, may be typed directly into the terminal.')
    print("\n\n")    

    commands = [
        ['correlations scan', 'Runs correlations on all ETFs on the market, with *every other ETF on the market. (Takes about half an hour)'],
        ['donchian [ticker]', 'Runs a donchian range calculation on a ticker'],
        ['financials [ticker]', 'Returns financials data for ticker, including some custom indicators not provided by IEX.'],
        ['macro trends', 'Scans all ETFs and returns the ETFs with the best short term performance.'],
        ['macro gainers', 'Scans all ETFs and returns ETFs with highest day change.'],
        ['hurst [ticker]', 'Runs a rescaled range analysis on a ticker.'],
        ['range [ticker]', 'Runs a volatility range analysis on a ticker.'],
        ['twitter follow [handle, page_number]', 'Combs through a followers of a user and follows particular people. Each loop is a *page* of 20 people.'],
        ['twitter trim [page_number]', 'Combs through your followers and removes certain types of people.'],
        ['trend chase', 'Scans all stocks and returns todays gainers with above certain thresholds (weeds out the penny stocks).'],
        ['trend earnings', 'Scans all stocks and returns todays gainers who have consistently good earnings.'],
        ['trend volume', 'Scans all stocks and returns todays gainers with abnormally high volume.'],
        ['trend gainers', 'Grabs todays gainers and checks their earnings.'],
    ]
    printTabs(commands, headers, 'simple')
    print("\n\n")


def correlations_controller(subroutine):
    # TODO Figure out the rest of correlations.
    if (subroutine == 'scan'):
        from lab.correlations.scanner import scanner
        print(scanner())


def donchian_controller(ticker, tweet):
    from lab.donchian.range import calculate
    print(calculate(ticker, tweet))


def financials_controller(ticker):
    from lab.financials.lookup import lookupFinancials
    print(lookupFinancials(ticker))


def macro_controller(subroutine):
    if (subroutine == 'trends'):
        import lab.macro.trends

    if (subroutine == 'gainers'):
        import lab.macro.gainers


def hurst_controller(ticker, output):
    from lab.rescaledrange.fractal_calculator import fractal_calculator
    print(fractal_calculator(ticker, output))


def range_controller(ticker, output):
    from lab.riskrange.lookup import rangeLookup
    print(rangeLookup(ticker, output))


def twitter_controller(args):
    subroutine = args[1]
    if (subroutine == 'follow'):
        from lab.twitter.user import followFollowers
        if ((len(args) >= 4) and (args[3] == 'restart')):
            print(followFollowers(args[2], 0))

        print(followFollowers(args[2]))

    if (subroutine == 'trim'):
        from lab.twitter.user import trimFollowers
        if ((len(args) >= 3) and (args[2] == 'restart')):
            print(trimFollowers(0))

        print(trimFollowers())


def trend_controller(args):
    subroutine = args[1]
    if (len(args) >= 3):
        if (subroutine == 'pricetarget'):
            # TODO: Finish price targets
            from lab.trend.pricetarget import lookup
            print(lookup(args[2]))

    if (subroutine == 'chase'):
        import lab.trend.chase

    if (subroutine == 'earnings'):
        import lab.trend.chase_earnings

    if (subroutine == 'volume'):
        import lab.trend.chase_volume

    if (subroutine == 'gainers'):
        import lab.trend.gainers


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab.settings')
    sys.argv.pop(0)

    args = [arg.strip() for arg in sys.argv]

    if (args[0] == 'list'):
        list_commands()
        return

    program = args[0]

    # Correlations
    if (program == 'correlations'):
        correlations_controller(args[1])

    # Donchian Range
    if (program == 'donchian'):
        tweet = True if ((len(args) >= 3) and (args[2] == 'tweet')) else False
        donchian_controller(args[1], tweet)
        return "Done"

    # Lookup Financials
    if (program == 'financials'):
        financials_controller(args[1])

    # Macro Trends and Gainers
    if (program == 'macro'):
        macro_controller(args[1])

    # Rescaled Range and Hurst Exponents
    if (program == 'hurst'):
        output = args[2] if (len(args) >= 3) else 'table'
        hurst_controller(args[1], output)

    # Volatility Range (AKA RiskRange)
    if (program == 'range'):
        output = args[2] if (len(args) >= 3) else 'table'
        range_controller(args[1], output)

    # Twitter Commands
    if (program == 'twitter'):
        twitter_controller(args)

    # Trend Chasing
    if (program == 'trend'):
        trend_controller(args)

    print("Error: your command did not match any known programs. Closing...")
    return


if __name__ == '__main__':
    main()
