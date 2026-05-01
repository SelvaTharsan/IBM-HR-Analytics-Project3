-- 1. TOTAL ATTRITION ANALYSIS

-- OVERALL ATTRITION RATE
SELECT 
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS employees_left,
    SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) AS employees_stayed,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate_percent
FROM employee_attrition;

-- TOTAL ORDERS (TRANSACTIONS) - COUNT OF EMPLOYEES
SELECT COUNT(*) AS total_employees
FROM employee_attrition;

-- ATTRITION BY DEMOGRAPHICS

-- ATTRITION BY AGE GROUP
SELECT 
    CASE 
        WHEN Age BETWEEN 18 AND 25 THEN '18-25'
        WHEN Age BETWEEN 26 AND 35 THEN '26-35'
        WHEN Age BETWEEN 36 AND 45 THEN '36-45'
        WHEN Age BETWEEN 46 AND 55 THEN '46-55'
        ELSE '56+'
    END AS age_group,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY age_group
ORDER BY attrition_rate DESC;

-- ATTRITION BY GENDER
SELECT 
    Gender,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY Gender
ORDER BY attrition_rate DESC;

-- ATTRITION BY EDUCATION LEVEL
SELECT 
    Education,
    CASE Education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END AS education_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY Education
ORDER BY attrition_rate DESC;

-- ATTRITION BY MARITAL STATUS
SELECT 
    MaritalStatus,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY MaritalStatus
ORDER BY attrition_rate DESC;

-- 3. ATTRITION BY DEPARTMENT & JOB ROLE

-- ATTRITION BY DEPARTMENT
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY Department
ORDER BY attrition_rate DESC;

-- ATTRITION BY JOB ROLE
SELECT 
    JobRole,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY JobRole
ORDER BY attrition_rate DESC;

-- ATTRITION BY JOB LEVEL
SELECT 
    JobLevel,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY JobLevel
ORDER BY JobLevel;

-- 4. INCOME & COMPENSATION ANALYSIS

-- MONTHLY INCOME COMPARISON (ATTRITION VS NON-ATTRITION)
SELECT 
    Attrition,
    COUNT(*) AS employee_count,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(MIN(MonthlyIncome), 2) AS min_income,
    ROUND(MAX(MonthlyIncome), 2) AS max_income
FROM employee_attrition
GROUP BY Attrition;

-- AVERAGE MONTHLY INCOME BY EDUCATION AND ATTRITION
SELECT 
    CASE Education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END AS education_level,
    Attrition,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    COUNT(*) AS employee_count
FROM employee_attrition
GROUP BY Education, Attrition
ORDER BY Education, Attrition;

-- PERCENT SALARY HIKE IMPACT
SELECT 
    Attrition,
    ROUND(AVG(PercentSalaryHike), 2) AS avg_salary_hike,
    ROUND(MIN(PercentSalaryHike), 2) AS min_hike,
    ROUND(MAX(PercentSalaryHike), 2) AS max_hike
FROM employee_attrition
GROUP BY Attrition;

-- STOCK OPTION LEVEL IMPACT
SELECT 
    StockOptionLevel,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY StockOptionLevel
ORDER BY StockOptionLevel;

-- JOB SATISFACTION & WORK-LIFE BALANCE

-- JOB SATISFACTION IMPACT
SELECT 
    CASE JobSatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS satisfaction_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY JobSatisfaction
ORDER BY JobSatisfaction;

-- WORK-LIFE BALANCE IMPACT
SELECT 
    CASE WorkLifeBalance
        WHEN 1 THEN 'Bad'
        WHEN 2 THEN 'Good'
        WHEN 3 THEN 'Better'
        WHEN 4 THEN 'Best'
    END AS wlb_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY WorkLifeBalance
ORDER BY WorkLifeBalance;

-- ENVIRONMENT SATISFACTION IMPACT
SELECT 
    CASE EnvironmentSatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS env_satisfaction,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY EnvironmentSatisfaction
ORDER BY EnvironmentSatisfaction;

-- JOB INVOLVEMENT IMPACT
SELECT 
    CASE JobInvolvement
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS involvement_level,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY JobInvolvement
ORDER BY JobInvolvement;

-- OVERTIME & BUSINESS TRAVEL IMPACT

-- OVERTIME IMPACT
SELECT 
    OverTime,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY OverTime;

-- BUSINESS TRAVEL IMPACT
SELECT 
    BusinessTravel,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY BusinessTravel
ORDER BY attrition_rate DESC;

-- 7. TENURE & PROMOTION ANALYSIS

