# Declaración de uso de IA generativa — Taller 2

> **Borrador en construcción.** Se actualiza a medida que avanza el taller (faltan la evaluación en prueba, el
> cálculo de valor, los insights y las interpretaciones de los notebooks).

**Integrantes:** Daniel Triviño · Nicolás Bedoya

**Herramienta y modelo:** Claude Code (Anthropic), con el modelo **Claude Opus 5.5**, usado como asistente dentro del
repositorio: leía archivos, escribía y ejecutaba código y consultaba la web para verificar datos.

**Periodo de uso:** 27 y 28 de octubre de 2026 *(actualizar al cierre)*.

## Para qué se usó

| Parte del trabajo | Qué hizo la IA | Qué hizo el equipo |
|---|---|---|
| Entendimiento (`01`) | Escribió el código de perfilado, el módulo reutilizable `calidad.py` (completitud, unicidad, validez, consistencia, IQR, negativos), los gráficos y el texto de los markdown | Determinó a mano el tipo de cada variable; definió los rangos válidos, los dominios, las equivalencias `M/F`, la regla `age > tenure` y qué revisar (IQR, negativos, filas completas) |
| Limpieza (`02`) | Resumió los hallazgos con opciones; escribió el código, la bitácora y la verificación con `assert` | Decidió eliminar filas sin sentido y duplicados, conservar los faltantes para imputarlos en el pipeline y llevar las categorías a su variante más común |
| Exploración (`03`) | Escribió el código de distribuciones, tasas de churn por grupo y correlación | Revisión de los resultados (la interpretación va en la fila de interpretaciones) |
| Modelado (`04`) | Propuso opciones; escribió el pipeline, la comparación de desbalance, la búsqueda de hiperparámetros y la selección | Eligió los modelos (logística, SVM, XGBoost), comparar SMOTE en CV, la métrica PR-AUC y las métricas adicionales; planteó y decidió **excluir género y país** por razones éticas |
| Interpretaciones | No las escribió (quedaron como espacios por completar) | *(por completar: las redacta el equipo)* |

## Decisiones del equipo frente a sugerencias de la IA

- **Iniciativa del equipo:** tipos de variables; rango de DataCrédito (150–950) para `credit_score`; edad entre 18 y
  100; `tenure` ≥ 0; salario ≥ 0; aceptar que el saldo puede ser negativo; regla `age > tenure`; tratar `M/F` como
  `Male/Female`; eliminar las filas sin sentido; excluir `gender` y `country`; los tres modelos; comparar estrategias
  de desbalance; reportar precisión, recall, F1 y ROC-AUC.
- **Elegidas por el equipo entre opciones que propuso la IA:** partición 80/20 con CV de 5 particiones; eliminar
  duplicados; imputar con la mediana dentro del pipeline; conservar los atípicos plausibles; PR-AUC como métrica de
  selección; conservar `age`; estrategia "ninguna" para el modelo final, decidida a partir de los resultados de la
  comparación.

## Verificación de información

La IA consultó y citó fuentes para respaldar decisiones: escala de puntaje de DataCrédito, Ley 27 de 1977 (mayoría de
edad), artículo 13 de la Constitución, Marco Ético para la IA en Colombia y el estudio de van den Goorbergh et al.
(2022, *JAMIA*) sobre correcciones de desbalance. En un caso **corrigió una premisa del equipo**: "un menor no puede
tener puntaje crediticio" es solo parcialmente cierto, porque existen productos con codeudor desde los 14 años.
*(Pendiente: que el equipo revise directamente las fuentes que se citen en el informe.)*

## Porcentaje de ayuda (estimado, por ajustar al cierre)

| Componente | Peso en el trabajo | Aporte de la IA |
|---|---|---|
| Código | 35% | ~95% |
| Redacción de notebooks | 25% | ~90% (sin contar las interpretaciones) |
| Decisiones analíticas | 40% | ~35% (la IA proponía opciones y el equipo decidía) |
| **Total ponderado** | | **≈ 70%** |

*(Si algún integrante usó IA por su cuenta, se suma aquí. El porcentaje debería bajar cuando el equipo escriba las
interpretaciones y el informe.)*

## Anexo: prompts más relevantes

Mensajes del equipo, literales. Donde dice *[selección]*, el equipo eligió entre opciones que planteó la IA.

| # | Prompt | Qué muestra |
|---|---|---|
| 1 | "…lo primero debera ser ver cantidad de datos por columna/variable, y determinar manualmente su tipo, realiza el codigo para yo revisar los datos y determinarlo" | El equipo determina los tipos; la IA solo prepara la evidencia |
| 2 | "…las categorias vendrian a ser country, gender. Las numericas serian credit_score que ademas parece ser discreta, tenure que es discreta y dado el contexto del negocio parece estar en años… Con esto en cuenta ahora quiero que realices funciones generales reusables para analizar completitud, consistencia, validez, unicidad" | Clasificación de tipos del equipo y pedido del módulo de calidad |
| 3 | "en consistencia… me parece relevante revisar valores donde age es mayor a tenure. Por otro lado, credit_score, tenure, balance y estimated_salary quiero revisar outliers haciendo uso de un boxplot y de IQR… y esos valores imprimir sus filas con todas las columnas" | El equipo define qué revisar en consistencia y validez |
| 4 | "para el credit score, dado que el contexto menciona una fintech colombiana vamos a usar los rangos de credito que usa datacredito, es decir de 150 a 950 puntos… para age de 18 a 100… (acorde a la ley colombiana, igual verifica este dato), y tenure simplemente que sea mayor o igual a 0. Por otro lado country y gender se formatean de acuerdo al valor mas comun" | Reglas de negocio del equipo, con pedido de verificar la fuente |
| 5 | "agrega estimated_salary, vamos a suponer que balance si puede ser negativo" | Decisión de negocio sobre los rangos |
| 6 | "primero hagamos la limpieza en el 02 dame un resumen de los hallazgos para decidir como tratar los datos, lo que si o si va es eliminar las pocas filas con valores que no tienen sentido" + *[selección: duplicados, faltantes, atípicos]* | El equipo decide el tratamiento a partir de un resumen |
| 7 | "logistic-svm-xgboost" + "primero definamos si hacer smote o como afrontar esto" | El equipo elige los modelos y pide discutir el desbalance |
| 8 | "…estoy pensando en quitar las columnas de genero pais y edad pues quiza el modelo podria sesgarse hacia ciertos segmentos y hasta donde tengo entendido eso es un problema etico, confirmame esto por favor" | Preocupación ética planteada por el equipo |
| 9 | "las estrategias actuales se quedan como documentacion, el modelo final va con ninguna, adicional quiero el resto de metricas, recall, precision, f1, roc auc" | Decisión final de la estrategia y métricas pedidas |
