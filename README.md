# Ciencia de Datos — Talleres

Repositorio de los talleres del curso MINE-4101 *Ciencia de Datos Aplicada* (Universidad de los Andes, 2026-20).

**Integrantes:** Daniel Triviño · Nicolás Bedoya

Cada taller vive en su propia carpeta, con su enunciado, datos, notebooks, figuras, informe y README. Todos comparten un
único entorno de Python definido en la raíz.

| Taller | Tema | README |
|---|---|---|
| Taller 1 | Supervisión de la contratación pública de bienes (SECOP II): calidad de datos, pruebas de hipótesis y criterios de focalización | [Taller 1/README.md](Taller%201/README.md) |
| Taller 2 | Predicción de abandono de clientes bancarios para FinAlpes: modelos de clasificación, evaluación, interpretabilidad y generación de valor | [Taller 2/README.md](Taller%202/README.md) |

## Estructura

```
.
├── Taller 1/
│   ├── Taller 1.pdf          # Enunciado
│   ├── data/                 # raw/ y processed/ (ignorados por git; ver su README para descargar el dataset)
│   ├── notebooks/            # 01 → 03, se ejecutan en orden
│   ├── figs/                 # Figuras exportadas por los notebooks
│   ├── informe/              # Informe ejecutivo (LaTeX + PDF)
│   ├── referencias/          # Fuentes oficiales para interpretar los datos
│   └── README.md
├── Taller 2/
│   ├── Taller2.pdf           # Enunciado
│   ├── churn.csv             # Dataset (incluido)
│   ├── data/processed/       # Generados por los notebooks (ignorados por git)
│   ├── notebooks/            # 01 → 07, se ejecutan en orden
│   ├── figs/
│   ├── informe/              # Informe ejecutivo (LaTeX + PDF)
│   ├── declaracion_IA.md     # Declaración de uso de IA generativa
│   └── README.md
├── requirements.txt          # Dependencias para pip / uv
└── environment.yml           # Dependencias equivalentes para conda
```

## Configuración del entorno

Se puede usar **uv**, **pip** o **conda**. Los tres instalan lo mismo; `requirements.txt` y `environment.yml` se
mantienen sincronizados.

### Opción A: uv (recomendada)

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r requirements.txt
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

# Registrar el kernel para Jupyter / VS Code (una sola vez)
python -m ipykernel install --user --name ciencia-de-datos --display-name "Python 3.12 (ciencia-de-datos, uv)"
```

En VS Code, seleccione el intérprete `.venv/bin/python` o el kernel "Python 3.12 (ciencia-de-datos, uv)".

### Opción B: pip + venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Opción C: conda

```bash
conda env create -f environment.yml
conda activate ciencia-de-datos
```

Para actualizar el entorno conda tras editar `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

## Librerías incluidas

- **Análisis de datos:** numpy, pandas (2.x), scipy, pyarrow (lectura y escritura de `.parquet`)
- **Visualización:** matplotlib, seaborn, plotly
- **Machine learning / estadística:** scikit-learn, statsmodels, xgboost, imbalanced-learn
- **Interpretabilidad:** shap, lime
- **Notebooks:** jupyterlab, notebook, ipykernel
- **Utilidades:** openpyxl, requests, tqdm, python-dotenv

## Ejecución

Los notebooks están versionados **con sus salidas**, así que se pueden leer en GitHub sin ejecutarlos. Para
reproducirlos, con el entorno activado, se ejecutan **en orden** desde su carpeta `notebooks/`, porque
usan rutas relativas como `../data` y `../figs`. El orden está en el README de cada taller. Para comprobar que un
notebook corre de principio a fin sin interfaz:

```bash
cd "Taller 2/notebooks"
jupyter nbconvert --to notebook --execute --inplace 01_entendimiento.ipynb
```

Los informes ejecutivos (PDF) ya están en el repositorio. Para regenerarlos hace falta LaTeX con XeLaTeX (por ejemplo,
TeX Live): desde la carpeta `informe/` de cada taller se ejecuta `latexmk`.

## Datos

Las carpetas `data/raw/` y `data/processed/` están en `.gitignore` para mantener el repositorio liviano.
- **Taller 1:** el dataset se descarga del enlace en su README.
- **Taller 2:** el dataset (`churn.csv`) está incluido.

Los archivos de `data/processed/` los generan los notebooks.
