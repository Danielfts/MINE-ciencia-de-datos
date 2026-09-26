# Plan — Taller 1: Supervisión de contratación pública de bienes

**Curso:** MINE-4101 Ciencia de Datos Aplicada · **Modalidad:** parejas · **Entrega:** repositorio público de GitHub, autocontenido, con notebooks ejecutables secuencialmente sin errores.

---

## 1. Contexto y objetivo

Como consultores de la oficina de control interno, el objetivo es **focalizar la supervisión** de los contratos de bienes (compraventa y suministros) firmados por entidades públicas colombianas (SECOP II, 2019–2025). Se busca identificar qué características del contrato (valor, modalidad, sector, tipo de entidad, destino del gasto) se asocian con **desviaciones de la ejecución**, para decidir a cuáles hacer seguimiento más cercano desde la firma.

## 2. Dataset

`secop_bienes.parquet` — **196.391 contratos × 36 columnas**, firmas 2019–2025. Pocos nulos (máx. ~1,2% en `fecha_de_inicio_del_contrato`).

## 3. Variables-objetivo (3 banderas de desviación, analizadas por separado)

El enunciado nombra tres tipos de desviación; las tratamos de forma independiente:

- **`adicion_plazo`** = `dias_adicionados` > 0 (y su magnitud, recortando outliers).
- **`subejecucion`** = `valor_pagado` / `valor_del_contrato` bajo un umbral, **solo en contratos con ejecución completable** (ver decisión de periodo).
- **`sin_liquidar`** = `liquidaci_n` == "No" en contratos terminados/cerrados.

## 4. Decisión de periodo → la define el EDA

El rango cubre 7 años y no todos son comparables. Se observó que >50% de los contratos tienen `valor_pagado`=0 y ~51k están "En ejecución" (2024–2025 aportan ~75k). Para que **subejecución** y **no-liquidación** sean medibles, el periodo se fijará en el notebook `01` a partir de una tabla **año × estado × % pagado=0**, con justificación escrita. Hipótesis de trabajo: el corte caerá en contratos cerrados/terminados (aprox. 2019–2023); se confirma con evidencia, no a priori.

## 5. Problemas de calidad identificados (a tratar de forma justificada)

| Problema | Evidencia | Tratamiento previsto |
|---|---|---|
| Encoding roto | `M�nima cuant�a`, `En ejecuci�n` | Reparar codificación (latin-1 ↔ utf-8) |
| Outliers de valor | `valor_del_contrato` máx = 1.28e16; media 6.6e10 vs mediana 33.6M | Winsorizar / filtrar; usar mediana y escala log |
| `dias_adicionados` absurdos | máx = 14.276 días (~39 años) | Tope lógico / recorte por percentil |
| Valores ≤ 0 | 188 contratos con `valor_del_contrato` ≤ 0 | Marcar/eliminar justificadamente |
| `valor_pendiente_de_pago` negativo | mín = -84M | Revisar y tratar |
| `duraci_n_del_contrato` como texto | "245 Dia(s)", "5 Mes(es)", "No definido" | Parsear a días numéricos |

## 6. Estrategia de análisis y técnicas

- **Estadística descriptiva:** univariado del top-5 de atributos; tasas de desviación por categoría.
- **Pruebas de hipótesis:** χ² de independencia (categóricas vs cada bandera), Mann-Whitney / Kruskal-Wallis (valor vs desviación), comparación de proporciones. Se reportan resultados **significativos y no significativos**.
- **Visualización multivariada:** relaciones entre valor, modalidad, destino, sector y las banderas de desviación.

### Hipótesis candidatas (se refinan con datos)
- Mínima cuantía → mayor tasa de adiciones de plazo.
- Inversión se liquida menos que funcionamiento.
- A mayor valor del contrato → mayor probabilidad de adición.
- Orden territorial vs nacional difiere en subejecución.
- PyME vs no-PyME en tasa de desviación.

## 7. Entregables (mapeo a la rúbrica)

1. **[20%] Entendimiento inicial** — dimensiones, tipos, nulos; top-5 atributos con univariado; decisión de periodo con evidencia; catálogo de calidad + tratamiento.
2. **[15%] Estrategia** — definición de las 3 banderas, acotación de periodo y arsenal estadístico/visual, con justificación.
3. **[40%] Desarrollo** — limpieza reproducible, construcción de métricas, contraste de hipótesis explícitas, insights (significativos y no).
4. **[25%] Resultados** — informe ejecutivo con criterios de focalización basados en datos + limitaciones.

## 8. Organización del repositorio

```
TALLER 1/
├─ data/                     # secop_bienes.parquet (+ parquet limpio generado)
├─ notebooks/
│  ├─ 01_entendimiento.ipynb # Entregable 1 + decisión de periodo
│  ├─ 02_limpieza.ipynb      # Encoding, outliers, banderas → parquet limpio
│  └─ 03_analisis.ipynb      # Hipótesis, pruebas, visualización (Entregables 2 y 3)
├─ figs/                     # Figuras exportadas
├─ informe_ejecutivo         # Entregable 4
├─ PLAN.md
└─ README.md                 # Integrantes, objetivo, alcance, insights, ejecución, dependencias
```

**Orden de ejecución:** `01 → 02 → 03`.

## 9. Estado

- [x] Lectura del enunciado y del dataset
- [x] EDA preliminar (dimensiones, tipos, nulos, distribuciones clave, problemas de calidad)
- [x] Planeación
- [x] Notebook 01 — Entendimiento inicial + decisión de periodo (ejecutado sin errores)
- [x] Notebook 02 — Limpieza y construcción de banderas (ejecutado sin errores; genera `data/secop_bienes_limpio.parquet`)
- [ ] Notebook 03 — Análisis e hipótesis
- [ ] Informe ejecutivo + README
