SELECT name, high, ts, hour
FROM(
 SELECT *,SUBSTRING(ts, 12, 2) AS hour, 
 ROW_NUMBER() OVER(PARTITION BY name, SUBSTRING(ts, 12, 2) ORDER BY high desc) as row_num
 FROM "yfinance_db"."18" 
) d
WHERE row_num=1 
ORDER BY name, ts