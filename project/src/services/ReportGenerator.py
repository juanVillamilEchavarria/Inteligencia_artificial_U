from controllers.MovementController import MovementController
from datetime import datetime

class ReportGenerator:
    def __init__(self, controller: MovementController):
        self.controller = controller

    def generate(self, output_path: str = 'informe_proyecto.md'):
        total_incomes = self.controller.getTotalIncomes()
        total_expenses = self.controller.getTotalExpenses()
        avg_incomes = self.controller.getIncomesAverage()
        avg_expenses = self.controller.getExpensesAverage()
        max_income = self.controller.getMaxIncome()
        min_income = self.controller.getMinIncome()
        max_expense = self.controller.getMaxExpense()
        min_expense = self.controller.getMinExpense()
        balance = total_incomes - total_expenses

        count_incomes = len(self.controller.service.getIncomes())
        count_expenses = len(self.controller.service.getExpenses())
        total_movements = count_incomes + count_expenses

        markdown = f"""# Leo Counter AI - Informe Estadístico de Finanzas

## Descripción de los Datos

El presente informe analiza un dataset de **{total_movements} transacciones financieras** extraídas del sistema Leo Counter, un gestor de finanzas open-source para hogares y PyMEs. Los datos incluyen movimientos de tipo **Ingreso** y **Gasto** registrados en múltiples cuentas (Banco Bogotá, Nequi, Bancolombia, Davivienda, DaviPlata, Efectivo, entre otras), con montos expresados en pesos colombianos (COP).

Cada registro contiene: identificador único (UUID), nombre de la transacción, cuenta asociada, categoría, tipo de movimiento, monto, fecha y descripción en texto libre. El período abarcado comprende desde agosto de 2026 hasta junio de 2024.

---

## Estadísticas Calculadas

### Resumen General

| Métrica | Valor |
|---------|------:|
| Total de movimientos | {total_movements} |
| Cantidad de ingresos | {count_incomes} |
| Cantidad de gastos | {count_expenses} |
| Balance neto | ${balance:,.2f} |

### Ingresos

| Métrica | Valor |
|---------|------:|
| Total de ingresos | ${total_incomes:,.2f} |
| Promedio por ingreso | ${avg_incomes:,.2f} |
| Ingreso máximo | ${max_income:,.2f} |
| Ingreso mínimo | ${min_income:,.2f} |

### Gastos

| Métrica | Valor |
|---------|------:|
| Total de gastos | ${total_expenses:,.2f} |
| Promedio por gasto | ${avg_expenses:,.2f} |
| Gasto máximo | ${max_expense:,.2f} |
| Gasto mínimo | ${min_expense:,.2f} |

---

## Interpretación de los Resultados

### Análisis del Balance
El balance neto de **${balance:,.2f}** indica que los ingresos superan a los gastos en el período analizado. Sin embargo, este resultado debe interpretarse con cautela: el ingreso máximo de **${max_income:,.2f}** corresponde a una venta extraordinaria (vehículo), lo que distorsiona el promedio. Al excluir este valor atípico, el comportamiento financiero real podría ser significativamente diferente.

### Análisis de Ingresos
El promedio de ingresos de **${avg_incomes:,.2f}** está fuertemente influenciado por transacciones extraordinarias. La brecha entre el ingreso mínimo (**${min_income:,.2f}**) y el máximo (**${max_income:,.2f}**) es de **${max_income - min_income:,.2f}**, lo que evidencia alta variabilidad en las fuentes de ingreso. Esto es relevante para el modelo de **Puntaje Z**, ya que transacciones como la venta del vehículo serían detectadas como anomalías estadísticas.

### Análisis de Gastos
El gasto promedio de **${avg_expenses:,.2f}** refleja un patrón de consumo distribuido en múltiples categorías. El gasto máximo (**${max_expense:,.2f}**) corresponde a una compra de tecnología (laptop), mientras que el mínimo (**${min_expense:,.2f}**) es un pasaje de transporte público. La dispersión entre estos valores confirma la necesidad de implementar **sub-categorías** mediante Naive Bayes, ya que agrupar todos los gastos en una sola categoría oculta patrones importantes de consumo.

### Relación con el Proyecto de IA
Estas estadísticas son la base para:
1. **Detección de anomalías**: El Puntaje Z utilizará la media y desviación estándar de estos montos para identificar transacciones atípicas en tiempo real.
2. **Clasificación semántica**: Las descripciones en texto libre asociadas a estos montos alimentarán el modelo Naive Bayes para detectar sub-categorías ocultas.
3. **Reportes inteligentes**: Estas métricas básicas evolucionarán hacia insights accionables cuando se integre el módulo de IA al sistema Leo Counter.

---

*Informe generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} por Leo Counter AI - Módulo de Estadísticas.*
"""
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown)
        
        print(f" Informe generado correctamente: {output_path}")