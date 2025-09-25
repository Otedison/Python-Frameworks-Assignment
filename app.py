# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import io

# Page configuration
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .section-header {
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin: 2rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned dataset"""
    try:
        df = pd.read_csv('data/cleaned_metadata.csv')
        df['publish_time'] = pd.to_datetime(df['publish_time'])
        return df
    except FileNotFoundError:
        st.error("Cleaned dataset not found. Please run the data cleaning script first.")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🔬 CORD-19 Data Explorer</h1>', unsafe_allow_html=True)
    st.write("Simple exploration of COVID-19 research papers")
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.title("Navigation")
    section = st.sidebar.radio(
        "Go to:",
        ["📊 Dashboard Overview", "📈 Publication Trends", "🏆 Journal Analysis", 
         "🔍 Paper Explorer", "📋 Data Summary"]
    )
    
    # Dashboard Overview
    if section == "📊 Dashboard Overview":
        show_dashboard(df)
    
    # Publication Trends
    elif section == "📈 Publication Trends":
        show_publication_trends(df)
    
    # Journal Analysis
    elif section == "🏆 Journal Analysis":
        show_journal_analysis(df)
    
    # Paper Explorer
    elif section == "🔍 Paper Explorer":
        show_paper_explorer(df)
    
    # Data Summary
    elif section == "📋 Data Summary":
        show_data_summary(df)

def show_dashboard(df):
    """Dashboard with overview metrics"""
    st.markdown('<h2 class="section-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Papers", f"{len(df):,}")
    
    with col2:
        st.metric("Time Span", f"{int(df['year'].min())}-{int(df['year'].max())}")
    
    with col3:
        st.metric("Unique Journals", f"{df['journal'].nunique():,}")
    
    with col4:
        avg_abstract = df['abstract_word_count'].mean()
        st.metric("Avg Abstract Words", f"{avg_abstract:.0f}")
    
    st.write("---")
    
    # Quick charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Publications by Year")
        yearly_counts = df['year'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        yearly_counts.plot(kind='bar', ax=ax, color='lightblue', edgecolor='black')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Papers')
        plt.xticks(rotation=45)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Top 10 Journals")
        top_journals = df['journal'].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(top_journals.values, labels=top_journals.index, autopct='%1.1f%%')
        st.pyplot(fig)
    
    # Recent publications sample
    st.subheader("Recent Publications Sample")
    recent_papers = df.nlargest(5, 'publish_time')[['title', 'journal', 'publish_time']]
    st.dataframe(recent_papers)

def show_publication_trends(df):
    """Publication trends analysis"""
    st.markdown('<h2 class="section-header">📈 Publication Trends</h2>', unsafe_allow_html=True)
    
    # Year range selector
    min_year, max_year = int(df['year'].min()), int(df['year'].max())
    year_range = st.slider(
        "Select year range:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Filter data
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Yearly Publication Trend")
        yearly_counts = filtered_df['year'].value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(10, 6))
        yearly_counts.plot(kind='line', marker='o', ax=ax, linewidth=2)
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Papers')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Abstract Length Distribution")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(filtered_df['abstract_word_count'], bins=50, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Word Count')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)
    
    # Word cloud
    st.subheader("Word Cloud of Paper Titles")
    if st.checkbox("Generate Word Cloud"):
        all_titles = ' '.join(filtered_df['title'].dropna().astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

def show_journal_analysis(df):
    """Journal-specific analysis"""
    st.markdown('<h2 class="section-header">🏆 Journal Analysis</h2>', unsafe_allow_html=True)
    
    # Top journals selector
    top_n = st.slider("Number of top journals to show:", 5, 20, 10)
    top_journals = df['journal'].value_counts().head(top_n)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top {top_n} Journals")
        fig, ax = plt.subplots(figsize=(10, 8))
        top_journals.plot(kind='barh', ax=ax)
        ax.set_xlabel('Number of Papers')
        st.pyplot(fig)
    
    with col2:
        st.subheader("Journal Distribution")
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.pie(top_journals.values, labels=top_journals.index, autopct='%1.1f%%')
        st.pyplot(fig)
    
    # Journal details
    selected_journal = st.selectbox("Select a journal for details:", top_journals.index)
    journal_papers = df[df['journal'] == selected_journal]
    
    st.subheader(f"Details for {selected_journal}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Papers", len(journal_papers))
    
    with col2:
        st.metric("Years Active", 
                 f"{int(journal_papers['year'].min())}-{int(journal_papers['year'].max())}")
    
    with col3:
        avg_words = journal_papers['abstract_word_count'].mean()
        st.metric("Avg Abstract Words", f"{avg_words:.0f}")
    
    # Sample papers from selected journal
    st.subheader("Sample Papers")
    sample_papers = journal_papers[['title', 'publish_time', 'authors']].head(5)
    st.dataframe(sample_papers)

def show_paper_explorer(df):
    """Interactive paper explorer"""
    st.markdown('<h2 class="section-header">🔍 Paper Explorer</h2>', unsafe_allow_html=True)
    
    # Search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("Search in titles and abstracts:")
    
    with col2:
        year_filter = st.selectbox("Filter by year:", 
                                 ['All'] + sorted(df['year'].unique(), reverse=True))
    
    with col3:
        journal_filter = st.selectbox("Filter by journal:", 
                                    ['All'] + df['journal'].value_counts().head(20).index.tolist())
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (filtered_df['title'].str.contains(search_term, case=False, na=False) | 
                filtered_df['abstract'].str.contains(search_term, case=False, na=False))
        filtered_df = filtered_df[mask]
    
    if year_filter != 'All':
        filtered_df = filtered_df[filtered_df['year'] == year_filter]
    
    if journal_filter != 'All':
        filtered_df = filtered_df[filtered_df['journal'] == journal_filter]
    
    st.write(f"**Found {len(filtered_df):,} papers matching your criteria**")
    
    # Results display
    if len(filtered_df) > 0:
        papers_per_page = st.slider("Papers per page:", 5, 50, 10)
        
        # Pagination
        total_pages = (len(filtered_df) // papers_per_page) + 1
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * papers_per_page
        end_idx = start_idx + papers_per_page
        
        for idx, (_, paper) in enumerate(filtered_df.iloc[start_idx:end_idx].iterrows()):
            with st.expander(f"{paper['title']}"):
                st.write(f"**Journal:** {paper['journal']}")
                st.write(f"**Published:** {paper['publish_time'].strftime('%Y-%m-%d')}")
                st.write(f"**Authors:** {paper['authors'][:200]}...")
                st.write(f"**Abstract:** {paper['abstract'][:500]}...")
    else:
        st.info("No papers found matching your criteria.")

def show_data_summary(df):
    """Data summary and statistics"""
    st.markdown('<h2 class="section-header">📋 Data Summary</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Information")
        st.write(f"**Shape:** {df.shape[0]:,} rows × {df.shape[1]} columns")
        st.write(f"**Time period:** {df['publish_time'].min().strftime('%Y-%m-%d')} to {df['publish_time'].max().strftime('%Y-%m-%d')}")
        st.write(f"**Unique journals:** {df['journal'].nunique():,}")
        
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Non-Null': df.notnull().sum(),
            'Null': df.isnull().sum(),
            'Data Type': df.dtypes
        })
        st.dataframe(col_info)
    
    with col2:
        st.subheader("Sample Data")
        st.dataframe(df.head(10))
        
        st.subheader("Basic Statistics")
        st.write("Abstract word count:")
        st.write(df['abstract_word_count'].describe())
        
        # Download cleaned data
        st.subheader("Download Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download cleaned data as CSV",
            data=csv,
            file_name="cord19_cleaned.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()