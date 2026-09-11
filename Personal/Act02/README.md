# Act 02 — Modelo de Roll (1984)

Estimacion del bid-ask spread y reconstruccion del precio eficiente en BTC,
usando el modelo de Roll, sobre datos de velas de 5 minutos.

## Datos

- Archivo: `data/btc_project_train.csv`
- Rango: 2022-06-01 a 2023-12-31
- Observaciones (tras limpiar NaN): 162,705
- Precio medio: 25,659.05 USD

## Resultados

**Muestra completa:** Cov(dP_t, dP_t-1) = +64.37 (positiva) -> s = nan.
No definido, porque la tendencia de BTC en este periodo (caida a 15,600,
recuperacion a 42,200) domina el efecto de bid-ask bounce.

**Ventanas moviles (N=500):** solo 28.05% de las ventanas tienen el
estimador definido (Cov < 0).

**Ventana valida (2023-07-10 a 2023-07-12):**
- s = 13.4708 USD
- sigma_u = 26.4832 USD

## Archivos

- `roll_model.py` — funciones del modelo (roll_estimator, infer_trade_direction, roll_efficient_price)
- `act02_roll_model.ipynb` — notebook con las Tareas 1-4 completas
- `outputs/roll_pt_vs_mt.png` — grafico final p_t vs m_t

## Como correrlo

```
pip install -r requirements.txt
jupyter notebook
```

