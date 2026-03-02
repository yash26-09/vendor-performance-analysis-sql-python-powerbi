# 🧾 Vendor Performance Analysis – Retail Inventory & Sales Optimization

## 🔹 Brief One-Line Summary

End-to-end retail analytics project analyzing vendor efficiency, pricing strategy, and inventory performance using SQL, Python, and Power BI.

---

## 📖 Overview

This project evaluates vendor performance and retail inventory dynamics to support strategic purchasing and profitability optimization.

A complete analytics pipeline was built:

- SQL for data ingestion and transformation  
- Python for exploratory analysis and statistical testing  
- Power BI for interactive executive dashboard reporting  

The goal is to simulate a real-world retail analytics case study.

---

## 🎯 Problem Statement

Retail businesses often face:

- Vendor dependency risks  
- Slow-moving inventory  
- Inefficient pricing strategies  
- Profitability imbalance across vendors  

This project aims to:

- Identify underperforming brands needing pricing or promotional adjustments  
- Determine top vendors contributing to revenue  
- Analyze bulk purchasing cost efficiency  
- Assess inventory turnover and unsold capital  
- Statistically validate differences in vendor profitability  

---

## 📂 Dataset

The dataset consists of multiple structured CSV files including:

- Sales transactions  
- Vendor details  
- Inventory data  
- Purchase & pricing information  

A vendor-level summary table was generated containing:

- Total Sales Dollars  
- Total Purchase Dollars  
- Gross Profit  
- Profit Margin  
- Stock Turnover  
- Sales-to-Purchase Ratio  
- Freight Cost  
- Unsold Capital  

---

## 🛠 Tools and Technologies

- SQL (Joins, Aggregations, CTEs)  
- Python  
  - Pandas  
  - Matplotlib  
  - Seaborn  
  - SciPy (Hypothesis Testing)  
- Power BI  
- Git & GitHub  

---

## 🔬 Methods

1. Data Cleaning  
   - Removed negative or zero-profit transactions  
   - Filtered zero sales quantity  
   - Handled missing values  

2. Feature Engineering  
   - Calculated profit margin %  
   - Created stock turnover metric  
   - Computed sales-to-purchase ratio  

3. Exploratory Data Analysis  
   - Distribution analysis  
   - Outlier detection  
   - Correlation heatmap  

4. Statistical Testing  
   - Hypothesis testing between high-performing and low-performing vendors  

5. Dashboard Development  
   - KPI Cards  
   - Vendor contribution donut chart  
   - Sales vs Profit scatter analysis  
   - Low-performing vendor identification  

---

## 📊 Key Insights

- Top 10 vendors contribute ~65% of total purchases → high dependency risk  
- 198 brands identified with low sales but high profit margins → promotional opportunity  
- $2.7M unsold inventory detected → holding cost risk  
- Strong correlation between purchase quantity and sales quantity (~0.99)  
- Low-performing vendors maintain higher margins (~41%) but lower sales volume  

Hypothesis testing confirmed statistically significant margin differences between vendor groups.

---

## 📈 Dashboard / Output

The Power BI dashboard includes:

- Total Sales, Purchase, Gross Profit, Profit Margin KPIs  
- Vendor contribution analysis  
- Top vendors and brands by sales  
- Low-performing vendor scatter plot  
- Inventory turnover insights  

Dashboard File:
dashboard/vendor_performance_dashboard.pbix

---

## ▶ How to Run This Project

1. Clone Repository:

git clone https://github.com/yourusername/vendor-performance-analysis.git

2. Install Dependencies:

pip install -r requirements.txt

3. Run Data Ingestion:

python scripts/ingestion_db.py

4. Generate Vendor Summary:

python scripts/get_vendor_summary.py

5. Run Notebooks:

jupyter notebook

Run:
- notebooks/exploratory_data_analysis.ipynb  
- notebooks/vendor_performance_analysis.ipynb  

6. Open Dashboard:

dashboard/vendor_performance_dashboard.pbix

---

## 🏁 Results & Conclusion

This project demonstrates how structured vendor performance analysis can:

- Improve pricing strategies  
- Reduce inventory holding costs  
- Identify vendor concentration risks  
- Support data-driven procurement decisions  

Strategic vendor diversification and targeted promotions can significantly improve overall profitability.

---

## 🚀 Future Work

- Build predictive model for vendor profitability  
- Implement automated inventory forecasting  
- Deploy dashboard to Power BI Service  
- Integrate real-time database pipeline  

---

## 👨‍💻 Author & Contact

Parth [Yash Khairnar]  
Aspiring Data Analyst | SQL • Python • Power BI  

Email: ym71062@gmail.com  
LinkedIn: www.linkedin.com/in/yashk2609
