# Referencias para la interpretación de los datos

Documentos oficiales que se usaron para interpretar las columnas del dataset (diccionario de datos del notebook
`01`, sección 1.1, y anexo técnico del informe). Todos se consultaron el 27 de septiembre de 2026.

| Archivo | Documento | Emisor | Fuente original | Para qué se usó |
|---|---|---|---|---|
| `secop_ii_contratos_electronicos_metadatos_jbjy-vk9h.json` | Metadatos del conjunto "SECOP II - Contratos Electrónicos" (95 columnas con su descripción) | Colombia Compra Eficiente, vía datos.gov.co | [API de metadatos](https://www.datos.gov.co/api/views/jbjy-vk9h.json) · [página del conjunto](https://www.datos.gov.co/Estad-sticas-Nacionales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h) | Descripción oficial de cada columna. Muestra que el conjunto completo trae `fecha_inicio_liquidacion` y `fecha_fin_liquidacion`, que no vienen en el extracto |
| `cce_guia_secop_ii_gestion_contractual_2021.pdf` | Guía SECOP II – Gestión contractual para entidades estatales (CCE-SEC-GI-13, v1, 2021) | Colombia Compra Eficiente | [formacionvirtual.colombiacompra.gov.co](https://formacionvirtual.colombiacompra.gov.co/pluginfile.php/9193/mod_folder/content/0/M%C3%B3dulo%20VI/Gu%C3%ADa%20-%20Gesti%C3%B3n%20Contractual.pdf) | Qué significa cada campo en la plataforma: `liquidaci_n` se marca al crear el contrato si aplica la liquidación (p. 8); `dias_adicionados` es un contador automático de días prorrogados (pp. 7–8 y sección de modificaciones); `valor_pagado` solo suma los pagos que la entidad "marca como pagados" (sección de ejecución del contrato) |
| `cce_secop_ii_terminacion_liquidacion_cierre.pdf` | SECOP II, Módulo VI, Unidad 5: Terminación, liquidación y cierre del contrato | Colombia Compra Eficiente | [formacionvirtual.colombiacompra.gov.co](https://formacionvirtual.colombiacompra.gov.co/pluginfile.php/9287/mod_folder/content/0/PDF/M%C3%B3dulo%206/Unidad%205/13_terminacion.pdf) | Estados "Terminado" y "Cerrado", y la fecha de liquidación que se configura al crear el contrato |
| `cce_manual_datos_abiertos_secop.pdf` | Manual para el uso de Datos Abiertos del SECOP (M-MUDA-02) | Colombia Compra Eficiente | [colombiacompra.gov.co](https://www.colombiacompra.gov.co/wp-content/uploads/2024/09/manual_de_datos_abiertos_actualizado.pdf) | Los datos son de fuente primaria (cada entidad responde por lo que publica, Ley 1712 de 2014) y se actualizan a diario |
| `cce_guia_liquidacion_contratos_G-LPC-01_2016.pdf` | Guía para la liquidación de los Procesos de Contratación (G-LPC-01, 2016) | Colombia Compra Eficiente | [colombiacompra.gov.co](https://www.colombiacompra.gov.co/wp-content/uploads/2024/08/2016-Guia-para-la-liquidacion-contratos-estatales-G-LPC-01.pdf) | Qué contratos deben liquidarse (tracto sucesivo, ejecución que se prolonga, "los demás que lo requieran") y que la entidad define en cada caso si un contrato requiere liquidación (sección II.B, p. 3). Respalda la lectura de `liquidaci_n` como "sujeto a liquidación" |
| `cce_concepto_C-968_2024_liquidacion_regimen_especial.docx` | Concepto C-968 de 2024 (16 de diciembre de 2024) | Colombia Compra Eficiente (relatoría) | [relatoria.colombiacompra.gov.co](https://relatoria.colombiacompra.gov.co/conceptos/c-968-de-2024/) | Las entidades de régimen exceptuado *"no están obligadas a aplicar el artículo 60 de la Ley 80 de 1993 ni el artículo 11 de la Ley 1150"*; pueden pactar la liquidación según su manual. Respalda la lectura del régimen especial en `03` (3.4) y en el informe. Descargado a mano desde la relatoría |
| `ley_80_1993_parte1.html`, `ley_80_1993_parte2.html` | Ley 80 de 1993, Estatuto General de Contratación de la Administración Pública (vigente, con notas de modificación). El art. 60 está en la parte 2 | Secretaría General del Senado | [parte 1](http://www.secretariasenado.gov.co/senado/basedoc/ley_0080_1993.html) · [parte 2](http://www.secretariasenado.gov.co/senado/basedoc/ley_0080_1993_pr001.html) | Art. 60 (modificado por el art. 217 del Decreto-Ley 19 de 2012): qué contratos deben liquidarse (tracto sucesivo) y qué es la liquidación |
| `ley_1150_2007.html` | Ley 1150 de 2007 | Secretaría General del Senado | [secretariasenado.gov.co](http://www.secretariasenado.gov.co/senado/basedoc/ley_1150_2007.html) | Art. 11: plazos de liquidación (4 meses bilateral, 2 meses unilateral, 2 años adicionales) |

## Consultadas pero no incluidas

- **Ámbito Jurídico, "La liquidación en los contratos de entidades estatales regidos por el derecho privado":**
  [enlace](https://www.ambitojuridico.com/noticias/informe/la-liquidacion-en-los-contratos-de-entidades-estatales-regidos-por-el-derecho).
  Es un artículo de prensa con derechos de autor, así que no se copia en un repositorio público. Además, el sitio
  bloquea el acceso automático (HTTP 403), así que no se pudo leer; la afirmación que respaldaba se verificó con
  el concepto C-968 de 2024.
- **Ley 1150 de 2007 en el Gestor Normativo de Función Pública:**
  [enlace](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=184686). No se pudo descargar por un
  error de certificado SSL del servidor; se usó la copia de la Secretaría del Senado.

Los archivos HTML de las leyes se guardaron tal como los entrega el sitio (codificación ISO-8859-1).
