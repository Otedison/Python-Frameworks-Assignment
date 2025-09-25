# part2_cleaning.py
import pandas as pd
import numpy as np
from part1_exploration import df  # Import from previous part

print("=== PART 2: DATA CLEANING AND PREPARATION ===\n")

# Create a copy for cleaning
df_clean = df.copy()

print("1. Original dataset shape:", df_clean.shape)

# 1. Handle missing data
print("\n2. Handling missing values...")

# Strategy for each column
missing_strategy = {
    'title': 'drop',  # Papers without titles are not useful
    'abstract': 'fill',  # Fill with placeholder text
    'publish_time': 'keep',  # We'll handle dates separately
    'authors': 'fill',  # Fill with 'Unknown'
    'journal': 'fill',  # Fill with 'Unknown Journal'
    'source_x': 'keep'  # Keep as is
}

# Apply strategies
rows_before = len(df_clean)

# Drop rows without titles
df_clean = df_clean[df_clean['title'].notna()]
print(f"Removed {rows_before - len(df_clean)} rows without titles")

# Fill missing abstracts
df_clean['abstract'] = df_clean['abstract'].fillna('No abstract available')

# Fill missing authors and journals
df_clean['authors'] = df_clean['authors'].fillna('Unknown authors')
df_clean['journal'] = df_clean['journal'].fillna('Unknown Journal')

print("3. Missing values after cleaning:")
important_columns = ['title', 'abstract', 'publish_time', 'authors', 'journal']
print(df_clean[important_columns].isnull().sum())

# 2. Prepare data for analysis
print("\n4. Preparing data for analysis...")

# Convert publish_time to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract year from publication date
df_clean['year'] = df_clean['publish_time'].dt.year

# Create abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].str.split().str.len()
df_clean['abstract_word_count'] = df_clean['abstract_word_count'].fillna(0)

# Create title word count
df_clean['title_word_count'] = df_clean['title'].str.split().str.len()

# Create a paper ID if not exists
if 'paper_id' not in df_clean.columns:
    df_clean['paper_id'] = range(1, len(df_clean) + 1)

print("5. New columns created:")
new_columns = ['year', 'abstract_word_count', 'title_word_count', 'paper_id']
print(df_clean[new_columns].head())

print("\n6. Data types after cleaning:")
print(df_clean[['publish_time', 'year', 'abstract_word_count']].dtypes)

print("\n7. Dataset shape after cleaning:", df_clean.shape)

# Save cleaned dataset
df_clean.to_csv('data/cleaned_metadata.csv', index=False)
print("✅ Cleaned dataset saved to 'data/cleaned_metadata.csv'")

print("\n✅ Part 2 completed successfully!")