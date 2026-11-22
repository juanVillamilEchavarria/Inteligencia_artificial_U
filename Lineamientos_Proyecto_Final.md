
--- Página 1 ---
1 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
Lineamientos del Proyecto Final 
Inteligencia Artificial · Ingeniería de Sistemas · Período 2026-02 · Docente: Jhon James Cano Sánchez · 
Tercer corte (40 %) 
Campo 
Detalle 
Fecha de sustentación 
Lunes 23 de noviembre de 2026, en la hora de clase, de forma 
presencial 
Entrega en AVACO 
Hasta las 11:59 p. m. del día anterior a la sustentación: informe final 
en PDF (normas APA), enlace al repositorio de GitHub y presentación 
(PDF) 
Ponderación 
Tercer corte (40 %): proyecto final funcional 25 % + 
sustentación/demostración y documentación 15 % 
Integrantes 
Los mismos de los avances 1 y 2 
 
Importante: No habrá sesión de recuperación (el 16 de noviembre es festivo y no hay 
otra fecha disponible). La sustentación se realiza únicamente en la fecha 
programada. 
1. Objetivo 
Cada grupo presentará el sistema de inteligencia artificial que construyó durante el 
semestre para una problemática real de Cartago, Valle. El proyecto debe demostrar el 
ciclo completo: datos → preparación → modelo construido desde cero → modelos de 
Scikit-Learn → evaluación → demostración, y el grupo debe ser capaz de explicar qué 
hace su modelo por dentro, que es el criterio central del curso. 

--- Página 2 ---
2 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
2. Componente 1: Sistema Funcional (25 %) 
2.1. Requisitos mínimos 
# 
Requisito 
Origen 
1 
Entorno reproducible con Docker: Dockerfile, docker-compose.yml y 
requirements.txt. Un tercero debe poder ejecutar el proyecto siguiendo el 
README. 
Clases 1–2 
2 
Datos del proyecto en data/ (o instrucciones para descargarlos si superan 50 MB) y 
su fuente documentada. 
Avance 1 
3 
Script de preparación de datos con Pandas que genere el dataset limpio. 
Avance 2 
4 
Perceptrón desde cero con NumPy (versión del Avance 2, con las correcciones de la 
retroalimentación). 
Avance 2 
5 
src/modelo_proyecto.py: al menos dos modelos de Scikit-Learn comparados 
con división entrenamiento/prueba, Pipeline, validación cruzada y las métricas 
adecuadas; el mejor modelo guardado con joblib. 
Clase 12 
6 
src/usar_modelo.py: carga el modelo guardado y predice casos nuevos. Es la 
base de la demostración en vivo. 
Clase 12 
7 
Gráficos en PNG: al menos 3 de análisis (Seaborn) y al menos 2 de evaluación (curva 
de aprendizaje del perceptrón, matriz de confusión o real vs predicho). 
Clases 7–12 
8 
README completo: descripción, estructura de carpetas, cómo ejecutar paso a paso 
con Docker, resultados principales y enlace al informe. 
Todo el curso 
9 
Historial de commits que muestre el trabajo de todos los integrantes a lo largo del 
semestre. 
Todo el curso 
 
2.2. Estructura sugerida del repositorio 
nombre-proyecto/ 
├── Dockerfile 
├── docker-compose.yml 
├── requirements.txt 
├── README.md 
├── data/ 
│   ├── datos_originales.csv 
│   └── datos_limpios.csv 
├── docs/ 
│   └── Informe_Final_GrupoXX.pdf 
├── graficos/                     ← o dentro de src/, según se haya trabajado 
└── src/ 
    ├── preparacion_datos.py 
    ├── perceptron_proyecto.py 
    ├── modelo_proyecto.py 
    ├── usar_modelo.py 
    └── modelo_final.joblib 
 
 

--- Página 3 ---
3 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
2.3. Valor agregado (opcional) 
Los siguientes elementos no son obligatorios. Suman en el criterio "Calidad técnica y 
valor agregado" si están bien explicados y funcionan: 
• 
Una interfaz sencilla (por ejemplo un menú en consola, Streamlit o Flask) que 
use usar_modelo.py. 
• 
Un componente de IA generativa (por ejemplo, un modelo de lenguaje que 
explique en lenguaje natural la predicción). Las claves de API van en un archivo 
.env incluido en .gitignore; nunca en el código ni en GitHub. 
• 
Una red neuronal (MLPClassifier) comparada con los demás modelos. 
• 
Optimización de hiperparámetros (GridSearchCV). 
• 
Datos obtenidos de una fuente oficial (datos.gov.co, DANE, IDEAM, Alcaldía de 
Cartago) o recolectados por el grupo. 
 