-- YEARS AT COMPANY ANALYSIS
SELECT 
    Attrition,
    ROUND(AVG(YearsAtCompany), 2) AS avg_years_at_company,
    ROUND(MIN(YearsAtCompany), 2) AS min_years,
    ROUND(MAX(YearsAtCompany), 2) AS max_years
FROM employee_attrition
GROUP BY Attrition;

-- YEARS SINCE LAST PROMOTION IMPACT
SELECT 
    promotion_gap,
    Attrition,
    employee_count,
    ROUND(100.0 * employee_count / SUM(employee_count) OVER (PARTITION BY promotion_gap), 2) AS percentage
FROM (
    SELECT 
        CASE 
            WHEN YearsSinceLastPromotion = 0 THEN 'No promotion'
            WHEN YearsSinceLastPromotion BETWEEN 1 AND 2 THEN '1-2 years'
            WHEN YearsSinceLastPromotion BETWEEN 3 AND 5 THEN '3-5 years'
            ELSE '5+ years'
        END AS promotion_gap,
        Attrition,
        COUNT(*) AS employee_count
    FROM employee_attrition
    GROUP BY promotion_gap, Attrition
) AS subquery
ORDER BY promotion_gap, Attrition;

-- NUMBER OF COMPANIES WORKED IMPACT
SELECT 
    NumCompaniesWorked,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY NumCompaniesWorked
ORDER BY NumCompaniesWorked;

-- YEARS IN CURRENT ROLE IMPACT
SELECT 
    Attrition,
    ROUND(AVG(YearsInCurrentRole), 2) AS avg_years_in_role,
    ROUND(MIN(YearsInCurrentRole), 2) AS min_years,
    ROUND(MAX(YearsInCurrentRole), 2) AS max_years
FROM employee_attrition
GROUP BY Attrition;

-- YEARS WITH CURRENT MANAGER IMPACT
SELECT 
    Attrition,
    ROUND(AVG(YearsWithCurrManager), 2) AS avg_years_with_manager,
    ROUND(MIN(YearsWithCurrManager), 2) AS min_years,
    ROUND(MAX(YearsWithCurrManager), 2) AS max_years
FROM employee_attrition
GROUP BY Attrition;

-- 8. DISTANCE & RELATIONSHIP ANALYSIS

-- DISTANCE FROM HOME IMPACT
SELECT 
    CASE 
        WHEN DistanceFromHome <= 5 THEN '0-5 miles'
        WHEN DistanceFromHome BETWEEN 6 AND 15 THEN '6-15 miles'
        WHEN DistanceFromHome BETWEEN 16 AND 25 THEN '16-25 miles'
        ELSE '25+ miles'
    END AS distance_category,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY distance_category
ORDER BY distance_category;

-- RELATIONSHIP SATISFACTION IMPACT
SELECT 
    CASE RelationshipSatisfaction
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Medium'
        WHEN 3 THEN 'High'
        WHEN 4 THEN 'Very High'
    END AS relationship_satisfaction,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY RelationshipSatisfaction
ORDER BY RelationshipSatisfaction;

-- 9. BONUS QUESTIONS FROM PDF

-- BREAKDOWN OF DISTANCE FROM HOME BY JOB ROLE AND ATTRITION
SELECT 
    JobRole,
    Attrition,
    ROUND(AVG(DistanceFromHome), 2) AS avg_distance,
    ROUND(MIN(DistanceFromHome), 2) AS min_distance,
    ROUND(MAX(DistanceFromHome), 2) AS max_distance,
    COUNT(*) AS employee_count
FROM employee_attrition
GROUP BY JobRole, Attrition
ORDER BY JobRole, Attrition;

-- COMPARE AVERAGE MONTHLY INCOME BY EDUCATION AND ATTRITION
SELECT 
    CASE Education
        WHEN 1 THEN 'Below College'
        WHEN 2 THEN 'College'
        WHEN 3 THEN 'Bachelor'
        WHEN 4 THEN 'Master'
        WHEN 5 THEN 'Doctor'
    END AS education_level,
    Attrition,
    ROUND(AVG(MonthlyIncome), 2) AS avg_monthly_income,
    ROUND(MIN(MonthlyIncome), 2) AS min_income,
    ROUND(MAX(MonthlyIncome), 2) AS max_income
FROM employee_attrition
GROUP BY Education, Attrition
ORDER BY Education, Attrition;


-- 10. TOP PERFORMING PRODUCTS

-- TOP 10 JOB ROLES BY ATTRITION COUNT
SELECT 
    JobRole,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY JobRole
ORDER BY left_count DESC
LIMIT 10;

-- TOP 10 DEPARTMENTS BY ATTRITION
SELECT 
    Department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY Department
ORDER BY left_count DESC;

-- 11. PERFORMANCE RATING ANALYSIS

