# Taller 2 — Predicción de abandono de clientes para FinAlpes

**Integrantes:** Daniel Triviño · Nicolás Bedoya

**Dataset:** [`churn.csv`](churn.csv), incluido en el repositorio: 10.045 clientes × 11 columnas.

## Enunciado

FinAlpes es una fintech colombiana que ofrece analítica a bancos, cooperativas y aseguradoras. Nos contrata para una
prueba de concepto: una herramienta que prediga qué clientes van a abandonar la entidad (*churn*) a partir de su perfil
comercial, para dirigirles campañas de retención. La muestra es de clientes europeos de un banco. El modelo debe
adaptarse a un banco colombiano con estos supuestos:
- 20.000 clientes y una tasa de abandono minorista de \~15 %;
- la campaña convence al 30 % de los clientes que iban a abandonar, pero se paga por todos los contactados;
- el ingreso anual por cliente activo es de COP 500.000 a 900.000.

<!-- TODO: revisar la redacción del enunciado. -->

## Entregables

1. **[10%] Entendimiento y preparación de los datos.** Dimensiones, tipos de variables, distribuciones e indicadores.
2. **[15%] Entrenamiento del modelo.** Al menos dos modelos, con la partición de datos, la búsqueda de
   hiperparámetros y la selección documentadas.
3. **[20%] Análisis cuantitativo.** Métricas, su significado para la empresa, la justificación del modelo elegido y
   las oportunidades de mejora.
4. **[20%] Análisis cualitativo.** Interpretación global y de predicciones individuales.
5. **[20%] Generación de valor.** Ganancia esperada por predicción, punto de equilibrio, supuestos con fuentes y
   limitaciones.
6. **[10%] Insights.** Informe ejecutivo con los hallazgos y una recomendación final.
7. **[5%] Declaración de uso de IA generativa.** Modelos, porcentaje de ayuda y prompts.

## Organización

```
Taller 2/
├── Taller2.pdf                     # Enunciado original
├── churn.csv                       # Dataset (incluido)
├── declaracion_IA.md               # Entregable 7
├── informe/
│   ├── informe_ejecutivo.pdf       # Entregable 6, con anexo técnico de los Entregables 1 a 5
│   └── informe_ejecutivo.tex       # Fuente LaTeX (se compila con XeLaTeX)
├── data/processed/                 # Generados por los notebooks (ignorados por git)
│   ├── churn_limpio.parquet        # 02
│   ├── churn_particion.parquet     # 04: partición entrenamiento/prueba
│   └── modelos/                    # 04: modelos ajustados + seleccion.json
├── notebooks/
│   ├── calidad.py                  # Funciones de calidad de datos (usadas por 01 y 02)
│   ├── 01_entendimiento.ipynb      # Entregable 1: perfilado, tipos y calidad
│   ├── 02_limpieza.ipynb           # Entregable 1: tratamiento → churn_limpio.parquet
│   ├── 03_exploracion.ipynb        # Entregable 1: distribuciones y relación con el churn
│   ├── 04_modelado.ipynb           # Entregable 2: partición, desbalance, hiperparámetros, selección
│   ├── 05_evaluacion.ipynb         # Entregable 3: métricas en prueba, IC, comparación, calibración
│   ├── 06_interpretabilidad.ipynb  # Entregable 4 (TODO)
│   └── 07_valor.ipynb              # Entregable 5 (TODO)
├── figs/                           # Figuras exportadas por los notebooks (prefijo = notebook)
└── README.md
```

## Instrucciones de ejecución

1. Crear el entorno desde la raíz del repositorio (`requirements.txt` o `environment.yml`).
2. Ejecutar los notebooks **en orden**, desde la carpeta `notebooks/`:
   1. `01_entendimiento.ipynb`
   2. `02_limpieza.ipynb` → genera `data/processed/churn_limpio.parquet`
   3. `03_exploracion.ipynb`
   4. `04_modelado.ipynb` → genera la partición y los modelos en `data/processed/`. Tarda unos minutos por la búsqueda
      de hiperparámetros.
   5. `05_evaluacion.ipynb`
   6. `06_interpretabilidad.ipynb` <!-- TODO -->
   7. `07_valor.ipynb` <!-- TODO -->
3. Leer el **[informe ejecutivo](informe/informe_ejecutivo.pdf)** (Entregable 6).

El PDF del informe ya está en el repositorio. Para regenerarlo hace falta LaTeX con XeLaTeX (por ejemplo, TeX Live):
desde `informe/` se ejecuta `latexmk`.

## Conclusiones (insights)

<!-- TODO: completar con los resultados del 06 y el 07 y revisar la redacción. Las cifras del 05 ya están verificadas. -->

- **Modelo elegido: XGBoost.** Es el que mejor ordena a los clientes por riesgo. En prueba obtiene PR-AUC 0,662
  (IC 95 % 0,62–0,70), 3,2 veces la línea base, y supera de forma relevante a la regresión logística. Frente a la SVM
  ordena mejor, pero en el punto de operación la diferencia no es concluyente.
- **Para la campaña:** con su umbral contacta al 18 % de los clientes; 6 de cada 10 contactados sí iban a abandonar, y
  se alcanza a más de la mitad de los que abandonan. El 10 % más riesgoso concentra el 38 % de los abandonos.
- **Probabilidades calibradas.** Se pueden usar directamente para calcular la ganancia esperada.
- **Auditoría:** el modelo subestima el riesgo en Alemania y en mujeres, variables que no entran al modelo por
  decisión ética. Hay que revisarlo antes de desplegar.
- **Cómo decide el modelo:** <!-- TODO (06) -->
- **Valor para el banco:** <!-- TODO (07): ganancia esperada por predicción, punto de equilibrio, sensibilidad -->
- **Recomendación:** <!-- TODO -->

Detalle en el **[informe ejecutivo](informe/informe_ejecutivo.pdf)**.

> **Estado:** Entregables 1, 2 y 3 completos (notebooks 01–05). Pendientes: 4 (06), 5 (07), 6 (informe, solo esqueleto)
> y 7 (declaración, en borrador).
