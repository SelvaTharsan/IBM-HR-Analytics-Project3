# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, classification_report

warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")
pd.set_option('display.max_columns', 35)


#  LOAD AND EXPLORE DATA
print("IBM HR ANALYTICS - EMPLOYEE ATTRITION ANALYSIS")

# Load dataset
df = pd.read_csv('/kaggle/input/datasets/tharsthanu/ibm-hr-analytics/WA_Fn-UseC_-HR-Employee-Attrition.csv')

print(f"\n DATASET INFO:")
print(f"   Shape: {df.shape}")
print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n FIRST 5 ROWS:")
print(df.head())

print("\n DATA TYPES:")
print(df.dtypes)

print("\n MISSING VALUES CHECK:")
print(df.isnull().sum())

print(f"\n DUPLICATE ROWS: {df.duplicated().sum()}")

print("\n STATISTICAL SUMMARY:")
print(df.describe())

# UNDERSTAND CURRENT TURNOVER RATES
print(" UNDERSTAND CURRENT TURNOVER RATES")

# Overall Attrition Rate
attrition_counts = df['Attrition'].value_counts()
attrition_percent = df['Attrition'].value_counts(normalize=True) * 100

print(f"\n OVERALL ATTRITION RATE:")
print(f"   Total Employees: {len(df):,}")
print(f"   Employees who Left (Yes): {attrition_counts['Yes']} ({attrition_percent['Yes']:.2f}%)")
print(f"   Employees who Stayed (No): {attrition_counts['No']} ({attrition_percent['No']:.2f}%)")

# Visualization - Attrition Distribution
plt.figure(figsize=(8, 6))
colors = ['#2ecc71', '#e74c3c']
ax = sns.countplot(data=df, x='Attrition', palette=colors)
for i, p in enumerate(ax.patches):
    ax.annotate(f'{attrition_percent.iloc[i]:.1f}%', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=12, fontweight='bold')
plt.title('Employee Attrition Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Attrition')
plt.ylabel('Count')
plt.tight_layout()
plt.show()


# Attrition by Age Group
df['AgeGroup'] = pd.cut(df['Age'], bins=[18, 25, 35, 45, 55, 65], 
                         labels=['18-25', '26-35', '36-45', '46-55', '56+'])

age_attrition = df.groupby('AgeGroup', observed=True)['Attrition'].value_counts(normalize=True).unstack() * 100
age_attrition['Yes'] = age_attrition['Yes'].fillna(0)
age_attrition = age_attrition.sort_values('Yes', ascending=False)

print(f"\n ATTRITION BY AGE GROUP:")
for age, rate in age_attrition['Yes'].items():
    print(f"   • {age}: {rate:.2f}%")

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=age_attrition.index, y=age_attrition['Yes'], palette='Reds_r')
for i, p in enumerate(ax.patches):
    ax.annotate(f'{age_attrition["Yes"].iloc[i]:.1f}%', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=11)
plt.title('Attrition Rate by Age Group', fontsize=14, fontweight='bold')
plt.xlabel('Age Group')
plt.ylabel('Attrition Rate (%)')
plt.ylim(0, 40)
plt.tight_layout()
plt.show()


# Attrition by Gender
gender_attrition = df.groupby('Gender')['Attrition'].value_counts(normalize=True).unstack() * 100
gender_attrition['Yes'] = gender_attrition['Yes'].fillna(0)

print(f"\n ATTRITION BY GENDER:")
print(f"   Male Attrition Rate: {gender_attrition.loc['Male', 'Yes']:.2f}%")
print(f"   Female Attrition Rate: {gender_attrition.loc['Female', 'Yes']:.2f}%")

plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df, x='Gender', hue='Attrition', palette=['#2ecc71', '#e74c3c'])
plt.title('Attrition Distribution by Gender', fontsize=14, fontweight='bold')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='Attrition')
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.show()


