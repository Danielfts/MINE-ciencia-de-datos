# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Coursework for MINE-4101 *Ciencia de Datos Aplicada* (Uniandes), done in pairs. Each workshop lives in its own
`Taller N/` folder (statement PDF, `data/raw`, `data/processed`, `notebooks/`, `figs/`), and they all share one
Python environment defined at the repo root. All prose, notebook markdown, variable names and commit messages
are in **Spanish**. Keep that convention.

Deliverables are graded on a public GitHub repo that must be **self-contained**, with notebooks that **run
sequentially without errors**.

## Environment

```bash
conda env create -f environment.yml && conda activate ciencia-de-datos   # or: pip install -r requirements.txt
conda env update -f environment.yml --prune                             # after editing deps
```

When you add a dependency, add it to **both** `requirements.txt` and `environment.yml`. `pyarrow` is needed for
the `.parquet` I/O.

There are no tests, linters or build steps. To check that a notebook still runs from start to finish, execute it
headless from its own directory. Notebooks use relative paths like `../data/...` and `../figs`, so the working
directory must be `notebooks/`:

```bash
cd "Taller 1/notebooks"
jupyter nbconvert --to notebook --execute --inplace 02_limpieza.ipynb
```

## Data

`data/raw/*` and `data/processed/*` are gitignored. Only the `.gitkeep` files are tracked. For Taller 1, the raw
dataset `secop_bienes.parquet` (196,391 × 36, SECOP II contracts 2019–2025) is downloaded from the Drive link in
`Taller 1/README.md`. If you need to version a small sample on purpose, use `git add -f`.

## Taller 1 architecture (notebooks are a pipeline: 01 → 02 → 03)

- **`01_entendimiento`** is the full detail behind Deliverable 1. It covers dimensions and types, univariate
  analysis of the top 5 attributes, the evidence for the period cut, and data quality (section 4). It reads raw
  data only. Section 4 walks the quality levels (atributo → registro → columna → tabla → múltiples tablas) and
  tags each finding with a course dimension. Every check calls `registrar(...)`, and the catalog in 4.7 is built
  from those calls, so add new checks the same way.
- **`02_limpieza`** reads raw data and writes `data/processed/secop_bienes_limpio.parquet`, which is the only
  input to 03. It keeps the original columns and adds derived ones (suffixes `_clean`, `_w`, `_bool`, `_log`).
  Key decisions:
  - `valor_del_contrato` ≤ 0 becomes NaN. Values are winsorized at P99.9 (`_w`), and `valor_log` is log10.
  - `dias_adicionados` is capped at 1,095 days for magnitude. The binary flag uses the raw value.
  - `duraci_n_del_contrato` is free text and is parsed to `duracion_dias`.
  - `ANIO_CORTE = 2023`: `periodo_analisis = anio_firma <= 2023`, and
    `ciclo_cerrado = estado_contrato in {Terminado, Cerrado}`.
  - **Three deviation flags, each with its own denominator.** Rows outside the base are NaN, so never compare
    the rates directly:
    - `adicion_plazo = dias_adicionados > 0`, computed on all rows. In 03 the base is `periodo_analisis`.
    - `subejecucion = facturado/valor < 0.9`, only when `ciclo_cerrado & periodo & valor_facturado > 0`.
    - `sin_liquidar = liquidaci_n == "no"`, only when `ciclo_cerrado & periodo`.
  - Encoding is already correct UTF-8. The `�` seen in the console is a display artifact, so do not "fix" it.
- **`03_analisis`** is Deliverables 2 and 3. It builds `base_adic`, `base_sub` and `base_liq` from the flags'
  non-null masks. The shared helpers are `test_categorica` (χ² + Cramér's V, which reports category rates with
  n ≥ 200) and `test_valor` (Mann-Whitney on `valor_log`). The significance level is `ALPHA = 0.05`. Hypotheses
  H1–H8 report both significant **and** non-significant results, which the rubric requires.
- **`informe/informe_ejecutivo.tex`** (and its committed PDF) holds two deliverables in one file. The executive
  report (Deliverable 4) comes first: a plain-language report of the targeting criteria and the limitations of
  the analysis. At the end, a technical annex (Deliverable 1) is a brief summary of notebook 01. The annex quotes
  numbers from 01's outputs, so update it when 01 changes. The report pulls figures from `../figs/` through
  `\graphicspath`. `figs/` holds PNGs exported by the notebooks, named with their notebook prefix (`01_*`, `03_*`).

## Building the report

```bash
cd "Taller 1/informe" && latexmk          # XeLaTeX via .latexmkrc; aux files go to build/ (gitignored)
```

Always rebuild and commit the PDF together with any `.tex` change; graders read the PDF.
- **Fonts:** it uses Red Hat Text/Display (installed system fonts), with an automatic fallback to TeX Gyre
  Heros, so it compiles on machines without them.
- **Missing packages:** the TeX Live install is Fedora's `scheme-medium` and lacks `tikzfill`. Use core tcolorbox
  only, with no `skins`/`most`, and install missing packages with `dnf install texlive-<pkg>`, not `tlmgr`.
- **Special characters:** write `~`, `≤`, `×` and `≈` as `\apx`, `$\leq$`, `$\times$` and `$\approx$`. Write
  dataset column names with `\col{...}`, which allows line breaks at underscores.
- `Taller 1/README.md` summarizes the conclusions and status. Update it when findings change.

## Conventions in the notebooks

- Numbers quoted in markdown cells must come from a preceding code cell that computes and prints them, so the
  text never drifts from the data. Keep the "~" approximations in prose consistent with those outputs.
- Every notebook starts with the same setup block (pandas display options, `sns.set_theme(style='whitegrid')`,
  path constants in uppercase such as `RUTA_*`). Figures are saved with
  `plt.savefig(f'{RUTA_FIGS}/NN_name.png', bbox_inches='tight')`.
