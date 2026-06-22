# FoodHub Business Intelligence & Predictive Analytics Engine

## 📊 Project Overview

This project is a complete **business intelligence and predictive analytics solution for FoodHub**. It combines data cleaning, exploratory analysis, and interactive dashboard visualizations to uncover operational trends in delivery, cuisine demand, restaurant performance, and customer satisfaction.

This project delivers four business-driven analytics paths using the FoodHub dataset:

1. Delivery Time Optimization: predict order fulfillment and ETA using regression.
2. Personalized Cuisine Recommendation: recommend cuisine types using classification.
3. Customer Segmentation / Revenue Strategy: group customers for targeted offers using clustering.
4. Restaurant Quality Control: flag risky restaurants using binary classification.

## 🎯 Objectives

- Analyze FoodHub order and delivery performance using historical transaction data
- Visualize customer trends, cuisine preferences, restaurant impact, and rating distribution
- Support business decisions with interactive dashboards and summary metrics
- Enable data-driven insights for operations, marketing, and partner evaluation

## 📈 Visualizations Included

### 1. **Bar Chart** - Orders by Day of Week
   - Reveals weekly demand patterns
   - Highlights peak delivery days and slow periods
   - Supports planning for staffing and promotions

### 2. **Bar Chart** - Delivery Distance Distribution
   - Shows order volume by delivery range
   - Identifies operational reach and fulfillment trends
   - Helps optimize delivery zones

### 3. **Pie Chart** - Top Cuisine Types
   - Displays share of popular cuisines
   - Highlights dominant food categories
   - Guides menu and marketing focus

### 4. **Bar Chart** - Top Restaurants by Orders
   - Compares restaurant performance by order count
   - Identifies high-impact partners
   - Supports restaurant quality and growth analysis

## 📋 Features

- ✅ Interactive Streamlit dashboard for fast business review
- ✅ Trend analysis for orders, distance, cuisine, and ratings
- ✅ Clean dataset loading and preprocessing from `foodhub_data.csv`
- ✅ Aggregated KPIs for orders, ratings, fulfillment, and cuisine popularity
- ✅ Support for filters like city, order status, and restaurant selection

## 🛠️ Technologies Used

- **Python 3.x**
- **Pandas** - data loading and transformation
- **NumPy** - numeric processing
- **Plotly Express** - interactive charts
- **Streamlit** - dashboard presentation
- **Scikit-learn** - predictive analytics support in notebook workflows

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/himanshuverma7019official-create/FoodHub-BI-Predictive-Analytics-Engine.git

# Navigate to the project folder
cd "FoodHub Business Intelligence & Predictive Analytics Engine"

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

Run the dashboard script:

```bash
streamlit run dashboard.py
```

Or open the analysis notebook:

```bash
jupyter lab FoodHub_Business_Intelligence.ipynb
```

## 📊 Data Structure

The project works with:
- **CSV dataset** from `foodhub_data.csv`
- **Pandas DataFrame** for feature engineering and aggregation
- **NumPy arrays** via data conversion and numeric metrics
- **Plotly Express visuals** for charts and dashboard plots
- **Streamlit widgets** for filters and interactive exploration

## 📝 Key Insights

- Weekly order demand is visible by day of week
- Delivery distance clusters show customer reach
- Top cuisines drive the majority of orders
- Restaurant order counts reveal best-performing partners
- Ratings help surface customer satisfaction trends

## 👤 Author

**Himanshu Verma**  
GitHub: [@himanshuverma7019official-create](https://github.com/himanshuverma7019official-create)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for improvements.

## 📬 Contact

For questions or suggestions, please open an issue on GitHub.
