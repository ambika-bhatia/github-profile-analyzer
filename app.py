import streamlit as st
import pandas as pd
from github_api import get_user_info, get_user_repos

st.set_page_config(page_title="GitHub Analyzer", page_icon="🐙", layout="wide")

st.title("GitHub Profile Analyzer")
username = st.text_input("Enter GitHub username:")

if username:
    user_data = get_user_info(username)
    
    if "login" not in user_data:
        st.error("User not found! Please check the username.")
    else:
        # Profile picture + basic info side by side
        col_img, col_info = st.columns([1, 3])
        with col_img:
            st.image(user_data["avatar_url"], width=150)
        with col_info:
            st.subheader(user_data.get("name") or user_data["login"])
            st.write(user_data.get("bio") or "No bio available")
            st.write("📍", user_data.get("location") or "Not specified")
        
        # Stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", user_data["followers"])
        col2.metric("Following", user_data["following"])
        col3.metric("Public Repos", user_data["public_repos"])
        
        # Top 5 repos by stars
        repos_data = get_user_repos(username)
        sorted_repos = sorted(repos_data, key=lambda r: r["stargazers_count"], reverse=True)
        top_5 = sorted_repos[:5]
        
        st.subheader("⭐ Top 5 Repositories")
        for repo in top_5:
            st.markdown(f"**[{repo['name']}]({repo['html_url']})** — ⭐ {repo['stargazers_count']}")
            st.caption(repo.get("description") or "No description")
        
        # Language chart
        language_count = {}
        for repo in repos_data:
            lang = repo["language"]
            if lang is not None:
                language_count[lang] = language_count.get(lang, 0) + 1
        
        df = pd.DataFrame(list(language_count.items()), columns=["Language", "Count"])
        st.bar_chart(df.set_index("Language"))