"""Funciones reutilizables para evaluar la calidad de un DataFrame en cuatro dimensiones:
completitud, unicidad, validez y consistencia.

Todas las funciones de chequeo devuelven una tabla de hallazgos con las mismas columnas
(`COLUMNAS_HALLAZGO`), para poder juntarlas en un solo catálogo con `catalogo(...)`.
Ninguna modifica el DataFrame: solo diagnostican.

Uso típico:

    import calidad as cal
    cat = cal.catalogo(
        cal.completitud(df),
        cal.unicidad(df)[0],
        cal.validez_tipos(df, ESQUEMA),
        cal.consistencia_formato(df)[0],
    )
"""

import unicodedata

import numpy as np
import pandas as pd

COLUMNAS_HALLAZGO = ['dimension', 'columna', 'chequeo', 'n_afectados', 'pct_afectados', 'ejemplos']
ORDEN_DIMENSIONES = ['completitud', 'unicidad', 'validez', 'consistencia']
TIPOS_VALIDOS = {'continua', 'discreta', 'categorica', 'binaria'}


# ----------------------------------------------------------------------------------------------
# Utilidades internas
# ----------------------------------------------------------------------------------------------

def _es_texto(serie):
    return serie.dtype == object or pd.api.types.is_string_dtype(serie.dtype)


def _normalizar(valor):
    """Texto sin espacios en los extremos, en minúscula y sin tildes. Lo que no es texto queda igual."""
    if not isinstance(valor, str):
        return valor
    texto = unicodedata.normalize('NFKD', valor.strip().lower())
    return ''.join(c for c in texto if not unicodedata.combining(c))


def _ejemplos(valores, n=6):
    """Hasta `n` valores distintos como texto. Si hay muchos y son números, muestra los extremos."""
    unicos = pd.Series(valores).dropna().unique()
    if len(unicos) == 0:
        return ''
    if pd.api.types.is_numeric_dtype(unicos.dtype):
        unicos = np.sort(unicos)
    if len(unicos) > n and pd.api.types.is_numeric_dtype(unicos.dtype):
        mitad = n // 2
        return ', '.join(map(str, unicos[:mitad])) + ' ... ' + ', '.join(map(str, unicos[-mitad:]))
    return ', '.join(map(str, unicos[:n]))


def _fila(dimension, columna, chequeo, n, total, ejemplos=''):
    n = np.nan if n is None else int(n)
    pct = round(100 * n / total, 2) if (total and not pd.isna(n)) else np.nan
    return {'dimension': dimension, 'columna': columna, 'chequeo': chequeo,
            'n_afectados': n, 'pct_afectados': pct, 'ejemplos': ejemplos}


def _a_tabla(filas):
    tabla = pd.DataFrame(filas, columns=COLUMNAS_HALLAZGO)
    tabla['n_afectados'] = tabla['n_afectados'].astype('Int64')   # entero que admite "sin conteo"
    return tabla


# ----------------------------------------------------------------------------------------------
# Completitud: ¿están todos los datos?
# ----------------------------------------------------------------------------------------------

def completitud(df, vacios_como_nulos=True):
    """Valores faltantes por columna.

    Si `vacios_como_nulos` es True, en las columnas de texto también cuenta como faltante el texto
    vacío o con solo espacios (pandas no siempre lo convierte a nulo).
    """
    total = len(df)
    filas = []
    for col in df.columns:
        faltante = df[col].isna()
        if vacios_como_nulos and _es_texto(df[col]):
            faltante = faltante | df[col].str.strip().eq('').fillna(False).astype(bool)
        filas.append(_fila('completitud', col, 'valores faltantes', faltante.sum(), total))
    return _a_tabla(filas)


def completitud_filas(df):
    """Faltantes por fila.

    Devuelve (hallazgos, distribucion): el hallazgo de filas con al menos un faltante y una tabla de
    cuántas filas tienen 0, 1, 2... faltantes. Sirve para saber si los faltantes se concentran en
    pocas filas (y se podrían descartar) o están repartidos.
    """
    n_por_fila = df.isna().sum(axis=1)
    distribucion = (n_por_fila.value_counts().sort_index()
                    .rename_axis('faltantes_en_la_fila').rename('n_filas').to_frame())
    hallazgos = _a_tabla([_fila('completitud', '(fila)', 'filas con al menos un faltante',
                                (n_por_fila > 0).sum(), len(df))])
    return hallazgos, distribucion


