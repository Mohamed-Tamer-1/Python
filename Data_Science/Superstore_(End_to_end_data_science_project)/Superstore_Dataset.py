import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"D:\Projecrs\vs_code\Python\Data_Science\End_to_end_data_science_project_part_1_analysis\Superstore.csv", encoding='windows-1252')
df_copy = df.copy()
# df_copy.head()
# df_copy.info()
# df_copy.describe()
# Assuming 'Order Date' and 'Ship Date' are columns in df_copy
df_copy['Order Date'] = pd.to_datetime(df_copy['Order Date'], format='%m/%d/%Y', dayfirst=False, errors='coerce')
df_copy['Ship Date'] = pd.to_datetime(df_copy['Ship Date'], format='%m/%d/%Y', dayfirst=False, errors='coerce')
df_copy['Sales Before Discount'] = df_copy['Sales'] / (1 - df_copy['Discount'])
df_copy['Price'] = df_copy.groupby('Product Name')['Sales Before Discount'].transform('sum') / df_copy.groupby('Product Name')['Quantity'].transform('sum')
df_copy['Price After Discount'] = round(df_copy['Price'] * (1 - df_copy['Discount']),2)
df_copy['Profit Margin'] = df_copy['Profit'] / df_copy['Sales']


def top_grouped_sales():
    return{
        "product": df_copy.groupby('Product Name')['Sales'].sum().sort_values(ascending=False),
        "category": df_copy.groupby('Category')['Sales'].sum().sort_values(ascending=False),
        "state": df_copy.groupby('State')['Sales'].sum().sort_values(ascending=False),
        "city": df_copy.groupby('City')['Sales'].sum().sort_values(ascending=False),
        "region": df_copy.groupby('Region')['Sales'].sum().sort_values(ascending=False),
        "discount": df.groupby('Discount')['Sales'].sum(),
 
    }
    
def top_grouped_profit():
    return{
        "product": df_copy.groupby('Product Name')['Profit'].sum().sort_values(ascending=False),
        "category": df_copy.groupby('Category')['Profit'].sum().sort_values(ascending=False),
        "state": df_copy.groupby('State')['Profit'].sum().sort_values(ascending=False),
        "city": df_copy.groupby('City')['Profit'].sum().sort_values(ascending=False),
        "region": df_copy.groupby('Region')['Profit'].sum().sort_values(ascending=False),
        "discount": df.groupby('Discount')['Profit'].sum(),
 
    }
    
def date_sales():
    return{
        "monthly": df_copy.groupby("Order Date")["Sales"].sum().resample("ME").sum(),
        "yearly": df_copy.groupby("Order Date")["Sales"].sum().resample("YE").sum(),
        "quarterly": df_copy.groupby("Order Date")["Sales"].sum().resample("QE").sum(),
    }
    
def date_profit():
    return{
        "monthly": df_copy.groupby("Order Date")["Profit"].sum().resample("ME").sum(),
        "yearly": df_copy.groupby("Order Date")["Profit"].sum().resample("YE").sum(),
        "quarterly": df_copy.groupby("Order Date")["Profit"].sum().resample("QE").sum(),
    }
    
def pivot_table():
    return{
        "segment" : df_copy.pivot_table(index='Segment' ,columns='Ship Mode', values='Sales', aggfunc='sum'),
        "product" : df_copy.pivot_table(index='Product Name', values=['Quantity', 'Sales', 'Profit'], aggfunc='sum').sort_values(by='Quantity', ascending=False),

    }
        
top_category_quantity = df_copy.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
avg_profit_margin_by_category = df_copy.groupby('Category')['Profit Margin'].mean()

def save_plot(data, kind, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10, 6))
    if kind == 'bar':
        data.plot(kind=kind, title=title)
    elif kind == 'line':
        data.plot(kind=kind, color='r', title=title)
    elif kind == 'barh':
        data.plot(kind=kind, color='green', title=title)
    else:
        raise ValueError("Unsupported plot type.")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
    # 1. Top 10 Products by Sales
save_plot(top_grouped_sales()["product"].head(10), 'barh', 'Top 10 Products by Sales', 'Sales', 'Products', 'top_10_products.png')

# 2. Top 10 States by Profit
save_plot(top_grouped_profit()["state"].head(10), 'barh', 'Top 10 States by Profit', 'Profit', 'States', 'top_10_states.png')

# 3. Sales by Category
save_plot(top_grouped_sales()["category"], 'bar', 'Sales by Category', 'Category', 'Sales', 'sales_by_category.png')

# 4. Average Profit Margin by Category
save_plot(avg_profit_margin_by_category, 'bar', 'Average Profit Margin by Category', 'Category', 'Profit Margin', 'avg_profit_margin_by_category.png')

# 5. Yearly Sales Trend
save_plot(date_sales()["yearly"], 'line', 'Yearly Sales Trend', 'Year', 'Sales', 'yearly_sales_trend.png')

# 6. Profit by Discount
save_plot(top_grouped_profit()["discount"], 'bar', 'Profit by Discount', 'Discount', 'Profit', 'profit_by_discount.png')

# 7. Highest Demand Category
save_plot(top_category_quantity, 'bar', 'Highest Demand Category', 'Category', 'Quantity', 'highest_demand_category.png')