# Attrition by Department
dept_attrition = df.groupby('Department')['Attrition'].value_counts(normalize=True).unstack() * 100
dept_attrition['Yes'] = dept_attrition['Yes'].fillna(0)
dept_attrition = dept_attrition.sort_values('Yes', ascending=False)

print(f"\n ATTRITION BY DEPARTMENT:")
for dept, rate in dept_attrition['Yes'].items():
    print(f"   • {dept}: {rate:.2f}%")

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=dept_attrition.index, y=dept_attrition['Yes'], palette='Reds_r')
for i, p in enumerate(ax.patches):
    ax.annotate(f'{dept_attrition["Yes"].iloc[i]:.1f}%', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=11)
plt.title('Attrition Rate by Department', fontsize=14, fontweight='bold')
plt.xlabel('Department')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.show()


# Attrition by Job Role
job_attrition = df.groupby('JobRole')['Attrition'].value_counts(normalize=True).unstack() * 100
job_attrition['Yes'] = job_attrition['Yes'].fillna(0)
job_attrition = job_attrition.sort_values('Yes', ascending=False)

print(f"\n ATTRITION BY JOB ROLE (Top 5):")
for role, rate in job_attrition['Yes'].head(5).items():
    print(f"   • {role}: {rate:.2f}%")

plt.figure(figsize=(12, 6))
top_roles = job_attrition.head(10)
ax = sns.barplot(x=top_roles.index, y=top_roles['Yes'], palette='Reds_r')
for i, p in enumerate(ax.patches):
    ax.annotate(f'{top_roles["Yes"].iloc[i]:.1f}%', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10)
plt.title('Attrition Rate by Job Role (Top 10)', fontsize=14, fontweight='bold')
plt.xlabel('Job Role')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


# IDENTIFY KEY FACTORS INFLUENCING TURNOVER
print(" IDENTIFY KEY FACTORS INFLUENCING TURNOVER")

# Monthly Income Analysis
income_stats = df.groupby('Attrition')['MonthlyIncome'].agg(['mean', 'median', 'std'])
print(f"\n MONTHLY INCOME ANALYSIS:")
print(f"   Statistics by Attrition Status:")
print(f"   {'Attrition':<12} {'Mean':<12} {'Median':<12} {'Std Dev':<12}")
print(f"   {'No':<12} ${income_stats.loc['No', 'mean']:>10,.0f} ${income_stats.loc['No', 'median']:>10,.0f} ${income_stats.loc['No', 'std']:>10,.0f}")
print(f"   {'Yes':<12} ${income_stats.loc['Yes', 'mean']:>10,.0f} ${income_stats.loc['Yes', 'median']:>10,.0f} ${income_stats.loc['Yes', 'std']:>10,.0f}")

# Job Satisfaction Analysis
satisfaction_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
df['JobSatisfactionLevel'] = df['JobSatisfaction'].map(satisfaction_map)

sat_attrition = df.groupby('JobSatisfactionLevel', observed=True)['Attrition'].value_counts(normalize=True).unstack() * 100
sat_attrition['Yes'] = sat_attrition['Yes'].fillna(0)

print(f"\n JOB SATISFACTION IMPACT:")
for level, rate in sat_attrition['Yes'].items():
    print(f"   • {level}: {rate:.2f}%")


# Work-Life Balance Analysis
wlb_map = {1: 'Bad', 2: 'Good', 3: 'Better', 4: 'Best'}
df['WorkLifeBalanceLevel'] = df['WorkLifeBalance'].map(wlb_map)

wlb_attrition = df.groupby('WorkLifeBalanceLevel', observed=True)['Attrition'].value_counts(normalize=True).unstack() * 100
wlb_attrition['Yes'] = wlb_attrition['Yes'].fillna(0)

print(f"\n WORK-LIFE BALANCE IMPACT:")
for level, rate in wlb_attrition['Yes'].items():
    print(f"   • {level}: {rate:.2f}%")

