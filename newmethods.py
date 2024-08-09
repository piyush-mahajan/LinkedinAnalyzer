import requests
import streamlit as st
import json
import plotly.graph_objects as go
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(layout="wide", page_title="LinkedIn Profile Analyzer")

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        background-color: black;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .st-bw {
        background-color: white;
    }
    div[data-testid="metric-container"] {
        background-color: #000000;
        border: 1px solid #cccccc;
        padding: 5% 5% 5% 10%;
        border-radius: 5px;
        color: #ffffff;
        overflow-wrap: break-word;
    }

    /* breakline for metric text         */
    div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
        overflow-wrap: break-word;
        white-space: break-spaces;
        color: #ffffff;
    }

    div[data-testid="metric-container"] > div[data-testid="stMetricValue"] > div {
        color: #00ff00;
    }
</style>
""", unsafe_allow_html=True)

API_KEY = st.secrets["proxycurl"]["api_key"]

headers = {
    'Authorization': 'Bearer ' + API_KEY
}

api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

def get_linkedin_profile(linkedin_profile_url):
    params = {
        'url': linkedin_profile_url,
        'skills': 'include'  
    }

    response = requests.get(api_endpoint, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

def analyze_profile(profile_data):
    insights = []

    if profile_data.get('occupation'):
        insights.append(("Occupation", profile_data['occupation']))
    else:
        insights.append(("Occupation", "Not specified"))

    if profile_data.get('skills'):
        insights.append(("Skills", len(profile_data['skills'])))
    else:
        insights.append(("Skills", 0))

    if profile_data.get('experiences'):
        insights.append(("Experiences", len(profile_data['experiences'])))
    else:
        insights.append(("Experiences", 0))

    if profile_data.get('education'):
        insights.append(("Education", len(profile_data['education'])))
    else:
        insights.append(("Education", 0))

    score = 0
    if profile_data.get('occupation'):
        score += 20
    if profile_data.get('skills'):
        score += 20
    if profile_data.get('experiences'):
        score += 20
    if profile_data.get('education'):
        score += 20
    if profile_data.get('summary'):
        score += 20

    insights.append(("Profile Score", f"{score}%"))

    return insights

def create_radar_chart(profile_data):
    categories = ['Occupation', 'Skills', 'Experiences', 'Education', 'Summary']
    values = [
        20 if profile_data.get('occupation') else 0,
        20 if profile_data.get('skills') else 0,
        20 if profile_data.get('experiences') else 0,
        20 if profile_data.get('education') else 0,
        20 if profile_data.get('summary') else 0
    ]

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Profile Completeness'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            )),
        showlegend=False
    )

    return fig

st.title("LinkedIn Profile Analyzer")
# colored_header(label="Get insights on LinkedIn profiles")

linkedin_profile_url = st.text_input("Enter the LinkedIn profile URL:")

if st.button("Analyze Profile"):
    if linkedin_profile_url:
        with st.spinner("Analyzing profile..."):
            profile_data = get_linkedin_profile(linkedin_profile_url)

        if profile_data:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(profile_data.get('profile_pic_url', 'https://via.placeholder.com/150'), width=150)
                st.subheader(profile_data.get('full_name', 'N/A'))
                st.write(profile_data.get('headline', 'N/A'))
                st.write(f"📍 {profile_data.get('city', 'N/A')}, {profile_data.get('country_full_name', 'N/A')}")
                st.write(f"👥 {profile_data.get('follower_count', 'N/A')} followers")

            with col2:
                colored_header(label="Profile Summary", description="", color_name="blue-30")
                st.write(profile_data.get('summary', 'No summary available.'))

            add_vertical_space(2)

            col1, col2 = st.columns(2)

            with col1:
                colored_header(label="Profile Insights", description="", color_name="blue-30")
                insights = analyze_profile(profile_data)
                for label, value in insights:
                    if label == "Skills" and isinstance(value, list):
                        st.metric(label, len(value))
                    else:
                        st.metric(label, value)

            with col2:
                colored_header(label="Profile Completeness", description="", color_name="blue-30")
                fig = create_radar_chart(profile_data)
                st.plotly_chart(fig, use_container_width=True)

            colored_header(label="Experience Timeline", description="", color_name="blue-30")
            if profile_data.get('experiences'):
                for exp in profile_data['experiences']:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.write(f"**{exp['starts_at']['year']} - {'Present' if exp['ends_at'] is None else exp['ends_at']['year']}**")
                    with col2:
                        st.write(f"**{exp['title']}** at {exp['company'] if exp['company'] else 'N/A'}")
                        st.write(f"{exp['description'] if exp['description'] else 'N/A'}")
                    st.write("---")
            else:
                st.write("No experiences listed.")

            if profile_data.get('skills'):
                colored_header(label="Skills", description="", color_name="blue-30")
                skills = profile_data['skills']
                cols = st.columns(3)
                for i, skill in enumerate(skills):
                    cols[i % 3].write(f"- {skill}")

        else:
            st.error("Failed to retrieve profile data.")
    else:
        st.error("Please enter a valid LinkedIn profile URL.")