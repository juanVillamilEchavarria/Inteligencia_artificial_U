from controllers.MovementController import MovementController
from datetime import datetime


class FinancialReportGenerator:
    def __init__(self, controller: MovementController):
        self.controller = controller

    def generate(self, outputPath: str = 'informe_proyecto.md') -> str:
        totalIncomes = self.controller.getTotalIncomes()
        totalExpenses = self.controller.getTotalExpenses()
        avgIncomes = self.controller.getIncomesAverage()
        avgExpenses = self.controller.getExpensesAverage()
        maxIncome = self.controller.getMaxIncome()
        minIncome = self.controller.getMinIncome()
        maxExpense = self.controller.getMaxExpense()
        minExpense = self.controller.getMinExpense()
        balance = totalIncomes - totalExpenses

        countIncomes = len(self.controller.service.getIncomes())
        countExpenses = len(self.controller.service.getExpenses())
        totalMovements = countIncomes + countExpenses

        markdown = f"""# Leo Counter AI - Informe Estadístico de Finanzas

## Descripción de los Datos

El presente informe analiza un dataset de **{totalMovements} transacciones financieras** extraídas del sistema Leo Counter, un gestor de finanzas open-source para hogares y PyMEs. Los datos incluyen movimientos de tipo **Ingreso** y **Gasto** registrados en múltiples cuentas (Banco Bogotá, Nequi, Bancolombia, Davivienda, DaviPlata, Efectivo, entre otras), con montos expresados en pesos colombianos (COP).

Cada registro contiene: identificador único (UUID), nombre de la transacción, cuenta asociada, categoría, tipo de movimiento, monto, fecha y descripción en texto libre. El período abarcado comprende desde agosto de 2026 hasta junio de 2024.

---

## Estadísticas Calculadas

### Resumen General

| Métrica | Valor |
|---------|------:|
| Total de movimientos | {totalMovements} |
| Cantidad de ingresos | {countIncomes} |
| Cantidad de gastos | {countExpenses} |
| Balance neto | ${balance:,.2f} |

### Ingresos

| Métrica | Valor |
|---------|------:|
| Total de ingresos | ${totalIncomes:,.2f} |
| Promedio por ingreso | ${avgIncomes:,.2f} |
| Ingreso máximo | ${maxIncome:,.2f} |
| Ingreso mínimo | ${minIncome:,.2f} |

### Gastos

| Métrica | Valor |
|---------|------:|
| Total de gastos | ${totalExpenses:,.2f} |
| Promedio por gasto | ${avgExpenses:,.2f} |
| Gasto máximo | ${maxExpense:,.2f} |
| Gasto mínimo | ${minExpense:,.2f} |

---

## Interpretación de los Resultados

### Análisis del Balance
El balance neto de **${balance:,.2f}** indica que los ingresos superan a los gastos en el período analizado. Sin embargo, este resultado debe interpretarse con cautela: el ingreso máximo de **${maxIncome:,.2f}** corresponde a una venta extraordinaria (vehículo), lo que distorsiona el promedio. Al excluir este valor atípico, el comportamiento financiero real podría ser significativamente diferente.

### Análisis de Ingresos
El promedio de ingresos de **${avgIncomes:,.2f}** está fuertemente influenciado por transacciones extraordinarias. La brecha entre el ingreso mínimo (**${minIncome:,.2f}**) y el máximo (**${maxIncome:,.2f}**) es de **${maxIncome - minIncome:,.2f}**, lo que evidencia alta variabilidad en las fuentes de ingreso. Esto es relevante para el modelo de **Puntaje Z**, ya que transacciones como la venta del vehículo serían detectadas como anomalías estadísticas.

### Análisis de Gastos
El gasto promedio de **${avgExpenses:,.2f}** refleja un patrón de consumo distribuido en múltiples categorías. El gasto máximo (**${maxExpense:,.2f}**) corresponde a una compra de tecnología (laptop), mientras que el mínimo (**${minExpense:,.2f}**) es un pasaje de transporte público. La dispersión entre estos valores confirma la necesidad de implementar **sub-categorías** mediante Naive Bayes, ya que agrupar todos los gastos en una sola categoría oculta patrones importantes de consumo.

### Relación con el Proyecto de IA
Estas estadísticas son la base para:
1. **Detección de anomalías**: El Puntaje Z utilizará la media y desviación estándar de estos montos para identificar transacciones atípicas en tiempo real.
2. **Clasificación semántica**: Las descripciones en texto libre asociadas a estos montos alimentarán el modelo Naive Bayes para detectar sub-categorías ocultas.
3. **Reportes inteligentes**: Estas métricas básicas evolucionarán hacia insights accionables cuando se integre el módulo de IA al sistema Leo Counter.

---

*Informe generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} por Leo Counter AI - Módulo de Estadísticas.*
"""
        with open(outputPath, 'w', encoding='utf-8') as file:
            file.write(markdown)

        return outputPath