-- PERFORMANCE RATING VS ATTRITION
SELECT 
    CASE PerformanceRating
        WHEN 1 THEN 'Low'
        WHEN 2 THEN 'Good'
        WHEN 3 THEN 'Excellent'
        WHEN 4 THEN 'Outstanding'
    END AS rating,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY PerformanceRating
ORDER BY PerformanceRating;


-- 12. TRAINING & DEVELOPMENT

-- TRAINING TIMES LAST YEAR IMPACT
SELECT 
    TrainingTimesLastYear,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) AS left_count,
    ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS attrition_rate
FROM employee_attrition
GROUP BY TrainingTimesLastYear
ORDER BY TrainingTimesLastYear;


-- 13. COMPLETE SUMMARY STATISTICS BY ATTRITION

SELECT 'Total Employees' AS metric, 
       CONCAT(COUNT(*)) AS stayed, 
       CONCAT(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)) AS left_value, 
       CONCAT(ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2), '%') AS left_percent
FROM employee_attrition

UNION ALL

SELECT 'Avg Age', 
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'No' THEN Age END), 1)),
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN Age END), 1)),
       '-'
FROM employee_attrition

UNION ALL

SELECT 'Avg Monthly Income', 
       CONCAT('$', ROUND(AVG(CASE WHEN Attrition = 'No' THEN MonthlyIncome END), 0)),
       CONCAT('$', ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END), 0)),
       '-'
FROM employee_attrition

UNION ALL

SELECT 'Avg Years at Company', 
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'No' THEN YearsAtCompany END), 1)),
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN YearsAtCompany END), 1)),
       '-'
FROM employee_attrition

UNION ALL

SELECT 'Avg Job Satisfaction', 
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'No' THEN JobSatisfaction END), 2)),
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN JobSatisfaction END), 2)),
       '-'
FROM employee_attrition

UNION ALL

SELECT 'Avg Work Life Balance', 
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'No' THEN WorkLifeBalance END), 2)),
       CONCAT(ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN WorkLifeBalance END), 2)),
       '-'
FROM employee_attrition

UNION ALL

SELECT '% Overtime', 
       CONCAT(ROUND(100.0 * SUM(CASE WHEN Attrition = 'No' AND OverTime = 'Yes' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END), 0), 2), '%'),
       CONCAT(ROUND(100.0 * SUM(CASE WHEN Attrition = 'Yes' AND OverTime = 'Yes' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END), 0), 2), '%'),
       '-'
FROM employee_attrition;


-- 14. HIGH RISK EMPLOYEES IDENTIFICATION

SELECT 
    EmployeeNumber,
    Age,
    Department,
    JobRole,
    MaritalStatus,
    OverTime,
    YearsAtCompany,
    JobSatisfaction,
    WorkLifeBalance,
    MonthlyIncome,
    CASE 
        WHEN OverTime = 'Yes' AND JobSatisfaction <= 2 THEN 'CRITICAL'
        WHEN OverTime = 'Yes' OR JobSatisfaction <= 2 THEN 'HIGH'
        WHEN YearsAtCompany <= 2 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level
FROM employee_attrition
WHERE Attrition = 'No'
    AND (OverTime = 'Yes' OR JobSatisfaction <= 2 OR YearsAtCompany <= 2)
ORDER BY 
    CASE 
        WHEN OverTime = 'Yes' AND JobSatisfaction <= 2 THEN 1
        WHEN OverTime = 'Yes' OR JobSatisfaction <= 2 THEN 2
        ELSE 3
    END;


-- 15. DEPARTMENT-WISE ATTRITION RISK FACTORS

SELECT 
    Department,
    ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN JobSatisfaction END), 2) AS avg_satisfaction_leavers,
    ROUND(AVG(CASE WHEN Attrition = 'No' THEN JobSatisfaction END), 2) AS avg_satisfaction_stayers,
    ROUND(100.0 * SUM(CASE WHEN OverTime = 'Yes' AND Attrition = 'Yes' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END), 0), 2) AS pct_overtime_leavers,
    ROUND(100.0 * SUM(CASE WHEN OverTime = 'Yes' AND Attrition = 'No' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END), 0), 2) AS pct_overtime_stayers
FROM employee_attrition
GROUP BY Department;

-- 16. MONTHLY INCOME DISTRIBUTION BY DEPARTMENT

SELECT 
    Department,
    Attrition,
    ROUND(AVG(MonthlyIncome), 2) AS avg_income,
    ROUND(MIN(MonthlyIncome), 2) AS min_income,
    ROUND(MAX(MonthlyIncome), 2) AS max_income,
    COUNT(*) AS employee_count
FROM employee_attrition
GROUP BY Department, Attrition
ORDER BY Department, Attrition;
