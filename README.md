Commands:

<!-- Donchian -->
python -c 'from fractalmarketslab.donchian.calculator import calculate; print(calculate("CHWY"))'
<!-- Value at Risk -->
python -c 'from fractalmarketslab.VaR.calculator import variancecovarianceVaR; print(variancecovarianceVaR("SPY"))'
<!-- Volatility -->
python -c 'from fractalmarketslab.volatility.calculator import calculate; print(calculate("SPY"))'
<!-- Portfolio -->
python -m fractalmarketslab.portfolio.donchian