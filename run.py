import os
import sys
from dotenv import load_dotenv
load_dotenv()


def correlations_controller(subroutine):
    # TODO Figure out the rest of correlations.
    if (subroutine == 'scanner'):
        from lab.correlations.scanner import scanner
        print(scanner())
        return "Done"


def donchian_controller(ticker, tweet):
    from lab.donchian.calculator import calculate
    print(calculate(ticker, tweet))
    return "Done"


def financials_controller(ticker):
    from lab.financials.lookup import lookupFinancials
    print(lookupFinancials(ticker))
    return "Done"


def macro_controller(subroutine):
    if (subroutine == 'trends'):
        import lab.macro.trends
        return "Done"
    if (subroutine == 'gainers'):
        import lab.macro.gainers
        return "Done"


def hurst_controller(ticker, output):
    from lab.rescaledrange.fractal_calculator import fractal_calculator
    print(fractal_calculator(ticker, output))
    return "Done"


def range_controller(ticker, output):
    from lab.riskrange.lookup import rangeLookup
    print(rangeLookup(ticker, output))
    return "Done"


def twitter_controller(args):
    subroutine = args[1]
    if (subroutine == 'follow'):
        from lab.twitter.user import followFollowers
        if (args[3] == 'restart'):
            print(followFollowers(args[2], 0))
            return "Done"
        print(followFollowers(args[2]))
        return "Done"

    if (subroutine == 'trim'):
        from lab.twitter.user import trimFollowers
        if (args[2] == 'restart'):
            print(trimFollowers(0))
            return "Done"
        print(trimFollowers())
        return "Done"


def trend_controller(args):
    subroutine = args[1]
    if (len(args) >= 3):
        if (subroutine == 'pricetarget'):
            # TODO: Finish price targets
            from lab.trend.pricetarget import lookup
            print(lookup(args[2]))
            return "Done"
    if (subroutine == 'chase'):
        import lab.trend.chase
        return "Done"
    if (subroutine == 'earnings'):
        import lab.trend.chase_earnings
        return "Done"
    if (subroutine == 'volume'):
        import lab.trend.chase_volume
        return "Done"
    if (subroutine == 'gainers'):
        import lab.trend.gainers
        return "Done"


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab.settings')
    sys.argv.pop(0)
    args = sys.argv
    program = args[0]

    # Correlations
    if (program == 'correlations'):
        correlations_controller(args[1])

    # Donchian Range
    if (program == 'donchian'):
        tweet = True if ((len(args) >= 3) and (args[2] == 'tweet')) else False
        donchian_controller(args[1], tweet)

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
