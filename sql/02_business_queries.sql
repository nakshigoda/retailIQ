-- =====================================
-- 1. Overall Business Performance
-- =====================================

SELECT
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Profit),2) AS Total_Profit,
    SUM(Quantity) AS Total_Items_Sold,
    COUNT(DISTINCT `Order ID`) AS Total_Orders
FROM sales;

SELECT
    Category,
    ROUND(SUM(Sales),2) AS Total_Sales,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC;

SELECT
    `Product Name`,
    ROUND(SUM(Sales),2) AS Revenue,
    ROUND(SUM(Profit),2) AS Profit
FROM sales
GROUP BY `Product Name`
ORDER BY Revenue DESC
LIMIT 10;

SELECT
    `Customer Name`,
    ROUND(SUM(Sales),2) AS Total_Spent
FROM sales
GROUP BY `Customer Name`
ORDER BY Total_Spent DESC
LIMIT 10;

SELECT
    Market,
    ROUND(SUM(Sales),2) AS Revenue,
    ROUND(SUM(Profit),2) AS Profit
FROM sales
GROUP BY Market
ORDER BY Revenue DESC;

SELECT
    `Order Year`,
    `Order Month`,
    ROUND(SUM(Sales),2) AS Total_Sales
FROM sales
GROUP BY `Order Year`, `Order Month`
ORDER BY `Order Year`,
FIELD(`Order Month`,
'January','February','March','April','May','June',
'July','August','September','October','November','December');

SELECT
    Region,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM sales
GROUP BY Region
ORDER BY Total_Profit DESC;

SELECT
    Category,
    ROUND(AVG(Discount)*100,2) AS Avg_Discount_Percentage
FROM sales
GROUP BY Category;

SELECT
    `Ship Mode`,
    ROUND(AVG(`Shipping Days`),2) AS Avg_Shipping_Days
FROM sales
GROUP BY `Ship Mode`;

SELECT
    `Product Name`,
    ROUND(SUM(Profit),2) AS Total_Profit
FROM sales
GROUP BY `Product Name`
ORDER BY Total_Profit ASC
LIMIT 10;