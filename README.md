# IBM-HR-Analytics-Project2
## Project Overview  
This project analyzes employee attrition using IBM's HR Analytics dataset (1,470 employees, 35 features). The goal is to identify key factors driving employee turnover and build predictive models to flag at-risk employees. The project combines Excel dashboards for business intelligence, SQL for data querying, and Machine Learning (Random Forest) for attrition prediction. Key findings reveal that overtime (3x higher attrition), low job satisfaction, and poor work-life balance are the strongest predictors of employee departure. The final deliverable includes an interactive Excel dashboard, 30+ SQL queries, and a production-ready ML model with 85% accuracy.

## Business Problem
Companies lose millions in recruitment and training costs due to employee turnover. This project helps HR teams:
- Identify employees likely to leave
- Understand root causes of attrition
- Take proactive retention actions

## Tools & Technologies
- **Python** - Data cleaning, EDA, Machine Learning
- **Excel** - Interactive dashboards, Pivot Tables
- **SQL** - Data extraction and analysis
- **Scikit-learn** - Random Forest, Logistic Regression

### Dataset used 1,470 employees | 35 features | 16.1% attrition rate
-	<a href="https://github.com/SelvaTharsan/Coffee-Sales-Analysis/blob/main/coffee%20sales_Dataset.csv"> Dataset </a>

## Excel Dashboard Features
- KPI Cards (Total Employees, Attrition Rate, etc.)
- 7 Interactive Charts
- Slicers for Department, Gender, Education
- Real-time filtering

  ## Machine Learning Performance

| Model | Accuracy | ROC-AUC |
|-------|----------|---------|
| Random Forest | 86.5% | 0.89 |
| Logistic Regression | 84.2% | 0.85 |
| Decision Tree | 82.1% | 0.81 |

**Top 5 Attrition Predictors:**
1. Overtime
2. Years at Company
3. Job Satisfaction
4. Monthly Income
5. Age


## Key Insights
-	Overtime employees have 30.53% attrition vs 10.44% without overtime (3x higher)
-	Age 18-25 has highest attrition at 35.77%; Age 36-45 has lowest at 9.19%
-	Sales department has highest attrition at 20.63%; R&D has lowest at 13.84%
-	Leavers earn $2,046 less on average ($4,787 vs $6,833 for stayers)
-	Low job satisfaction = 22.84% attrition; Very high satisfaction = 11.33% attrition
-	No stock option = 24.41% attrition; Stock option Level 2 = 7.59% attrition (70% reduction)

## Conclusion
The analysis reveals that overtime, age (18-25), and low job satisfaction are the strongest drivers of employee attrition, with overtime employees being 3x more likely to leave. The Random Forest model predicts attrition with 86.5% accuracy, identifying at-risk employees effectively. To reduce attrition from 16.12% to under 10%, IBM should prioritize overtime reduction, targeted retention programs for young employees, and compensation improvements for Bachelor's degree holders in the Sales department.

## Project Output
### Dashboard Preview
<img width="1366" height="618" alt="Dashboard" src="https://github.com/SelvaTharsan/Coffee-Sales-Analysis/blob/main/Dashboard.jpg" />

### SQL Results
[View Report](https://github.com/SelvaTharsan/Coffee-Sales-Analysis/blob/main/MY%20SQL%20QUERIES.sql)
  
### Model Predictions 
[View Report](https://github.com/SelvaTharsan/Coffee-Sales-Analysis/blob/main/project-1-coffee-sales.py)