plt.figure(figsize=(10, 6))
ax = sns.barplot(x=wlb_attrition.index, y=wlb_attrition['Yes'], palette='Reds_r')
for i, p in enumerate(ax.patches):
    ax.annotate(f'{wlb_attrition["Yes"].iloc[i]:.1f}%', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=11)
plt.title('Attrition Rate by Work-Life Balance', fontsize=14, fontweight='bold')
plt.xlabel('Work-Life Balance Level')
plt.ylabel('Attrition Rate (%)')
plt.tight_layout()
plt.show()


# Overtime Impact
overtime_attrition = df.groupby('OverTime')['Attrition'].value_counts(normalize=True).unstack() * 100
overtime_attrition['Yes'] = overtime_attrition['Yes'].fillna(0)

print(f"\n OVERTIME IMPACT:")
print(f"   Employees with Overtime - Attrition Rate: {overtime_attrition.loc['Yes', 'Yes']:.2f}%")
print(f"   Employees without Overtime - Attrition Rate: {overtime_attrition.loc['No', 'Yes']:.2f}%")

plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df, x='OverTime', hue='Attrition', palette=['#2ecc71', '#e74c3c'])
plt.title('Attrition Distribution by Overtime Status', fontsize=14, fontweight='bold')
plt.xlabel('OverTime')
plt.ylabel('Count')
plt.legend(title='Attrition')
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', 
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.show()


# Environment Satisfaction
env_map = {1: 'Low', 2: 'Medium', 3: 'High', 4: 'Very High'}
df['EnvSatisfactionLevel'] = df['EnvironmentSatisfaction'].map(env_map)

env_attrition = df.groupby('EnvSatisfactionLevel', observed=True)['Attrition'].value_counts(normalize=True).unstack() * 100
env_attrition['Yes'] = env_attrition['Yes'].fillna(0)

print(f"\n ENVIRONMENT SATISFACTION IMPACT:")
for level, rate in env_attrition['Yes'].items():
    print(f"   • {level}: {rate:.2f}%")

# 5. CORRELATION ANALYSIS
print("CORRELATION ANALYSIS")

df_numeric = df.copy()
df_numeric['Attrition_Numeric'] = (df_numeric['Attrition'] == 'Yes').astype(int)

numeric_cols = ['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
                'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
                'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
                'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears',
                'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany',
                'YearsInCurrentRole', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
                'Attrition_Numeric']

correlation_matrix = df_numeric[numeric_cols].corr()
attrition_corr = correlation_matrix['Attrition_Numeric'].sort_values(ascending=False)

print(f"\n TOP FACTORS CORRELATED WITH ATTRITION:")
for factor, corr in attrition_corr.head(10).items():
    if factor != 'Attrition_Numeric':
        direction = "positive" if corr > 0 else "negative"
        print(f"   • {factor}: {corr:.4f} ({direction})")

