import json
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from ..core.functions import *
import pandas as pd
import numpy as np
import calendar


def optionExpirationMinutes():
    today = datetime.today()
    year = today.year
    month = today.month
    next_month = today + relativedelta(months=+1)
    next_month_year = next_month.year
    next_month = next_month.month

    calndr = calendar.Calendar(firstweekday=calendar.SUNDAY)

    clndr_matrix = calndr.monthdatescalendar(year, month)
    third_friday = [day for week in clndr_matrix for day in week if
                    day.weekday() == calendar.FRIDAY and
                    day.month == month][2]

    clndr_matrix = calndr.monthdatescalendar(next_month_year, next_month)
    next_third_friday = [day for week in clndr_matrix for day in week if
                         day.weekday() == calendar.FRIDAY and
                         day.month == next_month][2]

    this_month_diff = datetime.combine(third_friday, datetime.min.time()) - today
    this_month_expir = int((this_month_diff.total_seconds() // 60) - 1440)

    next_month_diff = datetime.combine(next_third_friday, datetime.min.time()) - today
    next_month_expir = int((next_month_diff.total_seconds() // 60) - 1440)

    return this_month_expir, next_month_expir


def interdayReturns(prices):
    int_returns = []
    for i, price in enumerate(prices):
        ret = (prices[i + 1] / price) - 1 if (i + 1 in range(-len(prices), len(prices)) and float(prices[i + 1]) != 0) else 0
        int_returns.append(ret)

    return int_returns
