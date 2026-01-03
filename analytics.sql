-- ============================================================
-- Query 1: Regional Performance vs Sales Targets for Q4
-- ============================================================

SELECT
    s.region,
    SUM(o.quantity * o.unit_price) AS actual_revenue,
    t.target_amount,
    CASE
        WHEN t.target_amount = 0 THEN 0
        ELSE ROUND(
            (SUM(o.quantity * o.unit_price) / t.target_amount) * 100,
            2
        )
    END AS percent_of_target
FROM Suppliers s
JOIN Orders o
    ON s.supplier_id = o.supplier_id
JOIN Sales_Targets t
    ON s.region = t.region
WHERE
    t.quarter = 'Q4-2025'
    AND o.order_date BETWEEN '2025-10-01' AND '2025-12-31'
GROUP BY
    s.region,
    t.target_amount
ORDER BY
    percent_of_target DESC;

-- ============================================================
-- Query 2: Top 3 Suppliers per Region by Revenue for Q4
-- ============================================================

SELECT
    region,
    farm_name,
    total_revenue,
    regional_rank
FROM (
    SELECT
        s.region,
        s.farm_name,
        SUM(o.quantity * o.unit_price) AS total_revenue,
        RANK() OVER (
            PARTITION BY s.region
            ORDER BY SUM(o.quantity * o.unit_price) DESC
        ) AS regional_rank
    FROM Suppliers s
    JOIN Orders o
        ON s.supplier_id = o.supplier_id
    WHERE
        o.order_date BETWEEN '2025-10-01' AND '2025-12-31'
    GROUP BY
        s.supplier_id,
        s.region,
        s.farm_name
) ranked_suppliers
WHERE regional_rank <= 3
ORDER BY region, regional_rank;

