# Act01 — Reading a Book, Pricing a Trade

Barras de 1 minuto de AAPL (líquido) y SIF (ilíquido), proxy de tightness
y simulación GBM.

## Estructura

- `scripts/explore_tickers.py` — selección de tickers por métricas de liquidez
- `scripts/download_data.py` — descarga y congela las sesiones en `data/`
- `src/` — código sin red que importa el notebook
- `tests/` — prueba de la identidad media/mediana
- `act01_activity.ipynb` — entregable

## Cómo correrlo

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name act01
jupyter notebook
```