--- Página 4 ---
4 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
3. Componente 2: Informe Final en Normas APA (parte del 15 %) 
3.1. Estructura del informe 
Sección 
Contenido 
Extensión 
sugerida 
Portada 
Formato de trabajo estudiantil APA 7 (ver 3.3). 
1 página 
Resumen 
Un párrafo de 150 a 250 palabras: problema, datos, método, 
resultado principal y conclusión. Debajo, de 3 a 5 palabras 
clave. 
1 página 
Introducción 
Contexto de Cartago, problemática, justificación y pregunta 
que responde el proyecto. 
1 a 1½ páginas 
Objetivos 
Objetivo general y 3 a 4 específicos (verbos medibles). 
½ página 
Marco teórico 
Conceptos usados, explicados con palabras propias y con 
citas: perceptrón, sigmoide, función de pérdida, descenso del 
gradiente, modelos de Scikit-Learn usados y métricas. 
Mínimo 4 fuentes. 
2 a 3 páginas 
Metodología 
Fuente y descripción de los datos (diccionario de variables), 
preparación, perceptrón desde cero, modelos de Scikit-Learn, 
división entrenamiento/prueba, validación cruzada y entorno 
(Docker). 
2 a 3 páginas 
Resultados 
Tablas de métricas, gráficos (curva de aprendizaje, matriz de 
confusión o real vs predicho), comparación de modelos y 
ejemplos de predicción. 
2 a 3 páginas 
Discusión 
Interpretación de los resultados en el contexto de Cartago, 
limitaciones (datos, sesgos, tamaño de muestra) y 
consideraciones éticas. 
1 a 1½ páginas 
Conclusiones y trabajo 
futuro 
Respuesta a los objetivos y mejoras posibles. 
½ a 1 página 
Referencias 
Lista en formato APA 7, orden alfabético, sangría francesa. 
Mínimo 6 referencias. 
1 página 
Apéndices 
Enlace al repositorio, fragmentos de código relevantes, 
declaración de uso de IA. 
Libre 
 
Extensión total: 12 a 20 páginas sin contar portada, referencias ni apéndices. Nombre 
del archivo: Informe_Final_GrupoXX_NombreProyecto.pdf. 
 

--- Página 5 ---
5 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
3.2. Formato APA 7.ª edición (requisitos obligatorios) 
Elemento 
Norma 
Tamaño de página y 
márgenes 
Carta; márgenes de 2.54 cm en los cuatro lados. 
Fuente 
Una sola fuente en todo el documento: Times New Roman 12, Calibri 11, Arial 
11 o Georgia 11. 
Interlineado 
Doble en todo el texto, incluidas las referencias. Sin espacio adicional antes o 
después de los párrafos. 
Alineación y sangría 
Texto alineado a la izquierda (no justificado); sangría de 1.27 cm en la primera 
línea de cada párrafo. 
Numeración 
Número de página en la esquina superior derecha, desde la portada. 
Nivel 1 de título 
Centrado, negrita, mayúsculas y minúsculas. 
Nivel 2 de título 
Alineado a la izquierda, negrita. 
Nivel 3 de título 
Alineado a la izquierda, negrita y cursiva. 
Tablas 
Número en negrita arriba (Tabla 1), título en cursiva en la línea siguiente, sin 
líneas verticales, nota debajo si aplica. 
Figuras 
Número en negrita arriba (Figura 1), título en cursiva, la figura, y una nota 
debajo con la fuente (por ejemplo, "Elaboración propia con Matplotlib"). 
Citas en el texto 
Autor y año: (Géron, 2022) o Géron (2022) señala que…; cita textual de menos 
de 40 palabras entre comillas con página: (Géron, 2022, p. 120). 
Referencias 
Al final, en orden alfabético, con sangría francesa de 1.27 cm. 
 
