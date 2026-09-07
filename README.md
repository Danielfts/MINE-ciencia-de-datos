# Ciencia de Datos — Talleres

Repositorio para los talleres (workshops) del curso de Ciencia de Datos. Cada taller vive en su
propia carpeta (por ejemplo `Taller 1/`) con sus propios datos y notebooks, y todos comparten un
único entorno de Python con las librerías generales de ciencia de datos.

## Estructura

```
.
├── Taller 1/
│   ├── Taller 1.pdf      # Enunciado del taller
│   ├── data/
│   │   ├── raw/          # Datos crudos, sin procesar (ignorados por git)
│   │   └── processed/    # Datos limpios/derivados (ignorados por git)
│   └── notebooks/        # Notebooks de exploración y desarrollo
├── requirements.txt      # Dependencias para pip / venv
└── environment.yml        # Dependencias equivalentes para conda
```

Al agregar un nuevo taller, crea una carpeta `Taller N/` con su enunciado y sus propias
subcarpetas `data/` y `notebooks/`, siguiendo el mismo patrón que `Taller 1/`.

## Configuración del entorno

Puedes usar **pip** o **conda**, según tu preferencia.

### Opción A: pip + venv

```bash
python3 -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Opción B: conda

```bash
conda env create -f environment.yml
conda activate ciencia-de-datos
```

Para actualizar el entorno conda tras editar `environment.yml`:

```bash
conda env update -f environment.yml --prune
```

## Librerías incluidas

- **Análisis de datos:** numpy, pandas, scipy
- **Visualización:** matplotlib, seaborn, plotly
- **Machine learning / estadística:** scikit-learn, statsmodels
- **Notebooks:** jupyterlab, notebook, ipykernel
- **Utilidades:** openpyxl, requests, tqdm, python-dotenv

## Uso de Jupyter

Con el entorno activado:

```bash
jupyter lab
```

## Datos

Las carpetas `data/raw/` y `data/processed/` están en `.gitignore` para mantener el repositorio
liviano. Si necesitas versionar un dataset pequeño de ejemplo, agrégalo explícitamente con
`git add -f`.
