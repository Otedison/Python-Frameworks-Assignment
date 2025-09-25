# part3_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import collections
import numpy as np

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")

print("=== PART 3: DATA ANALYSIS AND VISUALIZATION ===\n")

# Load cleaned data
df_clean = pd.read_csv('data/cleaned_metadata.csv')
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'])

print("1. Performing basic analysis...")

# 1. Basic analysis
# Count papers by publication year
yearly_counts = df_clean['year'].value_counts().sort_index()
print("\nPublications by year:")
for year, count in yearly_counts.items():
    if pd.notna(year):
        print(f"  {int(year)}: {count:,} papers")

# Identify top journals
top_journals = df_clean['journal'].value_counts().head(10)
print("\nTop 10 journals:")
for journal, count in top_journals.items():
    print(f"  {journal}: {count:,} papers")

# Most frequent words in titles
print("\nAnalyzing frequent words in titles...")
all_titles = ' '.join(df_clean['title'].dropna().astype(str))
words = all_titles.lower().split()
# Remove common stop words
stop_words = {'the', 'and', 'of', 'in', 'to', 'a', 'for', 'with', 'on', 'by', 
              'as', 'an', 'from', 'at', 'that', 'is', 'are', 'this', 'was', 'were'}
filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
word_freq = collections.Counter(filtered_words).most_common(20)

print("Top 20 words in titles:")
for word, count in word_freq:
    print(f"  {word}: {count}")

# 2. Create visualizations
print("\n2. Creating visualizations...")

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('CORD-19 Dataset Analysis', fontsize=16, fontweight='bold')

# Plot 1: Publications over time
ax1 = axes[0, 0]
yearly_counts = df_clean['year'].value_counts().sort_index()
ax1.bar(yearly_counts.index, yearly_counts.values, color='skyblue', edgecolor='black')
ax1.set_title('Number of Publications per Year')
ax1.set_xlabel('Year')
ax1.set_ylabel('Number of Papers')
ax1.tick_params(axis='x', rotation=45)

# Plot 2: Top publishing journals
ax2 = axes[0, 1]
top_journals = df_clean['journal'].value_counts().head(10)
ax2.barh(range(len(top_journals)), top_journals.values)
ax2.set_yticks(range(len(top_journals)))
ax2.set_yticklabels(top_journals.index)
ax2.set_title('Top 10 Journals by Publication Count')
ax2.set_xlabel('Number of Papers')

# Plot 3: Distribution by source
ax3 = axes[1, 0]
source_counts = df_clean['source_x'].value_counts().head(8)
ax3.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%')
ax3.set_title('Paper Distribution by Source (Top 8)')

# Plot 4: Abstract word count distribution
ax4 = axes[1, 1]
abstract_lengths = df_clean['abstract_word_count']
ax4.hist(abstract_lengths[abstract_lengths < 500], bins=50, alpha=0.7, edgecolor='black')
ax4.set_title('Distribution of Abstract Word Counts')
ax4.set_xlabel('Word Count')
ax4.set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('visualizations/basic_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. Word cloud of paper titles
print("\n3. Generating word cloud...")
plt.figure(figsize=(12, 8))
wordcloud = WordCloud(width=800, height=400, background_color='white', 
                      max_words=100, colormap='viridis').generate(all_titles)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles', fontsize=16, pad=20)
plt.tight_layout()
plt.savefig('visualizations/wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()

# 4. Additional analysis - Monthly trends for recent years
print("\n4. Additional analysis - Monthly trends...")
recent_data = df_clean[df_clean['year'] >= 2019].copy()
recent_data['month'] = recent_data['publish_time'].dt.to_period('M')
monthly_trend = recent_data['month'].astype(str).value_counts().sort_index()

plt.figure(figsize=(12, 6))
plt.plot(monthly_trend.index, monthly_trend.values, marker='o', linewidth=2, markersize=4)
plt.title('Monthly Publication Trend (2019-2023)')
plt.xlabel('Month')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/monthly_trend.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n5. Summary Statistics:")
print(f"Total papers analyzed: {len(df_clean):,}")
print(f"Time period: {df_clean['year'].min()} - {df_clean['year'].max()}")
print(f"Average abstract length: {df_clean['abstract_word_count'].mean():.1f} words")
print(f"Unique journals: {df_clean['journal'].nunique():,}")

print("\n✅ Part 3 completed successfully!")
print("📊 Visualizations saved to 'visualizations/' folder")