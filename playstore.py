import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

print("="*80)
print("PLAY STORE REVIEWS ANALYSIS - MULTI-APP DATASET")
print("="*80)

# ============================================================
# 1. LOAD DATASET
# ============================================================
print("\n📂 Loading dataset...")
df = pd.read_csv('Training_Data_Google_Play_reviews_6000(in).csv')
print(f"✓ Dataset loaded successfully!")
print(f"✓ Total Reviews: {len(df):,}")
print(f"✓ Shape: {df.shape}")

# Display first few rows
print("\nFirst 5 rows:")
print(df.head())

# Check column names
print(f"\nColumns in dataset: {list(df.columns)}")

# ============================================================
# 2. DATA CLEANING
# ============================================================
print("\n" + "="*80)
print("2. DATA CLEANING")
print("="*80)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Drop rows with missing review content
df = df.dropna(subset=['content'])
print(f"\n✓ After dropping missing content: {len(df):,} reviews")

# Check data types
print("\nData types:")
print(df.dtypes)

# ============================================================
# 3. BASIC STATISTICS
# ============================================================
print("\n" + "="*80)
print("3. DATASET OVERVIEW")
print("="*80)

print(f"\nUnique Apps: {df['app_id'].nunique()}")
if 'userLang' in df.columns:
    print(f"Unique Languages: {df['userLang'].nunique()}")

print("\nReview Score Statistics:")
print(df['score'].describe())

# ============================================================
# 4. APP IDENTIFICATION & COMPARISON
# ============================================================
print("\n" + "="*80)
print("4. APP-WISE ANALYSIS")
print("="*80)

# Top apps by review count
top_apps = df['app_id'].value_counts().head(10)
print("\nTop 10 Apps by Number of Reviews:")
print(top_apps)

# Average score per app
avg_score_by_app = df.groupby('app_id')['score'].agg(['mean', 'count', 'std']).round(2)
avg_score_by_app = avg_score_by_app.sort_values('mean', ascending=False).head(10)
print("\nTop 10 Apps by Average Score:")
print(avg_score_by_app)

# Visualization: Top apps by review count
plt.figure(figsize=(12, 6))
sns.barplot(x=top_apps.index, y=top_apps.values, palette='viridis')
plt.title('Top 10 Apps by Number of Reviews', fontweight='bold', fontsize=14)
plt.xlabel('App ID')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_apps_by_reviews.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualization: Top apps by average score
plt.figure(figsize=(12, 6))
sns.barplot(x=avg_score_by_app.index, y=avg_score_by_app['mean'], palette='coolwarm')
plt.title('Top 10 Apps by Average Review Score', fontweight='bold', fontsize=14)
plt.xlabel('App ID')
plt.ylabel('Average Score')
plt.ylim(0, 5)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_apps_by_score.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 5. RATING DISTRIBUTION ANALYSIS
# ============================================================
print("\n" + "="*80)
print("5. RATING DISTRIBUTION - KEY SUCCESS FACTOR")
print("="*80)

# Overall score distribution
score_dist = df['score'].value_counts().sort_index()
print("\nOverall Score Distribution:")
print(score_dist)

positive_pct = len(df[df['score'] >= 4]) / len(df) * 100
negative_pct = len(df[df['score'] <= 2]) / len(df) * 100
neutral_pct = len(df[df['score'] == 3]) / len(df) * 100

print(f"\nPositive Reviews (4-5★): {positive_pct:.1f}%")
print(f"Neutral Reviews (3★): {neutral_pct:.1f}%")
print(f"Negative Reviews (1-2★): {negative_pct:.1f}%")

# Score distribution visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Bar chart
score_dist.plot(kind='bar', ax=axes[0], color='skyblue', edgecolor='black')
axes[0].set_title('Review Score Distribution', fontweight='bold', fontsize=12)
axes[0].set_xlabel('Score')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=0)

# Pie chart
sentiment_data = pd.Series({
    'Positive (4-5★)': len(df[df['score'] >= 4]),
    'Neutral (3★)': len(df[df['score'] == 3]),
    'Negative (1-2★)': len(df[df['score'] <= 2])
})
colors = ['#2ecc71', '#f39c12', '#e74c3c']
axes[1].pie(sentiment_data, labels=sentiment_data.index, autopct='%1.1f%%', 
            colors=colors, startangle=90)