# ----------------------------------------------------------------------------------------------
# Unicidad: ¿hay registros repetidos?
# ----------------------------------------------------------------------------------------------

def unicidad(df, subset=None, normalizar_texto=False):
    """Filas duplicadas.

    Cuenta como afectadas las copias sobrantes (deja la primera aparición de cada fila).
    - `subset`: columnas a comparar; por defecto, todas.
    - `normalizar_texto`: si es True, compara el texto sin mayúsculas, espacios ni tildes, para
      encontrar duplicados escondidos detrás de diferencias de escritura.

    Devuelve (hallazgos, filas_duplicadas), donde `filas_duplicadas` trae todas las apariciones
    (la original y sus copias), para poder revisarlas.
    """
    datos = df if subset is None else df[subset]
    if normalizar_texto:
        datos = datos.apply(lambda s: s.map(_normalizar) if _es_texto(s) else s)
    sobrantes = datos.duplicated(keep='first')
    todas = datos.duplicated(keep=False)
    alcance = 'todas las columnas' if subset is None else ', '.join(subset)
    chequeo = 'filas duplicadas ' + ('(texto normalizado)' if normalizar_texto else '(exactas)')
    hallazgos = _a_tabla([_fila('unicidad', alcance, chequeo, sobrantes.sum(), len(df))])
    return hallazgos, df[todas]


# ----------------------------------------------------------------------------------------------
# Validez: ¿los valores tienen sentido para lo que mide la columna?
# ----------------------------------------------------------------------------------------------

def validez_tipos(df, esquema):
    """Revisa que cada columna cumpla el tipo que determinamos a mano.

    `esquema`: {columna: 'continua' | 'discreta' | 'categorica' | 'binaria' | None}
    - continua / discreta / binaria: todos los valores deben poder leerse como número.
      La discreta, además, debe ser entera; la binaria, solo 0 o 1.
    - categorica: se reportan valores que parecen números (raro en una categoría). Si sus
      categorías son las permitidas se revisa con `validez_dominio`.
    - None: tipo sin determinar; se reporta (sin conteo) para que no quede olvidado.
    Los faltantes no se cuentan aquí: eso es completitud.
    """
    total = len(df)
    filas = []
    for col, tipo in esquema.items():
        if col not in df.columns:
            raise KeyError(f"'{col}' está en el esquema pero no en los datos")
        if tipo is None:
            filas.append(_fila('validez', col, 'tipo sin determinar (no se revisó)', None, total))
            continue
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"Tipo '{tipo}' de '{col}' no válido; usar uno de {sorted(TIPOS_VALIDOS)}")
        valores = df[col].dropna()
        numeros = pd.to_numeric(valores, errors='coerce')
        if tipo == 'categorica':
            parecen_numero = numeros.notna()
            filas.append(_fila('validez', col, 'valores numéricos en una categoría',
                               parecen_numero.sum(), total, _ejemplos(valores[parecen_numero])))
            continue
        no_numericos = numeros.isna()
        filas.append(_fila('validez', col, f'no numéricos (esperado {tipo})',
                           no_numericos.sum(), total, _ejemplos(valores[no_numericos])))
        numeros = numeros.dropna()
        if tipo == 'discreta':
            no_enteros = numeros % 1 != 0
            filas.append(_fila('validez', col, 'no enteros (esperado discreta)',
                               no_enteros.sum(), total, _ejemplos(numeros[no_enteros])))
        if tipo == 'binaria':
            fuera = ~numeros.isin([0, 1])
            filas.append(_fila('validez', col, 'distintos de 0/1 (esperado binaria)',
                               fuera.sum(), total, _ejemplos(numeros[fuera])))
    faltan = [c for c in df.columns if c not in esquema]
    for col in faltan:
        filas.append(_fila('validez', col, 'columna sin tipo en el esquema', None, total))
    return _a_tabla(filas)


def validez_rangos(df, rangos, devolver_filas=False):
    """Valores numéricos fuera del rango permitido.

    `rangos`: {columna: (minimo, maximo)}; usar None en un extremo para no poner límite.
    Ej.: {'balance': (0, None)} revisa que no haya saldos negativos.
    Con `devolver_filas=True` devuelve (hallazgos, filas), donde `filas` es {columna: filas
    completas fuera del rango}; si no, solo los hallazgos.
    """
    total = len(df)
    hallazgos, filas = [], {}
    for col, (minimo, maximo) in rangos.items():
        valores = pd.to_numeric(df[col], errors='coerce')
        fuera = pd.Series(False, index=df.index)
        if minimo is not None:
            fuera |= valores < minimo
        if maximo is not None:
            fuera |= valores > maximo
        hallazgos.append(_fila('validez', col, f'fuera del rango [{minimo}, {maximo}]',
                               fuera.sum(), total, _ejemplos(valores[fuera])))
        filas[col] = df[fuera]
    hallazgos = _a_tabla(hallazgos)
    return (hallazgos, filas) if devolver_filas else hallazgos


