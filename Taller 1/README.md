# Taller 1 — Supervisión de Contratación Pública de Bienes

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
├── Taller 1.pdf       # Enunciado original
├── data/
│   ├── raw/           # Dataset original sin procesar (ignorado por git)
│   └── processed/     # Datos limpios/derivados (ignorado por git)
├── notebooks/         # Notebooks de análisis (ejecutar en orden numerado)
└── README.md
```
