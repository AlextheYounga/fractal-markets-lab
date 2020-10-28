Commands
Must run the first time you start the project


```export DJANGO_SETTINGS_MODULE=lab.settings```

Donchian Formulas:


```python -c 'from lab.donchian.calculator import calculate; print(calculate("CHWY"))'```

Value at Risk (Still figuring this out)


```python -c 'from lab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'```


Rescaled Range (I think this is currently broken, and it needs to be redone completely. I have another repo with a working rescaled range calculator, the code is painful but I know how to make it gooder, just need the time to redo it.)


```python -m lab.rescaledrange.calculator```

Volatility Formulas


```python -c 'from lab.volatility.calculator import calculate; print(calculate("SPY"))'```

Trends


'''python -c 'from lab.trend.streak.analyze import streak_analyzer; print(streak_analyzer("SPY"))'
python -m lab.trend.chase
python -m lab.trend.gainers'''

Financials


'''python -c 'from lab.financials.lookup import lookupFinancials; print(lookupFinancials("BELDF"))''''