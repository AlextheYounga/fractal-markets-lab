Commands:
export DJANGO_SETTINGS_MODULE=lab.settings

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
python -c 'from lab.trend.streak.analyze import streak_analyzer; print(streak_analyzer("SPY"))'
python -m lab.trend.chaser.chase
<!-- Financials -->
python -c 'from lab.financials.lookup import lookupFinancials; print(lookupFinancials("BELDF"))'