def validez_dominio(df, dominios, equivalencias=None, devolver_filas=False):
    """Valores que no están en la lista de valores permitidos.

    `dominios`: {columna: valores permitidos}. La comparación es exacta, así que 'france' no
    cuenta como 'France': las diferencias de escritura aparecen aquí y en `consistencia_formato`.

    Además separa los valores fuera del dominio que **no corresponden a ningún valor permitido**,
    ni siquiera normalizando el texto o aplicando `equivalencias` (las mismas de
    `consistencia_formato`). Por ejemplo, con dominio {France, Germany, Spain}, 'FRANCE' es solo
    otra forma de escribir un valor válido, pero 'Italy' no tiene equivalente. Se reportan como un
    chequeo aparte ("sin equivalente en el dominio").

    Con `devolver_filas=True` devuelve (hallazgos, filas), donde `filas` es {columna: filas
    completas con valores sin equivalente}; si no, solo los hallazgos.
    """
    equivalencias = equivalencias or {}
    total = len(df)
    hallazgos, filas = [], {}
    for col, permitidos in dominios.items():
        permitidos = list(permitidos)
        valores = df[col].dropna()
        fuera = ~valores.isin(permitidos)
        hallazgos.append(_fila('validez', col, 'fuera de los valores permitidos',
                               fuera.sum(), total, _ejemplos(valores[fuera])))
        mapa = equivalencias.get(col, {})
        claves_permitidas = {_normalizar(p) for p in permitidos}
        claves = valores.map(lambda v: _normalizar(mapa.get(v, v)))
        sin_equivalente = fuera & ~claves.isin(claves_permitidas)
        hallazgos.append(_fila('validez', col, 'sin equivalente en el dominio',
                               sin_equivalente.sum(), total, _ejemplos(valores[sin_equivalente])))
        filas[col] = df.loc[valores.index[sin_equivalente]]
    hallazgos = _a_tabla(hallazgos)
    return (hallazgos, filas) if devolver_filas else hallazgos


def valores_negativos(df, columnas):
    """Valores negativos en columnas que, por lo que miden, no deberían tenerlos (edad, años, montos).

    Devuelve (hallazgos, filas), donde `filas` es un diccionario {columna: filas completas con valor
    negativo en esa columna}, para revisarlas con todas sus variables.
    """
    total = len(df)
    hallazgos, filas = [], {}
    for col in columnas:
        valores = pd.to_numeric(df[col], errors='coerce')
        negativo = valores < 0
        hallazgos.append(_fila('validez', col, 'valores negativos', negativo.sum(), total,
                               _ejemplos(valores[negativo])))
        filas[col] = df[negativo]
    return _a_tabla(hallazgos), filas


def atipicos_iqr(df, columna, k=1.5):
    """Valores atípicos con la regla del rango intercuartílico (IQR), por debajo y por encima.

    Límites: Q1 - k·IQR y Q3 + k·IQR, donde IQR = Q3 - Q1 (k = 1.5 es la regla clásica, la misma
    de los bigotes del boxplot). Un atípico no es necesariamente un error: es un valor lejos de la
    mayoría que hay que revisar. Y al revés: si la distribución es muy ancha, un valor imposible
    puede quedar dentro de los límites (para eso está `validez_rangos`).

    Devuelve (hallazgos, limites, filas_abajo, filas_arriba): dos filas de hallazgos (abajo y
    arriba), un diccionario con Q1, Q3, IQR y los límites, y las filas completas de los atípicos
    de cada lado.
    """
    valores = pd.to_numeric(df[columna], errors='coerce')
    q1, q3 = valores.quantile([0.25, 0.75])
    iqr = q3 - q1
    lim_inf, lim_sup = q1 - k * iqr, q3 + k * iqr
    abajo, arriba = valores < lim_inf, valores > lim_sup
    total = len(df)
    hallazgos = _a_tabla([
        _fila('validez', columna, f'atípicos por debajo de {lim_inf:,.2f} (IQR)',
              abajo.sum(), total, _ejemplos(valores[abajo])),
        _fila('validez', columna, f'atípicos por encima de {lim_sup:,.2f} (IQR)',
              arriba.sum(), total, _ejemplos(valores[arriba])),
    ])
    limites = {'q1': q1, 'q3': q3, 'iqr': iqr, 'limite_inferior': lim_inf, 'limite_superior': lim_sup}
    return hallazgos, limites, df[abajo], df[arriba]


