# 📊 InstaMood Dashboard

A comprehensive Streamlit dashboard for analyzing Instagram mood and sentiment patterns from user activity data.

## 🌟 Features

- **Mood Analysis Visualization** - Interactive charts showing mood trends over time
- **Sentiment Analysis** - Analysis of messages and interactions
- **Activity Insights** - Comprehensive view of Instagram engagement patterns
- **Interactive Dashboard** - Real-time data exploration with Plotly charts
- **Data Export** - Download mood summaries and insights

## 🚀 Live Demo

🔗 **[View Live Dashboard](https://your-app-url.streamlit.app)** *(Coming Soon)*

## 📋 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/hajira404/Sentigram.git
   cd Sentigram
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:8501`

## 📦 Dependencies

- **streamlit** (1.32.0) - Web app framework
- **pandas** (2.2.0) - Data manipulation and analysis
- **plotly** (5.18.0) - Interactive visualizations
- **nltk** (3.8.1) - Natural language processing

## 📁 Project Structure

```
instalite/
├── dashboard.py              # Main Streamlit application
├── requirements.txt          # Python dependencies
├── mood_summary.csv         # Processed mood data
├── data/                    # Raw Instagram data
│   ├── insta_mood_mock_ads_and_interests.json
│   ├── insta_mood_mock_likes.json
│   ├── insta_mood_mock_messages.json
│   ├── insta_mood_mock_reels.json
│   └── insta_mood_mock_watch_history.json
└── README.md                # Project documentation
```

## 🎯 Data Sources

This dashboard analyzes various Instagram activity patterns:

- **👍 Likes Activity** - Engagement with posts and content
- **💬 Messages** - Sentiment analysis of conversations
- **📺 Ads & Interests** - Targeted content and preferences
- **🎥 Reels Engagement** - Video content interaction patterns
- **📖 Watch History** - Content consumption behavior

## 🔧 Usage

1. **Launch Dashboard**: Run `streamlit run dashboard.py`
2. **Explore Data**: Navigate through different sections using the sidebar
3. **Analyze Trends**: View mood patterns and sentiment analysis
4. **Export Results**: Download insights and summaries

## 🌐 Deployment

This app is deployed on **Streamlit Community Cloud** for easy access and sharing.

### Deploy Your Own Copy

1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with main file: `dashboard.py`

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created by **Hajira** - [GitHub Profile](https://github.com/hajira404)

---

⭐ **Star this repository if you found it helpful!**