plt.figure(figsize=(12, 8))
top_factors = attrition_corr[1:11]
colors = ['#e74c3c' if x > 0 else '#2ecc71' for x in top_factors.values]
plt.barh(range(len(top_factors)), top_factors.values, color=colors)
plt.yticks(range(len(top_factors)), top_factors.index)
plt.xlabel('Correlation with Attrition')
plt.title('Top 10 Factors Correlated with Employee Attrition', fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.show()

# 6. SUMMARY DASHBOARD
print("SUMMARY DASHBOARD - KEY ATTRITION INSIGHTS")

summary_data = {
    'Metric': [
        'Overall Attrition Rate', 'Highest Attrition Age Group', 'Highest Attrition Gender',
        'Highest Attrition Department', 'Highest Attrition Job Role', 
        'Lowest Average Monthly Income (Attrition)', 'Highest Overtime Impact',
        'Lowest Job Satisfaction Impact', 'Lowest Work-Life Balance Impact'
    ],
    'Value': [
        f"{attrition_percent['Yes']:.2f}%",
        age_attrition['Yes'].idxmax(),
        gender_attrition['Yes'].idxmax(),
        dept_attrition['Yes'].idxmax(),
        job_attrition['Yes'].idxmax(),
        f"${income_stats.loc['Yes', 'mean']:,.0f}",
        f"{overtime_attrition.loc['Yes', 'Yes']:.1f}% vs {overtime_attrition.loc['No', 'Yes']:.1f}%",
        f"{sat_attrition.loc['Low', 'Yes']:.1f}% (Low) vs {sat_attrition.loc['Very High', 'Yes']:.1f}% (Very High)",
        f"{wlb_attrition.loc['Bad', 'Yes']:.1f}% (Bad) vs {wlb_attrition.loc['Best', 'Yes']:.1f}% (Best)"
    ]
}

summary_df = pd.DataFrame(summary_data)
print("\n KEY METRICS SUMMARY:")
print(summary_df.to_string(index=False))

# 7. MACHINE LEARNING - DATA PREPARATION
print("MACHINE LEARNING - EMPLOYEE ATTRITION PREDICTION")

# Prepare features
df_ml = df.copy()

# Remove derived columns
derived_cols = ['AgeGroup', 'EducationLevel', 'JobSatisfactionLevel', 
                'WorkLifeBalanceLevel', 'EnvSatisfactionLevel']
df_ml = df_ml.drop(columns=[col for col in derived_cols if col in df_ml.columns])

# Encode categorical variables
categorical_cols = ['BusinessTravel', 'Department', 'EducationField', 'Gender', 
                    'JobRole', 'MaritalStatus', 'Over18', 'OverTime']

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df_ml[col] = le.fit_transform(df_ml[col])
    label_encoders[col] = le

# Encode target
le_target = LabelEncoder()
df_ml['Attrition'] = le_target.fit_transform(df_ml['Attrition'])

print(f"\n TARGET DISTRIBUTION:")
print(f"   0 (Stayed): {(df_ml['Attrition'] == 0).sum()}")
print(f"   1 (Left): {(df_ml['Attrition'] == 1).sum()}")

# Separate features and target
X = df_ml.drop(columns=['Attrition'])
y = df_ml['Attrition']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=42, stratify=y)

print(f"\n DATA SPLIT:")
print(f"   Training set size: {X_train.shape}")
print(f"   Test set size: {X_test.shape}")

# Scale numerical features
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()
X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

# FEATURE IMPORTANCE ANALYSIS
print("\n FEATURE IMPORTANCE ANALYSIS")

rf_temp = RandomForestClassifier(n_estimators=100, random_state=42)
rf_temp.fit(X_train, y_train)

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_temp.feature_importances_
}).sort_values('Importance', ascending=False)

print(f"\n TOP 15 MOST IMPORTANT FEATURES:")
for i, row in feature_importance.head(15).iterrows():
    print(f"   {row['Feature']:<25} {row['Importance']:.6f}")

plt.figure(figsize=(12, 8))
top_features = feature_importance.head(15)
colors = plt.cm.RdYlGn_r(top_features['Importance'].values / top_features['Importance'].max())
plt.barh(range(len(top_features)), top_features['Importance'].values, color=colors)
plt.yticks(range(len(top_features)), top_features['Feature'].values)
plt.xlabel('Feature Importance Score')
plt.title('Top 15 Features Predicting Employee Attrition', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# TRAIN MULTIPLE MODELS
print("\n MODEL TRAINING AND COMPARISON")

models = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=10),
    'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=100),
    'SVM': SVC(random_state=42, probability=True)
}

results = []

print(f"\n{'Model':<20} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'ROC-AUC':<12}")
print("-" * 80)

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
    
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC-AUC': roc_auc
    })
    
    print(f"{name:<20} {accuracy:.4f}     {precision:.4f}     {recall:.4f}     {f1:.4f}     {roc_auc:.4f}")