3.3. Portada de trabajo estudiantil 
Centrada en la mitad superior de la página, en este orden, con interlineado doble: 
1. Título del proyecto (en negrita). 
2. Nombres completos de los integrantes. 
3. Programa: Ingeniería de Sistemas, Corporación de Estudios Tecnológicos del 
Norte del Valle. 
4. Asignatura: Inteligencia Artificial. 
5. Docente: Jhon James Cano Sánchez. 
6. Fecha de entrega (por ejemplo: 22 de noviembre de 2026). 

--- Página 6 ---
6 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
3.4. Ejemplos de referencias en APA 7 
Plantillas de referencias 
Libro: 
Géron, A. (2022). Hands-on machine learning with Scikit-Learn, Keras, and TensorFlow 
    (3rd ed.). O'Reilly Media. 
 
Artículo de revista: 
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., 
    Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., 
    Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: 
    Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830. 
 
Conjunto de datos: 
Nombre de la entidad. (Año). Título del conjunto de datos [Conjunto de datos]. 
    Nombre del portal. URL 
 
Software: 
Python Software Foundation. (2024). Python (Versión 3.12) [Software]. 
https://www.python.org 
 
Página web: 
Autor u organización. (Año, día de mes). Título de la página. Nombre del sitio. URL 
 
Herramienta de IA generativa: 
OpenAI. (2025). ChatGPT (versión del día de uso) [Modelo de lenguaje de gran tamaño]. 
    https://chat.openai.com 
 
En el informe, la cursiva de APA se aplica al título del libro, al nombre de la revista y su 
volumen, y al título del conjunto de datos. 
3.5. Declaración de uso de inteligencia artificial 
Se permite usar herramientas de IA generativa como apoyo, pero el informe debe incluir 
en los apéndices una declaración de uso de IA que indique: qué herramienta se usó, 
para qué tarea (por ejemplo: depurar un error, mejorar la redacción, explicar un 
concepto) y cómo se verificó el resultado. Los textos generados por IA que se incluyan 
deben citarse como en el ejemplo anterior. El grupo es responsable de todo lo que 
entrega y debe poder explicarlo en la sustentación. 
 

