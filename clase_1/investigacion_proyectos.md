# Investigacion de proyectos

### 1. Categorizador y analizador de finanzas
El proyecto resuelve la necesidad de automatizar y auditar el seguimiento de finanzas, categorizando transacciones de forma autónoma y detectando fugas de dinero o consumos inusuales. Para alimentarlo, se requerirá un dataset compuesto por registros de transacciones que incluyan descripciones de texto crudo y sus respectivos montos numéricos. El motor utilizará un modelo probabilístico de **Naive Bayes Multinomial** para la clasificación semántica, acoplado a un modelo estadístico de **Puntaje Z** para la detección de anomalías financieras

## 2. Segmentación de clientes

La segmentación de clientes busca agrupar a los clientes de acuerdo con características y comportamientos similares, permitiendo identificar diferentes tipos de consumidores y diseñar estrategias comerciales para cada tipo de grupo. Se necesitarían datos como frecuencia de compra, la cantidad de compras, el dinero gastado, los productos adquiridos y tiempo desde la última compra. Un modelo adecuado sería un algoritmo de clustering como K-Means, que permitiría encontrar grupos de clientes con comportamientos similares.

## 3. Recomendador de rutas

Un recomendador de rutas busca encontrar la mejor ruta entre punto A y punto B, teniendo en cuenta factores como distancia, el tiempo de viaje, tráfico y posibles obstáculos en el camino. Para desarrollarlo se necesitarían datos de ubicaciones, carreteras, distancias, tiempos de recorrido y, si es posible, información histórica del tráfico. Se podría utilizar un algoritmo de búsqueda de caminos como A* o Dijkstra y complementarlo con modelos de aprendizaje automático para predecir los tiempos de viaje y recomendar la ruta más conveniente.