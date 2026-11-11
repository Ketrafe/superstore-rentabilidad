# Resultados de las consultas SQL

## 1. Rentabilidad por categoría

```sql
SELECT category,
       ROUND(SUM(sales), 0)  AS ventas,
       ROUND(SUM(profit), 0) AS utilidad,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margen_pct
FROM ventas
GROUP BY category
ORDER BY utilidad
```

| category | ventas | utilidad | margen_pct |
|---|---|---|---|
| Furniture | 742000.0 | 18451.0 | 2.5 |
| Office Supplies | 719047.0 | 122491.0 | 17.0 |
| Technology | 836154.0 | 145455.0 | 17.4 |

## 2. Margen según tramo de descuento

```sql
SELECT CASE
         WHEN discount = 0    THEN '0%'
         WHEN discount <= 0.1 THEN '0-10%'
         WHEN discount <= 0.2 THEN '10-20%'
         WHEN discount <= 0.3 THEN '20-30%'
         WHEN discount <= 0.5 THEN '30-50%'
         ELSE '>50%'
       END AS tramo_descuento,
       COUNT(*) AS lineas,
       ROUND(SUM(profit), 0) AS utilidad,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margen_pct
FROM ventas
GROUP BY tramo_descuento
ORDER BY MIN(discount)
```

| tramo_descuento | lineas | utilidad | margen_pct |
|---|---|---|---|
| 0% | 4798 | 320988.0 | 29.5 |
| 0-10% | 94 | 9029.0 | 16.6 |
| 10-20% | 3709 | 91756.0 | 11.6 |
| 20-30% | 227 | -10369.0 | -10.0 |
| 30-50% | 310 | -48448.0 | -24.8 |
| >50% | 856 | -76559.0 | -119.2 |

## 3. Diez productos con mayor pérdida

```sql
SELECT product_name, ROUND(SUM(profit), 0) AS utilidad
FROM ventas
GROUP BY product_name
ORDER BY utilidad
LIMIT 10
```

| product_name | utilidad |
|---|---|
| Cubify CubeX 3D Printer Double Head Print | -8880.0 |
| Lexmark MX611dhe Monochrome Laser Printer | -4590.0 |
| Cubify CubeX 3D Printer Triple Head Print | -3840.0 |
| Chromcraft Bull-Nose Wood Oval Conference Tables & Bases | -2876.0 |
| Bush Advantage Collection Racetrack Conference Table | -1934.0 |
| GBC DocuBind P400 Electric Binding System | -1878.0 |
| Cisco TelePresence System EX90 Videoconferencing Unit | -1811.0 |
| Martin Yale Chadless Opener Electric Letter Opener | -1299.0 |
| Balt Solid Wood Round Tables | -1201.0 |
| BoxOffice By Design Rectangular and Half-Moon Meeting Room Tables | -1148.0 |

## 4. Crecimiento mensual de ventas (función de ventana)

```sql
WITH mensual AS (
  SELECT strftime('%Y-%m', order_date) AS mes, SUM(sales) AS ventas
  FROM ventas
  GROUP BY mes
)
SELECT mes,
       ROUND(ventas, 0) AS ventas,
       ROUND(100.0 * (ventas - LAG(ventas) OVER (ORDER BY mes)) / LAG(ventas) OVER (ORDER BY mes), 1) AS var_mensual_pct
FROM mensual
ORDER BY mes
```

| mes | ventas | var_mensual_pct |
|---|---|---|
| 2014-01 | 14237.0 |  |
| 2014-02 | 4520.0 | -68.3 |
| 2014-03 | 55691.0 | 1132.1 |
| 2014-04 | 28295.0 | -49.2 |
| 2014-05 | 23648.0 | -16.4 |
| 2014-06 | 34595.0 | 46.3 |
| 2014-07 | 33946.0 | -1.9 |
| 2014-08 | 27909.0 | -17.8 |
| 2014-09 | 81777.0 | 193.0 |
| 2014-10 | 31453.0 | -61.5 |
| 2014-11 | 78629.0 | 150.0 |
| 2014-12 | 69546.0 | -11.6 |
| 2015-01 | 18174.0 | -73.9 |
| 2015-02 | 11951.0 | -34.2 |
| 2015-03 | 38726.0 | 224.0 |
| 2015-04 | 34195.0 | -11.7 |
| 2015-05 | 30132.0 | -11.9 |
| 2015-06 | 24797.0 | -17.7 |
| 2015-07 | 28765.0 | 16.0 |
| 2015-08 | 36898.0 | 28.3 |
| 2015-09 | 64596.0 | 75.1 |
| 2015-10 | 31405.0 | -51.4 |
| 2015-11 | 75973.0 | 141.9 |
| 2015-12 | 74920.0 | -1.4 |
| 2016-01 | 18542.0 | -75.3 |
| 2016-02 | 22979.0 | 23.9 |
| 2016-03 | 51716.0 | 125.1 |
| 2016-04 | 38750.0 | -25.1 |
| 2016-05 | 56988.0 | 47.1 |
| 2016-06 | 40345.0 | -29.2 |
| 2016-07 | 39262.0 | -2.7 |
| 2016-08 | 31115.0 | -20.7 |
| 2016-09 | 73410.0 | 135.9 |
| 2016-10 | 59688.0 | -18.7 |
| 2016-11 | 79412.0 | 33.0 |
| 2016-12 | 96999.0 | 22.1 |
| 2017-01 | 43971.0 | -54.7 |
| 2017-02 | 20301.0 | -53.8 |
| 2017-03 | 58872.0 | 190.0 |
| 2017-04 | 36522.0 | -38.0 |
| 2017-05 | 44261.0 | 21.2 |
| 2017-06 | 52982.0 | 19.7 |
| 2017-07 | 45264.0 | -14.6 |
| 2017-08 | 63121.0 | 39.4 |
| 2017-09 | 87867.0 | 39.2 |
| 2017-10 | 77777.0 | -11.5 |
| 2017-11 | 118448.0 | 52.3 |
| 2017-12 | 83829.0 | -29.2 |

## 5. Sub-categorías con pérdida y su descuento promedio

```sql
SELECT category, sub_category,
       ROUND(SUM(profit), 0) AS utilidad,
       ROUND(AVG(discount) * 100, 1) AS descuento_prom_pct
FROM ventas
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY utilidad
```

| category | sub_category | utilidad | descuento_prom_pct |
|---|---|---|---|
| Furniture | Tables | -17725.0 | 26.1 |
| Furniture | Bookcases | -3473.0 | 21.1 |
| Office Supplies | Supplies | -1189.0 | 7.7 |
