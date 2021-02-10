import json
import math
import statistics
import sys
from ..core.api.historical import getHistoricalData
from ..core.api.stats import getKeyStats
from ..core.api.bonds import get3mTreasury
from ..core.functions import extract_data, logReturns
from .functions import *


def vix_explanation():
    """
    I have followed the official VIX whitepaper to the best of my ability in the making of this program.
    This program uses the TD Ameritrade API to fetch the entire option chain, and the IEX Cloud API to fetch the
    3M Treasury Bond yield, (the risk-free interest rate).

    I have attempted to document the process as best as I can. 
    https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx

    
    """


def vix_equation(ticker='SPY', sandbox=False):
    """
    Runs the VIX equation on a ticker.

    Parameters
    ----------
    ticker      :string
    sandbox     :bool
                Sets the IEX environment to sandbox mode to make limitless API calls for testing.

    Returns
    -------
    vix         :float
    """

    # Step 1: Fetch the option chain for the ticker.
    chain = collectOptionChain(ticker)

    # Step 2
    # Find the proper "near-term" and "next-term" option expirations to be used to find Forward Level. 
    # See selectOptionExpirations() in functions.py.
    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx (slide 4)
    selectedDates, selectedChain = selectOptionExpirations(chain)


    # Step 3
    # Determine the forward SPX level, F, by identifying the strike price at which the
    # absolute difference between the call and put prices is smallest
    forwardLevel = calculateForwardLevel(selectedChain)

    # Step 4
    # Calculate R
    # The risk-free interest rate, R, is the bond-equivalent yield of the U.S. T-bill maturing
    # closest to the expiration dates of relevant SPX options. As such, the VIX calculation may
    # use different risk-free interest rates for near- and next-term options.
    r = get3mTreasury()[0]['value']

    # Step 5
    # Calculate T1 and T2, for near-term and next-term options respectively. See calculateT() in functions.py for more.
    t1, t2 = calculateT(selectedDates)

    # Step 6
    # Calculate F, where F is the: "forward SPX {but in our case, any ticker} level, by identifying the strike price at which the
    # absolute difference between the call and put prices is smallest."
    # https://www.optionseducation.org/referencelibrary/white-papers/page-assets/vixwhite.aspx (slide 5)

    f1, f2 = calculateF(t1, t2, r, forwardLevel)

    # Step 7
    # Calculate K0 and upper/lower boundaries on chain
    # See calculateK() for more info here.
    k = calculateK(f1, f2, selectedChain)

    # Step 8
    # Calculate deltaK for each contract in selected chain.
    deltaK = deltaK(k, selectedChain)


    sys.exit()

    # minutes in year, minutes in month
    # min_in_year = 525600
    # min_in_month = 43200

    # Vix calculation as explained by Investopedia.
    # vix = math.sqrt(
    #     (this_month_option / min_in_year) * vol3Weeks * (next_month_option - min_in_month / next_month_option - this_month_option) +
    #     (next_month_option / min_in_year) * monthVol * (min_in_month - this_month_option / next_month_option - this_month_option)
    # )

    return vix
