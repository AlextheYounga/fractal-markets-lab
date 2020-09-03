Commands:

<!-- Donchian -->
python -c 'from lab.donchian.calculator import calculate; print(calculate("CHWY"))'
<!-- Value at Risk -->
python -c 'from lab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'
<!-- Volatility -->
python -c 'from lab.volatility.calculator import calculate; print(calculate("SPY"))'
<!-- Risk Range -->
python -m lab.riskrange.scan_portfolio
python -c 'from lab.riskrange.lookup import rangeLookup; print(rangeLookup("EDV"))'
<!-- Trend -->
python -c 'from lab.trend.analyze import analyze; print(analyze("SPY"))'
<!-- Financials -->
python -c 'from lab.financials.lookup import lookupFinancials; print(lookupFinancials("BELDF"))'