# 10. HYPERPARAMETER TUNING
print("\n HYPERPARAMETER TUNING FOR LOGISTIC REGRESSION")

param_grid = {
    'C': [0.1, 1, 10],
    'class_weight': ['balanced', None]
}

lr = LogisticRegression(random_state=42, max_iter=2000, solver='liblinear')
grid_search = GridSearchCV(estimator=lr, param_grid=param_grid, 
                          cv=5, scoring='precision', n_jobs=-1)
grid_search.fit(X_train, y_train)

print(f"\n   Best Parameters: {grid_search.best_params_}")
print(f"   Best CV Score: {grid_search.best_score_:.4f}")

best_lr = grid_search.best_estimator_
y_pred_best = best_lr.predict(X_test)
y_pred_proba_best = best_lr.predict_proba(X_test)[:, 1]

print(f"\n TUNED LOGISTIC REGRESSION PERFORMANCE:")
print(f"   Accuracy:  {accuracy_score(y_test, y_pred_best):.4f}")
print(f"   Precision: {precision_score(y_test, y_pred_best):.4f}")
print(f"   Recall:    {recall_score(y_test, y_pred_best):.4f}")
print(f"   F1-Score:  {f1_score(y_test, y_pred_best):.4f}")
print(f"   ROC-AUC:   {roc_auc_score(y_test, y_pred_proba_best):.4f}")



