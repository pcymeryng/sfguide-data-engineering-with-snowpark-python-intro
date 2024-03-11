WITH cte_dau
AS (
  SELECT event_date AS "day",
  COUNT(DISTINCT userid) as dau
  FROM user_activity_log
  GROUP BY event_date
  ORDER BY 1
)
SELECT 
  a.dy,
  AVG(b.dau) AS "3_day_dau_avg"
FROM cte_dau a
INNER JOIN cte_dau b
ON b.dy BETWEEN DATEADD(day, -3, a.dy) AND a.dy
GROUP BY a.dy
ORDER BY a.dy
