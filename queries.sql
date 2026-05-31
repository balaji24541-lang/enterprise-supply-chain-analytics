-- ============================================================================
--
-- ============================================================================

SELECT 
    `Shipping Mode`,
    COUNT(*) as Total_Shipments,
    ROUND(AVG(`Days for shipping (real)`), 2) as Avg_Actual_Transit_Days,
    ROUND(AVG(`Scheduled_Transit_Window`), 2) as Avg_Scheduled_Transit_Days,
    ROUND(AVG(`Days for shipping (real)` - `Scheduled_Transit_Window`), 2) as Avg_SLA_Breach_Days,
    ROUND(AVG(Delay_Probability) * 100, 2) as Model_Predicted_Delay_Rate_Pct
FROM 
    supply_chain_predictions
GROUP BY 
    `Shipping Mode`
ORDER BY 
    Avg_SLA_Breach_Days DESC;


-- ============================================================================
-- 
-- ============================================================================

SELECT 
    `Customer Region`,
    COUNT(*) as Impacted_Order_Volume,
    ROUND(SUM(Sales), 2) as Total_Gross_Revenue,
    ROUND(SUM(Revenue_At_Risk), 2) as Total_Financial_Capital_At_Risk,
    ROUND((SUM(Revenue_At_Risk) / SUM(Sales)) * 100, 2) as Regional_Risk_Exposure_Ratio_Pct
FROM 
    supply_chain_predictions
GROUP BY 
    `Customer Region`
HAVING 
    Total_Financial_Capital_At_Risk > 
ORDER BY 
    Total_Financial_Capital_At_Risk DESC;
