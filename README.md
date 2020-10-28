Useful Commands:


Must run the first time you start the project


```export DJANGO_SETTINGS_MODULE=lab.settings```

Donchian Formulas:


```python -c 'from lab.donchian.calculator import calculate; print(calculate("CHWY"))'```

Value at Risk (Still figuring this out)


```python -c 'from lab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'```


Rescaled Range (I think this is currently broken, and it needs to be redone completely. I have another repo with a working rescaled range calculator, the code is painful but I know how to make it gooder, just need the time to redo it.)


```python -m lab.rescaledrange.calculator```



VIX Volatility Index



I recreated the VIX Volatility Index here. I'm suspicious of the math involved with the VIX formula. Maybe I'm missing something on the option expiration dates, but still, the logic behind the math seems very odd. Amazingly, you can use the VIX formula on a penny stock and get a value like 23. Supposedly the VIX is the most accurate vol index on SPY in existence, but I'm starting to question that. I'd like to eventually go through and test the VIX compared to common vol equations. 

I've thoroughly commented the equation to explain what is happening at each step. You can see how weird the logic is yourself. I set the default ticker to Spanish Mountain Gold so you can see the weirdness for yourself. 


```python -c 'from lab.vix.calculation import vixCalculation; print(vixCalculation("SPY"))'```

Trends


```
python -c 'from lab.trend.streak.analyze import streak_analyzer; print(streak_analyzer("SPY"))'
python -m lab.trend.chase
python -m lab.trend.gainers
```

Financials


```python -c 'from lab.financials.lookup import lookupFinancials; print(lookupFinancials("BELDF"))'```