--- Página 7 ---
7 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
4. Componente 3: Sustentación y Demostración (parte del 15 %) 
4.1. Logística 
• 
Tiempo por grupo: 8 minutos (6 de exposición con demostración + 2 de 
preguntas; el docente podrá ajustar el tiempo según el número final de grupos 
y lo informará en AVACO. 
• 
El orden de presentación se sortea al inicio de la sesión: todos los grupos 
deben estar listos desde el comienzo. 
• 
La demostración se ejecuta en vivo, desde el contenedor Docker del grupo. 
Tener el contenedor encendido y la presentación abierta antes de que llegue el 
turno. 
• 
Plan B obligatorio: tener capturas de pantalla de la ejecución dentro de la 
presentación por si falla el equipo o la conexión. 
• 
Todos los integrantes deben hablar durante la exposición y estar preparados 
para responder preguntas sobre cualquier parte del proyecto. 
4.2. Estructura de la presentación (6 minutos) 
Momento 
Tiempo 
Contenido 
1. Problema 
1 min 
Problemática de Cartago, a quién beneficia el sistema y objetivo. 
2. Datos 
1 min 
Fuente, tamaño, principales problemas de calidad y cómo se 
resolvieron. 
3. Modelo por dentro 
1½ min 
Perceptrón desde cero: qué aprendió (signo de los pesos) y su frontera 
de decisión. 
4. Resultados 
1 min 
Comparación de los modelos de Scikit-Learn, métrica elegida y por 
qué. 
5. Demostración en vivo 
1 min 
python usar_modelo.py con casos nuevos; interpretar la 
probabilidad. 
6. Cierre 
½ min 
Limitaciones y trabajo futuro. 
 
4.3. Preguntas que pueden hacerse en la sustentación 
• 
¿Qué significa el signo y el tamaño de los pesos de su modelo? 
• 
¿Por qué eligieron esa métrica? ¿Qué error es más costoso en su problema? 
• 
¿Qué pasaría si llegan datos de otra zona o de otro año? 
• 
¿Cómo evitaron que el modelo "hiciera trampa" (fuga de información, escalado 
con datos de prueba)? 
• 
¿Qué cambiaron a partir de la retroalimentación del Avance 2? 
• 
Señale en el código dónde se actualizan los pesos / dónde se divide 
entrenamiento y prueba. 

--- Página 8 ---
8 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
5. Rúbricas de Evaluación 
5.1. Proyecto final funcional – 25 % (nota sobre 5.0) 
Criterio 
Peso 
Descripción del nivel completo 
Entorno reproducible 
0.5 
El proyecto se ejecuta con Docker siguiendo el README, sin 
pasos ocultos. 
Preparación de datos 
0.7 
Script de limpieza completo y justificado; dataset limpio 
generado por código. 
Perceptrón desde cero 
0.8 
Implementación correcta con NumPy, interpretada y corregida 
según la retroalimentación. 
Modelos de Scikit-Learn y 
evaluación 
1.3 
≥ 2 modelos en Pipeline, entrenamiento/prueba, validación 
cruzada, métricas adecuadas al problema y elección 
justificada. 
Demostración 
(usar_modelo.py) 
0.6 
Carga el modelo guardado y predice casos nuevos 
correctamente. 
Calidad técnica y valor agregado 
0.6 
Código organizado y comentado, gráficos claros; elementos 
opcionales bien integrados. 
Repositorio y trabajo en equipo 
0.5 
README completo, historial de commits de todos los 
integrantes, atención a la retroalimentación del Avance 2. 
Total 
5.0 
 
 
5.2. Sustentación/demostración y documentación – 15 % (nota sobre 5.0) 
Criterio 
Peso 
Descripción del nivel completo 
Informe: contenido 
1.5 
Todas las secciones completas, coherentes con el código y los 
resultados; discusión crítica con limitaciones y ética. 
Informe: normas APA 
1.0 
Portada, formato, títulos, tablas, figuras, citas y referencias 
según APA 7; declaración de uso de IA. 
Exposición 
1.0 
Estructura clara, tiempo respetado, participación de todos los 
integrantes. 
Demostración en vivo 
0.5 
El sistema se ejecuta desde el contenedor y el grupo interpreta 
la predicción. 
Dominio (preguntas) 
1.0 
Respuestas correctas sobre qué hace el modelo por dentro y 
sobre las decisiones del proyecto. 
Total 
5.0 
 
 
Nota individual: La nota de la sustentación es individual: el docente puede dirigir 
preguntas a cada integrante. Un integrante que no pueda explicar su parte del 
proyecto podrá recibir una nota distinta a la del grupo. 
Integridad académica: La copia de proyectos entre grupos o la entrega de código 
que el grupo no pueda explicar se tratará según el reglamento estudiantil. 
 

--- Página 9 ---
9 
 
INTELIGENCIA ARTIFICIAL – JHON JAMES CANO SÁNCHEZ 
6. Lista de Verificación Antes de Entregar 
• 
☐ El repositorio es público y el enlace abre en una ventana de incógnito. 
• 
☐ Clonar el repositorio en otra carpeta y ejecutarlo desde cero con docker-
compose up -d --build: funciona. 
• 
☐ usar_modelo.py se ejecuta sin volver a entrenar. 
• 
☐ El informe está en PDF, cumple APA 7 y tiene entre 12 y 20 páginas de 
contenido. 
• 
☐ Las cifras del informe coinciden con las que imprime el código. 
• 
☐ La declaración de uso de IA está incluida. 
• 
☐ La presentación en PDF incluye capturas de la demostración (plan B). 
• 
☐ Los tres archivos/enlaces están cargados en AVACO antes de las 11:59 p. m. 
del día anterior. 
7. Cronograma Sugerido para los Grupos 
Fecha 
Meta del grupo 
Hasta el 6 de noviembre 
Leer la retroalimentación del Avance 2 y planear las correcciones. 
9 de noviembre (Clase 12) 
Primer modelo_proyecto.py funcionando en clase. 
10 al 15 de noviembre 
Completar los modelos, guardar el mejor y crear 
usar_modelo.py; congelar resultados. 
16 al 20 de noviembre 
Redactar el informe APA con los resultados congelados. 
Día anterior a la sustentación 
Entrega en AVACO; ensayo cronometrado de 6 minutos. 
23 de noviembre 
Sustentación presencial. 
 
