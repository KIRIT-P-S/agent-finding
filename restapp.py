import os
import streamlit as st
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Restaurant Finder", layout="wide")
st.title("🍽️ AI-Powered Restaurant Finder")

st.header("Find the Best Restaurants Near You")

city = st.text_input("📍 Enter your city or area:", placeholder="e.g., Coimbatore")

if st.button("Find Restaurants"):
    if not city:
        st.warning("Please enter a location.")
    else:
        with st.spinner("Searching for restaurants..."):
            web_agent = Agent(
                name="Restaurant Finder",
                model=Groq(id="llama-3.3-70b-versatile"), 
                tools=[DuckDuckGo(search=True)],
                instructions=[
                    "Search for popular restaurants in the given city.",
                    "Include restaurant names, addresses, cuisine type, and if available, ratings or reviews.",
                    "Use DuckDuckGo to find results for 'best restaurants in <city>'.",
                    "Present results in a clean, structured list with headings.",
                    "Focus on actual restaurant names and locations (e.g., 'Annapoorna Gowrishankar - Crosscut Road').",
                ],
                markdown=True,
                debug_mode=True,
            )
            response = web_agent.run(f"Best restaurants in {city} with location, cuisine, and rating")

            st.markdown("## 🍴 Available Restaurants")
            if hasattr(response, 'content'):
                restaurants = response.content.split("\n")
                for restaurant in restaurants:
                    if restaurant.strip():
                        st.markdown(f"- {restaurant.strip()}")
            else:
                st.markdown("No results found. Please try another city.")

# Debug Info
st.sidebar.header("🔧 Debug Info")
st.sidebar.write("Debug mode is enabled for detailed responses.")

st.sidebar.markdown("### Share this App:")
st.sidebar.markdown("[Visit the App](https://your-app-url.streamlit.app/)")
