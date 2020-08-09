Commands:

<!-- Donchian -->
python -c 'from lab.donchian.calculator import calculate; print(calculate("CHWY"))'
<!-- Value at Risk -->
python -c 'from lab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'
<!-- Volatility -->
python -c 'from lab.volatility.calculator import calculate; print(calculate("SPY"))'
<!-- Signal -->
python -m lab.signal.scan_portfolio
python -c 'from lab.signal.lookup import lookup_signal; print(lookup_signal("EDV"))'
<!-- Trend -->
python -c 'from lab.trend.analyze import analyze; print(analyze("SPY"))'