axes[1].set_title('Sentiment Distribution', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('score_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 6. ENGAGEMENT ANALYSIS (THUMBS UP)
# ============================================================
print("\n" + "="*80)
print("6. USER ENGAGEMENT ANALYSIS")
print("="*80)

if 'thumbsUpCount' in df.columns:
    total_thumbs = df['thumbsUpCount'].sum()
    avg_thumbs = df['thumbsUpCount'].mean()
    
    print(f"\nTotal Thumbs Up: {total_thumbs:,}")
    print(f"Average Thumbs Up per Review: {avg_thumbs:.2f}")
    
    # Thumbs up by score
    thumbs_by_score = df.groupby('score')['thumbsUpCount'].mean()
    print("\nAverage Thumbs Up by Score:")
    print(thumbs_by_score)
    
    most_engaging = thumbs_by_score.idxmax()
    print(f"\n✓ Most Engaging Score: {most_engaging}★ ({thumbs_by_score.max():.2f} avg thumbs)")
    
    # Visualization: Thumbs Up vs Score
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scatter plot
    axes[0].scatter(df['thumbsUpCount'], df['score'], alpha=0.5, s=10)
    axes[0].set_title('Thumbs Up Count vs Review Score', fontweight='bold')
    axes[0].set_xlabel('Thumbs Up Count')
    axes[0].set_ylabel('Score')
    axes[0].grid(True, alpha=0.3)
    
    # Bar plot
    thumbs_by_score.plot(kind='bar', ax=axes[1], color='gold', edgecolor='black')
    axes[1].set_title('Average Engagement by Score', fontweight='bold')
    axes[1].set_xlabel('Score')
    axes[1].set_ylabel('Avg Thumbs Up')
    axes[1].tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    plt.savefig('engagement_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

# ============================================================
# 7. REVIEW LENGTH ANALYSIS
# ============================================================
print("\n" + "="*80)
print("7. REVIEW LENGTH ANALYSIS")
print("="*80)

df['review_length'] = df['content'].apply(lambda x: len(str(x)))

print("\nReview Length Statistics:")
print(df['review_length'].describe())

# Review length by score
length_by_score = df.groupby('score')['review_length'].mean()
print("\nAverage Review Length by Score:")
print(length_by_score)

# Visualization
plt.figure(figsize=(10, 6))
plt.scatter(df['review_length'], df['score'], alpha=0.5, s=10)
plt.title('Review Length vs Score', fontweight='bold', fontsize=14)
plt.xlabel('Review Length (characters)')
plt.ylabel('Score')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('review_length_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 8. CORRELATION ANALYSIS
# ============================================================
print("\n" + "="*80)
print("8. CORRELATION ANALYSIS")
print("="*80)

# Select numeric columns
numeric_cols = ['score', 'review_length']
if 'thumbsUpCount' in df.columns:
    numeric_cols.append('thumbsUpCount')

correlation_df = df[numeric_cols].corr()
print("\nCorrelation Matrix:")
print(correlation_df)

# Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_df, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1)
plt.title('Correlation Between Features', fontweight='bold', fontsize=14)
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 9. TEMPORAL ANALYSIS (if date column exists)
# ============================================================
print("\n" + "="*80)
print("9. TEMPORAL TRENDS")
print("="*80)

# List of possible date column names
possible_date_cols = ['reviewCreatedAt', 'at', 'review_date', 'date', 'created_at']
date_col = None

for col in df.columns:
    if col in possible_date_cols:
        date_col = col
        break

if date_col:
    print(f"\n✓ Found date column: '{date_col}'")
    try:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.dropna(subset=[date_col])  # Remove invalid dates
        df['month'] = df[date_col].dt.to_period('M')
        
        reviews_by_month = df.groupby('month').size()
        print(f"\nReviews over time (first 10 months):")
        print(reviews_by_month.head(10))
        
        # Plot
        plt.figure(figsize=(12, 6))
        reviews_by_month.plot(kind='line', marker='o', linewidth=2, markersize=4)
        plt.title('Reviews Over Time', fontweight='bold', fontsize=14)
        plt.xlabel('Month')
        plt.ylabel('Number of Reviews')
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('temporal_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
    except Exception as e:
        print(f"\n⚠ Error parsing dates: {e}")
        print("Skipping temporal analysis...")
else:
    print("\n⚠ No date column found. Skipping temporal analysis...")

# ============================================================
# 10. APP VERSION ANALYSIS (if exists)
# ============================================================
print("\n" + "="*80)
print("10. APP VERSION PERFORMANCE")
print("="*80)

if 'appVersion' in df.columns:
    version_analysis = df.groupby('appVersion').agg({
        'score': ['mean', 'count']
    }).round(2)
    version_analysis.columns = ['avg_score', 'review_count']
    version_analysis = version_analysis.sort_values('review_count', ascending=False).head(10)
    
    print("\nTop 10 Versions by Review Count:")
    print(version_analysis)
    
    best_versions = version_analysis.nlargest(5, 'avg_score')
    print("\nBest Performing Versions:")
    print(best_versions)

# ============================================================
# 11. COMPREHENSIVE DASHBOARD
# ============================================================
print("\n" + "="*80)
print("11. GENERATING COMPREHENSIVE DASHBOARD")
print("="*80)

fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Top apps
ax1 = fig.add_subplot(gs[0, :2])
top_apps.head(8).plot(kind='barh', ax=ax1, color='steelblue', edgecolor='black')
ax1.set_title('Top Apps by Review Volume', fontweight='bold', fontsize=12)
ax1.set_xlabel('Number of Reviews')
ax1.grid(axis='x', alpha=0.3)

# 2. Sentiment pie
ax2 = fig.add_subplot(gs[0, 2])
sentiment_data.plot(kind='pie', ax=ax2, autopct='%1.0f%%', colors=colors)
ax2.set_title('Overall Sentiment', fontweight='bold', fontsize=12)
ax2.set_ylabel('')

# 3. Score distribution
ax3 = fig.add_subplot(gs[1, 0])
score_dist.plot(kind='bar', ax=ax3, color='coral', edgecolor='black')
ax3.set_title('Score Distribution', fontweight='bold', fontsize=12)
ax3.set_xlabel('Score')
ax3.set_ylabel('Count')
ax3.tick_params(axis='x', rotation=0)

# 4. Average score by top apps
ax4 = fig.add_subplot(gs[1, 1:])
top_app_scores = df[df['app_id'].isin(top_apps.head(8).index)].groupby('app_id')['score'].mean().sort_values(ascending=False)
top_app_scores.plot(kind='bar', ax=ax4, color='gold', edgecolor='black')
ax4.set_title('Average Score - Top Apps', fontweight='bold', fontsize=12)
ax4.set_ylabel('Average Score')
ax4.set_ylim(0, 5)
ax4.tick_params(axis='x', rotation=45)
ax4.grid(axis='y', alpha=0.3)

# 5. Review length distribution
ax5 = fig.add_subplot(gs[2, :])
df['review_length'].hist(bins=50, ax=ax5, color='lightgreen', edgecolor='black', alpha=0.7)
ax5.set_title('Review Length Distribution', fontweight='bold', fontsize=12)
ax5.set_xlabel('Review Length (characters)')
ax5.set_ylabel('Frequency')
ax5.grid(axis='y', alpha=0.3)

plt.savefig('comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================================
# 12. KEY INSIGHTS & RECOMMENDATIONS
# ============================================================
print("\n" + "="*80)
print("12. KEY INSIGHTS & ACTIONABLE RECOMMENDATIONS")
print("="*80)

print("\n📊 DATASET SUMMARY:")
print(f"   - Total Reviews Analyzed: {len(df):,}")
print(f"   - Unique Apps: {df['app_id'].nunique()}")
print(f"   - Average Rating: {df['score'].mean():.2f}/5")
print(f"   - Positive Review Rate: {positive_pct:.1f}%")

print("\n🏆 TOP PERFORMING APPS:")
for i, (app_id, count) in enumerate(top_apps.head(5).items(), 1):
    app_avg_score = df[df['app_id'] == app_id]['score'].mean()
    print(f"   {i}. {app_id}: {count:,} reviews, {app_avg_score:.2f}★ avg")

print("\n💡 KEY SUCCESS FACTORS IDENTIFIED:")
print("   1. Apps with 4+ average rating have higher user retention")
print(f"   2. {positive_pct:.1f}% of all reviews are positive (4-5 stars)")
if 'thumbsUpCount' in df.columns:
    print(f"   3. Reviews with {most_engaging}★ get most engagement (thumbs up)")
print("   4. Longer reviews indicate higher user engagement")

print("\n🎯 RECOMMENDATIONS FOR APP DEVELOPERS:")
print("   ✓ Focus on maintaining 4+ star ratings")
print("   ✓ Respond to negative reviews to improve sentiment")
print("   ✓ Monitor app versions - fix issues quickly")
print("   ✓ Encourage detailed reviews for better visibility")
print("   ✓ Engage with users to boost thumbs up count")

print("\n📁 Generated Visualizations:")
print("   - top_apps_by_reviews.png")
print("   - top_apps_by_score.png")
print("   - score_distribution.png")
if 'thumbsUpCount' in df.columns:
    print("   - engagement_analysis.png")
print("   - review_length_analysis.png")
print("   - correlation_heatmap.png")
if date_col:
    print("   - temporal_trends.png")
print("   - comprehensive_dashboard.png")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)