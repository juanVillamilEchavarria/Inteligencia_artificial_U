
--- Página 1 ---
1 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Entregable Avance de Proyecto – Segundo Corte 
Inteligencia Artificial · Ingeniería de Sistemas · Período 2026-02 · Docente: Jhon James Cano Sánchez 
Campo 
Detalle 
Modalidad 
No presencial. No hay sustentación en clase: el avance se sustenta 
con un video. 
Fecha límite de entrega 
Domingo 25 de octubre de 2026, 11:59 p. m., en la plataforma 
AVACO 
Qué se entrega 
1) Documento del avance en PDF · 2) Enlace al video (máximo 10 
minutos) · 3) Enlace al repositorio de GitHub 
Ponderación 
10 % del segundo corte (30 %) 
Integrantes 
Los mismos del avance 1 (grupos de 2 o 3 estudiantes, o individual) 
 
1. Objetivo del Entregable 
El grupo demostrará que su proyecto pasó de comprender los datos (primer corte) a 
prepararlos para Machine Learning y entrenar un primer modelo construido por el 
propio grupo. Este avance recoge lo trabajado en las clases 7, 8 y 9: Pandas, Seaborn, 
preparación de datos y el perceptrón desde cero con descenso del gradiente. 
¿Por qué un video y no una exposición? El calendario del segundo corte no deja 
sesiones libres (el 2 de noviembre es festivo). El video permite que cada grupo 
sustente su avance sin consumir clase. 
2. Requisitos Mínimos del Avance 
A. Ajustes a partir del avance 1 
• 
Enumerar las observaciones recibidas en la sustentación del 21 de septiembre 
y qué se hizo con cada una. 
• 
Si cambió el alcance, la fuente de datos o el objetivo del proyecto, explicarlo y 
justificarlo. 
B. Preparación de datos con Pandas (Clase 7) 
• 
Carga del dataset del proyecto con Pandas e inspección: shape, info(), nulos 
por columna y duplicados. 
• 
Tratamiento justificado de: valores nulos, duplicados, tipos de datos 
incorrectos, valores atípicos o imposibles, y categorías inconsistentes (lo que 
aplique al dataset). 
• 
Codificación de variables categóricas con pd.get_dummies si se van a usar en 
el modelo. 

--- Página 2 ---
2 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
• 
Dataset 
limpio 
exportado 
a 
data/ 
(por 
ejemplo 
data/proyecto_limpio.csv). 
• 
Tabla "antes / después": número de filas, columnas y nulos. 
C. Visualización con Seaborn (Clase 7) 
• 
Al menos 3 gráficos con Seaborn, con títulos y ejes claros. Al menos uno debe 
relacionar las variables de entrada con la variable objetivo. 
• 
Cada gráfico con una interpretación de 2 a 4 líneas: qué muestra y qué decisión 
del proyecto se apoya en él. 
D. Primer modelo: perceptrón desde cero (Clases 8 y 9) 
Corresponde 
a 
la 
actividad 
independiente 
de 
la 
Clase 
9 
(perceptron_proyecto.py). 
• 
Definición clara de la variable objetivo 0/1 (si se creó a partir de una columna 
numérica, explicar el umbral usado y por qué esa columna no se usa como 
entrada). 
• 
Dos variables de entrada numéricas escaladas (estandarización). 
• 
Perceptrón con sigmoide, pérdida logarítmica y descenso del gradiente 
implementado con NumPy, sin Scikit-Learn. 
• 
Resultados: pesos finales (w1, w2, b), pérdida inicial y final, exactitud. 
• 
Gráficos: curva de aprendizaje y frontera de decisión. 
• 
Interpretación: significado del signo de cada peso en el contexto del proyecto, 
si los datos parecen linealmente separables y las limitaciones del modelo. 
E. Plan hacia el proyecto final 
• 
¿Qué tipo de problema es el proyecto: clasificación o regresión? 
• 
¿Qué modelos de Scikit-Learn se planean comparar en la Clase 12 (9 de 
noviembre)? ¿Qué métrica se usará para elegir el mejor y por qué? 
• 
¿Cómo será la demostración final (qué casos nuevos se van a predecir)? 
• 
Cronograma breve del grupo hasta la sustentación final (23 o 30 de noviembre). 
F. Control de versiones 
• 
Repositorio de GitHub actualizado con el código, los datos (o instrucciones para 
obtenerlos si son muy grandes), los gráficos y el README. 
• 
Al menos 5 commits desde el avance 1, con mensajes descriptivos. 
• 
README con una sección "Avance 2" que resuma los resultados y explique 
cómo ejecutar los scripts con Docker. 

