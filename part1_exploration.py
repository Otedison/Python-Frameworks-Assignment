# part1_exploration.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("=== PART 1: DATA LOADING AND BASIC EXPLORATION ===\n")

# 1. Download and load the data
print("1. Loading the dataset...")
try:
    df = pd.read_csv('data/metadata.csv')
    print("✅ Dataset loaded successfully!")
except FileNotFoundError:
    print("❌ File not found. Please download metadata.csv from Kaggle and place in data/ folder")
    exit()

# 2. Examine the first few rows and data structure
print("\n2. First few rows of the dataset:")
print(df.head())

print("\n3. Dataset columns:")
print(df.columns.tolist())

# 3. Basic data exploration
print("\n4. DataFrame dimensions:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\n5. Data types of each column:")
print(df.dtypes)

print("\n6. Checking for missing values in important columns:")
important_columns = ['title', 'abstract', 'publish_time', 'authors', 'journal', 'source_x']
missing_data = df[important_columns].isnull().sum()
missing_percent = (missing_data / len(df)) * 100

missing_df = pd.DataFrame({
    'Missing Count': missing_data,
    'Missing Percentage': missing_percent
})
print(missing_df)

print("\n7. Basic statistics for numerical columns:")
# Identify numerical columns
numerical_cols = df.select_dtypes(include=[np.number]).columns
if len(numerical_cols) > 0:
    print(df[numerical_cols].describe())
else:
    print("No numerical columns found in the dataset")

print("\n8. Sample of paper titles:")
print(df['title'].head(10).tolist())

# Save basic info for later use
basic_info = {
    'shape': df.shape,
    'columns': df.columns.tolist(),
    'missing_data': missing_df
}

print("\n✅ Part 1 completed successfully!")