# 11. CONFUSION MATRIX

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Stayed', 'Left'], yticklabels=['Stayed', 'Left'])
axes[0].set_title(f'Confusion Matrix - Logistic Regression', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

cm_percent = cm.astype('float') / cm.sum() * 100
sns.heatmap(cm_percent, annot=True, fmt='.1f', cmap='Greens', ax=axes[1],
            xticklabels=['Stayed', 'Left'], yticklabels=['Stayed', 'Left'])
axes[1].set_title(f'Confusion Matrix (%) - Logistic Regression', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

plt.tight_layout()
plt.show()

print(f"\n CONFUSION MATRIX INTERPRETATION:")
print(f"   True Negatives (Correctly predicted Stayed): {cm[0,0]} ({cm_percent[0,0]:.1f}%)")
print(f"   True Positives (Correctly predicted Left): {cm[1,1]} ({cm_percent[1,1]:.1f}%)")
print(f"   False Positives (Wrongly predicted Left): {cm[0,1]} ({cm_percent[0,1]:.1f}%)")
print(f"   False Negatives (Wrongly predicted Stayed): {cm[1,0]} ({cm_percent[1,0]:.1f}%)")


# 12. ROC CURVES COMPARISON

plt.figure(figsize=(10, 8))

colors = ['blue', 'green', 'red', 'orange', 'purple']
for (name, model), color in zip(models.items(), colors):
    if hasattr(model, 'predict_proba'):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        plt.plot(fpr, tpr, color=color, lw=2, label=f'{name} (AUC = {roc_auc:.3f})')

plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--', label='Random Classifier')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
plt.legend(loc='lower right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()



# 13. SAMPLE PREDICTIONS

print("MAKING PREDICTIONS ON SAMPLE EMPLOYEES")

feature_names = X.columns.tolist()

sample_employees = pd.DataFrame([
    {  # High risk employee
        'Age': 28, 'BusinessTravel': 2, 'DailyRate': 500, 'Department': 1,
        'DistanceFromHome': 20, 'Education': 2, 'EducationField': 1,
        'EmployeeCount': 1, 'EmployeeNumber': 9999, 'EnvironmentSatisfaction': 1,
        'Gender': 1, 'HourlyRate': 50, 'JobInvolvement': 1, 'JobLevel': 1,
        'JobRole': 5, 'JobSatisfaction': 1, 'MaritalStatus': 1,
        'MonthlyIncome': 3000, 'MonthlyRate': 10000, 'NumCompaniesWorked': 5,
        'Over18': 1, 'OverTime': 1, 'PercentSalaryHike': 10,
        'PerformanceRating': 3, 'RelationshipSatisfaction': 2,
        'StandardHours': 80, 'StockOptionLevel': 0, 'TotalWorkingYears': 5,
        'TrainingTimesLastYear': 2, 'WorkLifeBalance': 1,
        'YearsAtCompany': 1, 'YearsInCurrentRole': 1,
        'YearsSinceLastPromotion': 0, 'YearsWithCurrManager': 1
    },
    {  # Low risk employee
        'Age': 45, 'BusinessTravel': 0, 'DailyRate': 800, 'Department': 0,
        'DistanceFromHome': 5, 'Education': 4, 'EducationField': 2,
        'EmployeeCount': 1, 'EmployeeNumber': 9998, 'EnvironmentSatisfaction': 4,
        'Gender': 0, 'HourlyRate': 80, 'JobInvolvement': 4, 'JobLevel': 3,
        'JobRole': 1, 'JobSatisfaction': 4, 'MaritalStatus': 2,
        'MonthlyIncome': 12000, 'MonthlyRate': 15000, 'NumCompaniesWorked': 1,
        'Over18': 1, 'OverTime': 0, 'PercentSalaryHike': 20,
        'PerformanceRating': 4, 'RelationshipSatisfaction': 4,
        'StandardHours': 80, 'StockOptionLevel': 2, 'TotalWorkingYears': 15,
        'TrainingTimesLastYear': 4, 'WorkLifeBalance': 3,
        'YearsAtCompany': 10, 'YearsInCurrentRole': 5,
        'YearsSinceLastPromotion': 3, 'YearsWithCurrManager': 5
    }
])

for col in feature_names:
    if col not in sample_employees.columns:
        sample_employees[col] = 0

sample_employees = sample_employees[feature_names]
predictions_sample = best_lr.predict(sample_employees)
probabilities = best_lr.predict_proba(sample_employees)

print(f"\n SAMPLE EMPLOYEE PREDICTIONS (Logistic Regression - Best Model):")

for i in range(len(sample_employees)):
    risk = "HIGH RISK" if predictions_sample[i] == 1 else "LOW RISK"
    prob_left = probabilities[i][1] * 100
    prob_stay = probabilities[i][0] * 100
    print(f"\n   Employee {i+1}:")
    print(f"      Age: {sample_employees.iloc[i]['Age']}")
    print(f"      Monthly Income: ${sample_employees.iloc[i]['MonthlyIncome']:,}")
    print(f"      Overtime: {'Yes' if sample_employees.iloc[i]['OverTime'] == 1 else 'No'}")
    print(f"      Prediction: {risk}")
    print(f"      Probability of Leaving: {prob_left:.1f}%")
    print(f"      Probability of Staying: {prob_stay:.1f}%")
    
    if predictions_sample[i] == 1:
        print(f"      Recommended Action: Schedule retention interview, review compensation and work-life balance")
    else:
        print(f"      Recommended Action: Continue monitoring, good retention candidate")

# 14. FINAL RECOMMENDATIONS

print("FINAL RECOMMENDATIONS")

# Find best model by Precision (Business Value)
best_model_name = results_df.loc[results_df['Precision'].idxmax(), 'Model']
best_precision_score = results_df.loc[results_df['Precision'].idxmax(), 'Precision']
best_accuracy_score = results_df.loc[results_df['Precision'].idxmax(), 'Accuracy']

print(f"\n BEST MODEL FOR BUSINESS: {best_model_name}")
print(f"   Precision: {best_precision_score:.4f} ({best_precision_score*100:.2f}%)")
print(f"   Accuracy: {best_accuracy_score:.4f} ({best_accuracy_score*100:.2f}%)")
print(f"\n   Why: Highest precision means when the model predicts an employee will leave,")
print(f"        you can trust it {best_precision_score*100:.1f}% of the time.")
print(f"\n   This model should be used to identify employees at risk of attrition")
print(f"   for proactive retention strategies.")

