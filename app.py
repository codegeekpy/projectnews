# app.py

import streamlit as st
import feedparser
import requests

# RSS Feeds for AI/ML (updated and verified)
RSS_FEEDS = {
    "TechCrunch AI": "https://techcrunch.com/tag/artificial-intelligence/feed/",
    "MIT News – AI": "https://news.mit.edu/topic/artificial-intelligence/rss.xml",
    "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",
    "OpenAI Blog": "https://openai.com/blog/rss",
    "DeepMind Blog": "https://www.deepmind.com/blog/rss.xml",
    "HuggingFace Blog": "https://huggingface.co/blog/feed.xml",
    "KDnuggets": "https://www.kdnuggets.com/feed",
    "Towards Data Science": "https://towardsdatascience.com/feed",
    "NVIDIA AI": "https://blogs.nvidia.com/blog/category/ai/feed/",
    "VentureBeat AI": "https://venturebeat.com/category/ai/feed/"
}

def get_feed_articles(feed_url, limit=5):
    try:
        response = requests.get(feed_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
    except Exception as e:
        st.error(f"Unable to reach feed: {e}")
        return []

    # DEBUG INFO
    st.write(f"Fetched {len(response.content)} bytes from {feed_url}")
    
    feed = feedparser.parse(response.content)
    
    st.write(f"Parsed feed with {len(feed.entries)} entries")

    if not feed.entries:
        st.warning(f"No entries found in feed at {feed_url}")
        return []

    articles = []
    for entry in feed.entries[:limit]:
        content = getattr(entry, "summary", getattr(entry, "description", entry.title))
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "content": content,
        })
    return articles


# --- Streamlit UI ---
st.set_page_config(page_title="AI/ML News Digest", layout="wide")
st.title("🧠 AI & ML Tech News (Daily Digest)")
st.markdown("Stay updated with the latest AI/ML articles from popular sources.")

feed_choice = st.selectbox("Choose News Source", list(RSS_FEEDS.keys()))

if "articles" not in st.session_state or st.button("🔄 Refresh Feed"):
    with st.spinner("Fetching articles..."):
        st.session_state.articles = get_feed_articles(RSS_FEEDS[feed_choice])

if st.session_state.get("articles"):
    for article in st.session_state.articles:
        st.subheader(article["title"])
        st.write(article["content"], unsafe_allow_html=True)
        st.markdown(f"[Read More]({article['link']})", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.info("No articles to display.")