--- Página 3 ---
3 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
3. Documento del Avance (PDF) 
Extensión: 6 a 10 páginas, sin contar portada ni anexos. Letra de 11 o 12 puntos, 
interlineado 1.15 o 1.5. No se exige norma APA en este avance (sí en el informe final), 
pero toda figura y tabla debe tener número, título y una frase que la explique, y toda 
fuente de datos debe estar referenciada. 
Sección 
Contenido 
Extensión 
sugerida 
Portada 
Nombre del proyecto, integrantes, programa, asignatura, 
docente, fecha. 
1 página 
1. Resumen del proyecto 
Problemática de Cartago, objetivo del sistema de IA y 
datos usados. 
½ página 
2. Ajustes desde el avance 1 
Requisito A. 
½ página 
3. Preparación de datos 
Requisito B, con la tabla antes/después y fragmentos 
cortos de código. 
1½ a 2 páginas 
4. Análisis visual 
Requisito C: los 3 gráficos con su interpretación. 
1½ a 2 páginas 
5. Perceptrón desde cero 
Requisito D: explicación del modelo, resultados, 
gráficos e interpretación. 
2 a 3 páginas 
6. Plan hacia el proyecto final 
Requisito E. 
½ página 
7. Referencias 
Fuente de los datos y bibliografía consultada. 
— 
Anexo 
Enlace al repositorio y al video. 
— 
 