# ----------------------------------------------------------------------------------------------
# Consistencia: ¿los datos se representan igual y no se contradicen?
# ----------------------------------------------------------------------------------------------

def consistencia_formato(df, columnas=None, equivalencias=None):
    """Valores de texto que significan lo mismo pero están escritos distinto ('France' / 'FRANCE').

    Agrupa los valores por su versión normalizada (sin mayúsculas, espacios ni tildes). En cada
    grupo con más de una variante, cuenta como afectadas las filas que no usan la variante más
    común.
    - `columnas`: columnas a revisar; por defecto, todas las de texto.
    - `equivalencias`: {columna: {variante: valor_canonico}} para casos que la normalización no
      junta, como abreviaturas ('F' -> 'Female'). Es una decisión nuestra, por eso es opcional.

    Devuelve (hallazgos, detalle), donde `detalle` lista cada variante con su frecuencia.
    """
    columnas = columnas or [c for c in df.columns if _es_texto(df[c])]
    equivalencias = equivalencias or {}
    total = len(df)
    filas, detalle = [], []
    for col in columnas:
        conteo = df[col].dropna().value_counts()
        mapa = equivalencias.get(col, {})
        claves = conteo.index.map(lambda v: _normalizar(mapa.get(v, v)))
        n_afectados, ejemplos = 0, []
        for clave, variantes in conteo.groupby(claves):
            if len(variantes) < 2:
                continue
            principal = variantes.idxmax()
            n_afectados += variantes.drop(principal).sum()
            ejemplos.append('/'.join(map(str, variantes.index)))
            for valor, n in variantes.items():
                detalle.append({'columna': col, 'grupo': clave, 'variante': valor,
                                'n': int(n), 'es_la_mas_comun': valor == principal})
        filas.append(_fila('consistencia', col, 'mismo valor escrito de varias formas',
                           n_afectados, total, '; '.join(ejemplos)))
    detalle = pd.DataFrame(detalle, columns=['columna', 'grupo', 'variante', 'n', 'es_la_mas_comun'])
    return _a_tabla(filas), detalle


def consistencia_reglas(df, reglas):
    """Reglas que cruzan columnas: datos que no se contradicen entre sí.

    `reglas`: {nombre_de_la_regla: funcion}, donde `funcion(df)` devuelve una máscara booleana
    con True en las filas que **incumplen** la regla. En `ejemplos` van los índices de algunas
    filas que la incumplen.
    Ej.: {'saldo negativo': lambda d: d['balance'] < 0}
    """
    total = len(df)
    filas = []
    for nombre, regla in reglas.items():
        incumple = pd.Series(regla(df), index=df.index).fillna(False).astype(bool)
        filas.append(_fila('consistencia', 'varias', nombre, incumple.sum(), total,
                           _ejemplos(pd.Series(df.index[incumple]))))
    return _a_tabla(filas)


# ----------------------------------------------------------------------------------------------
# Catálogo
# ----------------------------------------------------------------------------------------------

def juntar(*tablas):
    """Une tablas de hallazgos en el orden en que vienen, ignorando las vacías."""
    no_vacias = [t for t in tablas if len(t)]
    return pd.concat(no_vacias, ignore_index=True) if no_vacias else _a_tabla([])


def catalogo(*tablas, solo_problemas=True):
    """Junta las tablas de hallazgos en una sola, ordenada por dimensión y por % de filas afectadas.

    Con `solo_problemas=True` quita los chequeos sin filas afectadas, pero deja los que no tienen
    conteo (por ejemplo, un tipo sin determinar), para que no se pierdan de vista.
    """
    cat = juntar(*tablas)
    if solo_problemas:
        cat = cat[(cat['n_afectados'].isna() | (cat['n_afectados'] > 0)).fillna(False).astype(bool)]
    cat['dimension'] = pd.Categorical(cat['dimension'], categories=ORDEN_DIMENSIONES, ordered=True)
    return cat.sort_values(['dimension', 'pct_afectados'], ascending=[True, False]).reset_index(drop=True)
