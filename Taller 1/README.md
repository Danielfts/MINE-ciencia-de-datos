# Taller 1 — Supervisión de Contratación Pública de Bienes

**Integrantes:** Daniel Triviño · Nicolás Bedoya

**Dataset:** [Contratos de bienes SECOP II (2019-2025)](https://drive.google.com/file/d/1R0pSXh2bgCoPKcXlAlafdavVwvzZX6AQ/view)

## Enunciado

Actuamos como consultores de ciencia de datos para la oficina de control interno de una
entidad del Estado, que busca focalizar la supervisión de los contratos públicos de compra de
bienes (compraventa y suministros). Dado que el equipo de supervisión es pequeño frente al
volumen de contratos firmados cada año, se necesita identificar qué características de un
contrato (valor, modalidad de contratación, sector, tipo de entidad, destino del gasto, entre
otras) se asocian con desviaciones en su ejecución —adiciones de plazo, presupuesto no
ejecutado, cierre sin liquidar— para priorizar el seguimiento desde el momento de la firma.

El dataset provisto contiene contratos de bienes firmados por entidades públicas colombianas
entre 2019 y 2025, extraído de SECOP II (Sistema Electrónico de Contratación Pública). Incluye
atributos como valor del contrato, valor efectivamente pagado, días adicionados al plazo,
modalidad de contratación, sector y orden de la entidad, departamento, tipo de proveedor y
destino del gasto. Al cubrir siete años, no todos los periodos son necesariamente comparables
entre sí, por lo que parte del trabajo consiste en justificar qué rango temporal usar para el
análisis. Son datos administrativos reales, por lo que pueden tener problemas de calidad que
deben identificarse y tratarse de forma justificada.

## Entregables

1. **[20%] Entendimiento inicial de datos** — Reporte con las dimensiones del dataset, los
   tipos de datos, el top 5 de atributos más relevantes para el análisis con su comportamiento
   o distribución (análisis univariado), y los problemas de calidad de datos identificados junto
   con el tratamiento dado.
2. **[15%] Estrategia de análisis** — Descripción concreta (uno o dos párrafos) de la estrategia
   y técnicas a usar —desde estadísticos básicos hasta pruebas de hipótesis y visualización
   multivariada— para identificar qué contratos deberían recibir supervisión más cercana.
3. **[40%] Desarrollo de la estrategia** — Implementación de la estrategia definida: procesamiento
   de datos, técnicas estadísticas y de visualización aplicadas, hipótesis formuladas y
   contrastadas, e insights extraídos (reportando resultados significativos y no significativos).
4. **[25%] Generación de resultados** — Informe ejecutivo o presentación corta con criterios de
   focalización de supervisión recomendados (valor del contrato, modalidad, destino del gasto,
   sector, entre otros), basados en datos, incluyendo las limitaciones del análisis.

## Organización

```
Taller 1/
├── Taller 1.pdf                    # Enunciado original
├── informe/
│   ├── informe_ejecutivo.pdf       # Entregable 4 (criterios + limitaciones) y anexo con el Entregable 1
│   └── informe_ejecutivo.tex       # Fuente LaTeX del informe (se compila con XeLaTeX)
├── data/
│   ├── raw/                        # Dataset original sin procesar (ignorado por git)
│   │   └── secop_bienes.parquet    # (descargar del enlace de arriba y ubicar aquí)
│   └── processed/                  # Datos derivados, generados por 02 (ignorado por git)
│       └── secop_bienes_limpio.parquet
├── notebooks/
│   ├── 01_entendimiento.ipynb      # Entregable 1: entendimiento inicial + decisión de periodo
│   ├── 02_limpieza.ipynb           # Limpieza + construcción de las 3 banderas de desviación
│   └── 03_analisis.ipynb           # Entregables 2 y 3: estrategia, hipótesis (χ²/Mann-Whitney), visualización
├── figs/                           # Figuras exportadas por los notebooks
└── README.md
```

## Instrucciones de ejecución

1. Descargar el dataset del enlace de arriba y ubicarlo en `data/raw/secop_bienes.parquet`.
2. Ejecutar los notebooks **secuencialmente**:
   1. `notebooks/01_entendimiento.ipynb`
   2. `notebooks/02_limpieza.ipynb` → genera `data/processed/secop_bienes_limpio.parquet`
   3. `notebooks/03_analisis.ipynb`

4. Leer el **[informe ejecutivo](informe/informe_ejecutivo.pdf)** (Entregable 4) con las conclusiones y recomendaciones; su
   anexo técnico resume el entendimiento inicial de los datos (Entregable 1).

Dependencias en `requirements.txt` / `environment.yml` (raíz del repo).

El PDF del informe ya está en el repositorio. Para regenerarlo hace falta una distribución de LaTeX con XeLaTeX
(por ejemplo, TeX Live); desde `informe/` se ejecuta `latexmk`.

## Conclusiones (insights)

- El **valor** del contrato anticipa riesgo, pero en dirección distinta según la desviación: los grandes piden
  más plazo y ejecutan menos; los pequeños se cierran sin liquidar.
- La **modalidad** predice las adiciones de plazo (licitación ~20% vs mínima cuantía ~5%).
- El **tipo de contrato** marca la no-ejecución (suministros ~13% vs compraventa ~2%).
- La **no-liquidación** es masiva (~59%): no sirve para triage, sí como alerta de proceso en Salud y entidades
  territoriales.
- El **tamaño del proveedor (PyME)** no discrimina: no conviene usarlo como criterio.
- **Perfil de mayor riesgo:** suministros de funcionamiento en modalidades de mayor cuantía (~2× el promedio).

Detalle y recomendaciones priorizadas en el **[informe ejecutivo](informe/informe_ejecutivo.pdf)**.

> **Estado:** completos los cuatro entregables (notebooks 01–03 + informe ejecutivo).
