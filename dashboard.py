import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from test import analyze_sentiment, sia

# Set page config
st.set_page_config(
    page_title="Instagram Mood Analyzer Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Instagram Mood Analyzer Dashboard")
st.markdown("""
This dashboard shows your Instagram activity mood analysis and emotional patterns over time.
""")

# Load and process data
@st.cache_data
def load_data():
    folder_path = "data"
    all_data = []
    
    # Load all JSON files and process them
    json_files = {
        "likes": "insta_mood_mock_likes.json",
        "reels": "insta_mood_mock_reels.json",
        "messages": "insta_mood_mock_messages.json",
        "ads": "insta_mood_mock_ads_and_interests.json",
        "videos": "insta_mood_mock_watch_history.json"
    }
    
    for source, filename in json_files.items():
        try:
            with open(os.path.join(folder_path, filename)) as f:
                data = json.load(f)
                if source == "messages":
                    for convo in data:
                        if 'messages' in convo:
                            for msg in convo['messages']:
                                msg['source'] = source
                                msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
                                msg['date'] = msg['timestamp'].date()
                                s = analyze_sentiment(msg.get('content', ''))
                                msg['mood'] = s['label']
                                msg['mood_score'] = s['compound']
                                all_data.append(msg)
                else:
                    for item in data:
                        item['source'] = source
                        item['timestamp'] = datetime.fromisoformat(item['timestamp'])
                        item['date'] = item['timestamp'].date()
                        if source != "videos":
                            s = analyze_sentiment(item.get('caption', '') or item.get('content', ''))
                            item['mood'] = s['label']
                            item['mood_score'] = s['compound']
                        else:
                            item['mood'] = "neutral"
                            item['mood_score'] = 0.0
                        all_data.append(item)
        except Exception as e:
            st.error(f"Error loading {filename}: {str(e)}")
    
    return pd.DataFrame(all_data)

# Load the data
df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

sources = st.sidebar.multiselect(
    "Select Sources",
    options=df['source'].unique(),
    default=df['source'].unique()
)

# Filter data based on sidebar selections
mask = (df['date'] >= date_range[0]) & (df['date'] <= date_range[1]) & (df['source'].isin(sources))
filtered_df = df[mask]

# Create two columns for the layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Mood Trends Over Time")
    
    # Calculate daily mood scores and anomalies
    daily_mood = filtered_df.groupby('date')['mood_score'].mean().reset_index()
    daily_mood['mood_change'] = daily_mood['mood_score'].diff()
    daily_mood['volatility'] = filtered_df.groupby('date')['mood_score'].std()
    daily_mood['activity_level'] = filtered_df.groupby('date').size()
    
    # Detect anomalies
    daily_mood['sudden_drop'] = daily_mood['mood_change'].apply(lambda x: True if x is not None and x < -0.3 else False)
    daily_mood['high_volatility'] = daily_mood['volatility'] > 0.4
    daily_mood['low_activity'] = (daily_mood['activity_level'] < 3) & (daily_mood['mood_score'] < -0.2)
    
    # Create mood trend line chart
    fig = px.line(daily_mood, x='date', y='mood_score',
                  title='Daily Average Mood Score',
                  labels={'mood_score': 'Mood Score', 'date': 'Date'})
    
    # Add anomaly points
    for anomaly_type, color in [
        ('sudden_drop', 'red'),
        ('high_volatility', 'orange'),
        ('low_activity', 'purple')
    ]:
        anomaly_df = daily_mood[daily_mood[anomaly_type]]
        if not anomaly_df.empty:
            fig.add_scatter(
                x=anomaly_df['date'],
                y=anomaly_df['mood_score'],
                mode='markers',
                marker=dict(color=color, size=10),
                name=f'{anomaly_type.replace("_", " ").title()}'
            )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display anomaly details
    st.subheader("🚨 Detected Anomalies")
    
    # Sudden mood drops
    mood_drops = daily_mood[daily_mood['sudden_drop']]
    if not mood_drops.empty:
        st.warning("Sudden Mood Drops Detected")
        for _, row in mood_drops.iterrows():
            st.write(f"- {row['date']}: Mood dropped from {(row['mood_score'] - row['mood_change']):.2f} to {row['mood_score']:.2f}")
    
    # High volatility days
    volatility_days = daily_mood[daily_mood['high_volatility']]
    if not volatility_days.empty:
        st.warning("High Mood Volatility Days")
        for _, row in volatility_days.iterrows():
            st.write(f"- {row['date']}: Volatility = {row['volatility']:.2f}")
    
    # Low activity with negative mood
    low_activity_days = daily_mood[daily_mood['low_activity']]
    if not low_activity_days.empty:
        st.warning("Low Activity with Negative Mood")
        for _, row in low_activity_days.iterrows():
            st.write(f"- {row['date']}: Activity Level = {row['activity_level']}, Mood Score = {row['mood_score']:.2f}")

with col2:
    st.subheader("🎭 Mood Distribution by Source")
    
    # Create mood distribution pie chart
    mood_dist = filtered_df.groupby(['source', 'mood']).size().unstack(fill_value=0)
    fig = px.pie(values=mood_dist.values.flatten(),
                 names=mood_dist.columns.repeat(len(mood_dist)),
                 title='Mood Distribution Across Sources')
    st.plotly_chart(fig, use_container_width=True)

# Mood Summary Table
st.subheader("📊 Mood Summary Table")
summary = filtered_df.groupby(['date', 'source'])['mood'].value_counts().unstack(fill_value=0)
st.dataframe(summary)

# Additional Statistics
col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Total Posts Analyzed", len(filtered_df))

with col4:
    avg_mood = filtered_df['mood_score'].mean()
    st.metric("Average Mood Score", f"{avg_mood:.2f}")

with col5:
    most_common_mood = filtered_df['mood'].mode()[0]
    st.metric("Most Common Mood", most_common_mood)

# Download button for the data
st.download_button(
    label="Download Mood Summary CSV",
    data=summary.to_csv().encode('utf-8'),
    file_name='mood_summary.csv',
    mime='text/csv'
) 