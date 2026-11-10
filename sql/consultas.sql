-- Consultas para SQLite sobre la tabla `ventas` (ver src/cargar_a_sqlite.py)

-- 1. Rentabilidad por categoría
SELECT category,
       ROUND(SUM(sales), 0)  AS ventas,
       ROUND(SUM(profit), 0) AS utilidad,
       ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS margen_pct
FROM ventas
GROUP BY category
ORDER BY utilidad;

-- 2. Margen según tramo de descuento
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
ORDER BY MIN(discount);

-- 3. Diez productos con mayor pérdida
SELECT product_name, ROUND(SUM(profit), 0) AS utilidad
FROM ventas
GROUP BY product_name
ORDER BY utilidad
LIMIT 10;

-- 4. Crecimiento mensual de ventas (función de ventana)
WITH mensual AS (
  SELECT strftime('%Y-%m', order_date) AS mes, SUM(sales) AS ventas
  FROM ventas
  GROUP BY mes
)
SELECT mes,
       ROUND(ventas, 0) AS ventas,
       ROUND(100.0 * (ventas - LAG(ventas) OVER (ORDER BY mes)) / LAG(ventas) OVER (ORDER BY mes), 1) AS var_mensual_pct
FROM mensual
ORDER BY mes;

-- 5. Sub-categorías con pérdida y su descuento promedio
SELECT category, sub_category,
       ROUND(SUM(profit), 0) AS utilidad,
       ROUND(AVG(discount) * 100, 1) AS descuento_prom_pct
FROM ventas
GROUP BY category, sub_category
HAVING SUM(profit) < 0
ORDER BY utilidad;
