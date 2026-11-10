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

## Objetivo y alcance

**Objetivo:** construir un modelo que prediga qué clientes van a abandonar el banco. También busca explicar cómo
decide y estimar cuánto valor genera una campaña de retención dirigida con él.

**Alcance:**
- **Qué cubre:** una prueba de concepto con la muestra europea del enunciado. Incluye limpieza, comparación de tres
  modelos de clasificación (regresión logística, SVM y XGBoost), evaluación en un conjunto de prueba reservado,
  interpretabilidad (ICE, LIME y SHAP) y un cálculo paramétrico de valor para un banco colombiano promedio.
- **Qué no cubre:** el despliegue del modelo ni la validación con datos de un banco colombiano.
- **Variables excluidas:** el modelo no usa el género ni el país del cliente, por decisión ética.

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
│   ├── informe_ejecutivo.pdf       # Entregable 6 (2 páginas; el detalle está en los notebooks)
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
│   ├── 06_interpretabilidad.ipynb  # Entregable 4: ICE, LIME, SHAP y comparación de técnicas
│   └── 07_valor.ipynb              # Entregable 5: valor esperado (Provost), punto de equilibrio, sensibilidad
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
   6. `06_interpretabilidad.ipynb`
   7. `07_valor.ipynb`
3. Leer el **[informe ejecutivo](informe/informe_ejecutivo.pdf)** (Entregable 6).

El PDF del informe ya está en el repositorio. Para regenerarlo hace falta LaTeX con XeLaTeX (por ejemplo, TeX Live):
desde `informe/` se ejecuta `latexmk`.

## Dependencias

Python 3.12 con el entorno de la raíz del repositorio ([`requirements.txt`](../requirements.txt) o
[`environment.yml`](../environment.yml)). Las principales librerías de este taller son:
- **Datos:** pandas, numpy y pyarrow (archivos `.parquet`);
- **Modelos:** scikit-learn, xgboost e imbalanced-learn (SMOTE);
- **Estadística:** scipy y statsmodels (McNemar);
- **Interpretabilidad:** shap y lime;
- **Gráficos:** matplotlib y seaborn.

Las instrucciones de instalación (uv, pip o conda) están en el [README de la raíz](../README.md).

## Conclusiones (insights)

- **Modelo elegido: XGBoost.** Es el que mejor ordena a los clientes por riesgo. En prueba obtiene PR-AUC 0,662
  (IC 95 % 0,62–0,70), 3,2 veces la línea base, y supera de forma relevante a la regresión logística. Frente a la SVM
  ordena mejor, pero en el punto de operación la diferencia no es concluyente.
- **Para la campaña:** con su umbral (0,33), en la muestra de prueba contacta al 18 % de los clientes; 6 de cada 10
  contactados sí iban a abandonar, y se alcanza a más de la mitad de los que abandonan. El 10 % más riesgoso concentra
  el 38 % de los abandonos.
- **Probabilidades calibradas.** Se pueden usar directamente para calcular la ganancia esperada.
- **Auditoría:** el modelo subestima el riesgo en Alemania y en mujeres, variables que no entran al modelo por
  decisión ética. Hay que revisarlo antes de desplegar.
- **Cómo decide el modelo:** la edad, el número de productos y la actividad suman el 90 % de la importancia SHAP.
  - **Edad:** el riesgo sube hasta los 50–59 años y luego baja.
  - **Productos:** 2 productos es lo más protector; 3 o 4 disparan el riesgo.
  - **Actividad:** la inactividad sube el riesgo y amplifica el efecto de la edad. A los 55 años, el riesgo medio es
    del 68 % en inactivos y del 30 % en activos.

  ICE, LIME, SHAP y la regresión logística coinciden. Son asociaciones, no causas.
- **Valor para el banco:** para un banco de 20.000 clientes con 15 % de abandono, el modelo deja \~COP 13.500 por
  cliente evaluado y por año (\~COP 271 millones al año) y recupera una inversión de \~COP 61 millones en \~2,7 meses.
  Es rentable mientras la precisión supere 0,11 (la del modelo es 0,52). El resultado depende sobre todo del costo de
  la oferta, que hay que confirmar con un piloto. Fijar el umbral por ganancia (\~0,15) en lugar de por F1 sube la
  ganancia \~18 %, pero implica contactar al 40 % de la base.
- **Recomendación:** implementar el modelo como piloto. Se contactaría a los clientes con riesgo ≥ 0,33 (\~16 % de
  la base del banco, que abandona menos que la muestra) y se reservaría un grupo de control sin oferta. El piloto
  sirve para medir el costo real de la oferta y la tasa real de retención, que hoy son supuestos. Antes de escalar, hay que reentrenar con clientes del propio banco y
  sumar datos de comportamiento (transacciones, reclamos, uso de canales).

Detalle en el **[informe ejecutivo](informe/informe_ejecutivo.pdf)**. Las limitaciones están en el informe y en la
sección 7 del `07_valor`.

## Declaración de uso de IA generativa

Está en [`declaracion_IA.md`](declaracion_IA.md) (Entregable 7).