Nombre del archivo: Avance2_GrupoXX_NombreProyecto.pdf (sin espacios ni 
tildes; por ejemplo Avance2_Grupo03_PrediccionCafe.pdf). 
4. Video de Sustentación (máximo 10 minutos) 
Estructura del video 
Momento 
Duración 
Contenido 
1. Presentación 
0:00 – 1:30 
Integrantes (todos deben aparecer y hablar en el video), 
nombre del proyecto y problemática. 
2. Datos y limpieza 
1:30 – 3:45 
Mostrar el dataset original y los problemas encontrados; 
explicar las decisiones de limpieza. 
3. Visualización 
3:45 – 5:30 
Mostrar los gráficos de Seaborn y el hallazgo más importante. 
4. Perceptrón en vivo 
5:30 – 7:15 
Ejecutar perceptron_proyecto.py dentro del contenedor 
Docker (se debe ver el prompt root@...:/app/src#), explicar 
la salida, la curva de aprendizaje y la frontera de decisión. 
5. Próximos pasos 
7:15 – 10:00 
Qué modelo de Scikit-Learn se usará y cómo será la 
demostración final. 
 
Requisitos técnicos 
• 
Duración máxima: 10:00 minutos. Si el video es más largo, solo se evaluarán 
los primeros 10 minutos. 
• 
Grabación de pantalla con voz (y cámara opcional). Herramientas gratuitas 
sugeridas: la grabación de reuniones de Microsoft Teams o Google Meet, OBS 
Studio, o la herramienta Recortes de Windows (grabación de pantalla). 

--- Página 4 ---
4 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
• 
Publicación: YouTube como video no listado, o Google Drive / OneDrive con 
permiso "cualquier persona con el enlace puede ver". Verificar el enlace en 
una ventana de incógnito antes de entregarlo: un enlace sin permiso equivale 
a no entregar el video. 
• 
Audio claro. Letra del editor de código o de la terminal ampliada (Ctrl + + en 
VSCode) para que el código se lea. 
• 
Nombre del video: Avance2_GrupoXX_NombreProyecto. 
Recomendación: Escribir un guion corto antes de grabar y ensayar una vez con 
cronómetro. Cinco minutos se pasan rápido: es mejor mostrar el perceptrón 
funcionando que leer diapositivas. 
5. Forma de Entrega en AVACO 
1. Un solo integrante por grupo carga la entrega en la actividad "Avance 2 del 
proyecto". 
2. Adjuntar el PDF del documento. 
3. En el campo de texto de la entrega, pegar: (a) los nombres de los integrantes, (b) 
el enlace del video y (c) el enlace del repositorio de GitHub. 
4. Antes del cierre (domingo 1 de noviembre, 11:59 p. m.), verificar que los tres 
elementos quedaron cargados. 
Las entregas fuera de plazo se rigen por el reglamento estudiantil y las condiciones que 
el docente haya informado al inicio del semestre. 
6. ¿Qué NO se requiere para este avance? 
• 
No se requiere usar Scikit-Learn (se verá en la Clase 12, el 9 de noviembre). 
• 
No se requiere una interfaz gráfica ni web. 
• 
No se requiere el informe en normas APA (se exige en el informe final). 
• 
No se requieren diapositivas: el video puede mostrar directamente VSCode, la 
terminal y el documento. 

--- Página 5 ---
5 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
7. Rúbrica de Evaluación (nota máxima 5.0) 
Criterio 
Peso 
Completo (100 %) 
Aceptable (60 %) 
Deficiente (0–30 %) 
Preparación de datos (B) 
1.0 
Todos los problemas tratados y 
justificados; dataset limpio 
exportado; tabla 
antes/después. 
Limpieza parcial o 
sin justificar. 
Sin limpieza o con 
errores que invalidan 
los datos. 
Visualización (C) 
0.6 
3 gráficos de Seaborn claros e 
interpretados, uno relacionado 
con el objetivo. 
Menos gráficos o sin 
interpretación. 
Sin gráficos o 
ilegibles. 
Perceptrón desde cero 
(D) 
1.4 
Implementación completa con 
NumPy, la pérdida baja, ambos 
gráficos e interpretación en 
contexto. 
Funciona pero falta 
escalado, algún 
gráfico o la 
interpretación. 
No funciona, no es 
desde cero o falta. 
Documento (A, E y 
estructura) 
0.8 
Estructura completa, ajustes 
del avance 1, plan claro y 
redacción cuidada. 
Faltan secciones o el 
plan es vago. 
Documento 
incompleto o sin 
estructura. 
Video 
0.8 
≤ 5 min, todos los integrantes 
participan, el perceptrón se 
ejecuta en el contenedor y se 
explica con claridad. 
Falta la ejecución en 
vivo o no participan 
todos. 
Enlace sin permiso, 
sin audio o sin 
contenido del 
avance. 
GitHub (F) 
0.4 
≥ 5 commits descriptivos, 
README con sección Avance 2 
e instrucciones de ejecución. 
Pocos commits o 
README básico. 
Repositorio vacío, 
desactualizado o 
privado. 
Total 
5.0 
 
 
 
 
Nota individual: Si un integrante no aparece en el video ni en el historial de commits, 
el docente podrá asignarle una nota individual diferente a la del grupo. 
8. Ejemplo de Avance (para referencia de los estudiantes) 
Elemento 
Contenido de ejemplo 
Proyecto 
Predicción de cosechas de café en la zona rural de Cartago 
Ajuste desde el avance 
1 
Se reemplazó un dataset genérico de Kaggle por datos de fincas de la 
región; se definió la variable objetivo. 
Limpieza 
312 → 287 filas: 9 duplicados, 11 filas sin producción, 5 altitudes 
registradas en km; variedad unificada ("castillo" → "Castillo"). 
Objetivo 0/1 
cosecha_buena = 1 si la producción por hectárea supera la mediana (1 
450 kg/ha). La producción no se usa como entrada. 
Entradas 
altitud_msnm y lluvia_mm_mes (estandarizadas). 
Resultados 
w1 = 1.84, w2 = 1.12, b = −0.21; pérdida 0.693 → 0.412; exactitud 81 %. 
Interpretación 
Mayor altitud y más lluvia aumentan la probabilidad de buena cosecha; 
la frontera deja mal clasificadas las fincas bajas con riego. 
Plan final 
Clasificación; comparar regresión logística y árbol de decisión; priorizar 
recall para no dejar sin asistencia fincas en riesgo. 
 
Los números del ejemplo son ilustrativos. 
