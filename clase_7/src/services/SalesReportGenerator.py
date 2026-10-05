from controllers.SalesController import SalesController
from datetime import datetime


class SalesReportGenerator:
    def __init__(self, controller: SalesController):
        self.controller = controller

    def generate(self, output_path: str = 'informe_ventas.md'):
        stats_service = self.controller.service
        
        total_sales = stats_service.get_total_sales()
        avg_sale = stats_service.get_average_sale()
        min_sale = stats_service.get_min_sale()
        max_sale = stats_service.get_max_sale()
        count_sales = stats_service.sales_collection.count()
        null_ages = stats_service.get_null_age_count()
        
        categories = stats_service.get_categories()
        cat_stats = {}
        for cat in categories:
            cat_stats[cat] = stats_service.get_total_sales_by_category(cat)
        
        payment_methods = stats_service.get_payment_methods()
        cities = stats_service.get_cities()

        markdown = f"""# Informe Estadístico de Ventas

## Descripción de los Datos

El presente informe analiza un dataset de **{count_sales} transacciones de ventas** de una tienda. Los datos incluyen información sobre producto, categoría, precio unitario, cantidad, ciudad, edad del cliente y método de pago.

Cada registro contiene: identificador único, fecha, producto, categoría, precio unitario, cantidad, ciudad, edad del cliente y método de pago. El período abarcado comprende enero de 2025.

---

## Estadísticas Calculadas

### Resumen General

| Métrica | Valor |
|---------|------:|
| Total de transacciones | {count_sales} |
| Total de ventas | ${total_sales:,.2f} |
| Promedio por transacción | ${avg_sale:,.2f} |
| Venta mínima | ${min_sale:,.2f} |
| Venta máxima | ${max_sale:,.2f} |
| Valores nulos en edad del cliente | {null_ages} |

### Ventas por Categoría

| Categoría | Total Ventas |
|-----------|-------------:|"""

        for cat, total in sorted(cat_stats.items(), key=lambda x: x[1], reverse=True):
            markdown += f"\n| {cat} | ${total:,.2f} |"

        markdown += f"""

### Métodos de Pago

| Método | Cantidad |
|--------|---------:|"""

        for method in payment_methods:
            sales = stats_service.get_sales_by_payment_method(method)
            markdown += f"\n| {method} | {len(sales)} |"

        markdown += f"""

### Ciudades

| Ciudad | Cantidad |
|--------|---------:|"""

        for city in cities:
            sales = stats_service.sales_collection.get_by_key(
                __import__('enums.SaleFilteringKeys', fromlist=['SaleFilteringKeys']).SaleFilteringKeys.CIUDAD, city
            )
            markdown += f"\n| {city} | {len(sales)} |"

        markdown += f"""

---

## Interpretación de los Resultados

### Análisis General
El total de ventas asciende a **${total_sales:,.2f}** distribuido en **{count_sales} transacciones** con un promedio de **${avg_sale:,.2f}** por transacción. La venta máxima fue de **${max_sale:,.2f}** y la mínima de **${min_sale:,.2f}**.

### Análisis por Categoría
La categoría con mayor volumen de ventas es **{max(cat_stats, key=cat_stats.get)}** con **${max(cat_stats.values()):,.2f}**, mientras que la de menor volumen es **{min(cat_stats, key=cat_stats.get)}** con **${min(cat_stats.values()):,.2f}**.

### Calidad de Datos
Se detectaron **{null_ages} valores nulos en la edad del cliente**, los cuales fueron imputados con la mediana para el análisis.

---

*Informe generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.*
"""
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown)
        
        print(f"Informe generado correctamente: {output_path}")