import requests
import streamlit as st
import json
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
        return response.json()  # Return the JSON response
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

def analyze_profile(profile_data):
    insights = []

    if profile_data.get('occupation'):
        insights.append(f"**Occupation:** {profile_data['occupation']}")
    else:
        insights.append("No occupation specified.")

    if profile_data.get('skills'):
        insights.append(f"**Skills:** {', '.join(profile_data['skills'])}")
    else:
        insights.append("No skills listed.")

    if profile_data.get('experiences'):
        insights.append(f"**Total Experiences:** {len(profile_data['experiences'])}")
    else:
        insights.append("No experiences listed.")

    if profile_data.get('education'):
        insights.append(f"**Total Education Entries:** {len(profile_data['education'])}")
    else:
        insights.append("No education entries listed.")

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

    insights.append(f"**Profile Completeness Score:** {score}/100")

    return insights

st.title("LinkedIn Profile Analyzer")
st.markdown("### Get insights on LinkedIn profiles")

linkedin_profile_url = st.text_input("Enter the LinkedIn profile URL:")

if st.button("Analyze Profile"):
    if linkedin_profile_url:
        profile_data = get_linkedin_profile(linkedin_profile_url)

        if profile_data:
            st.subheader("Profile Summary")
            st.image(profile_data.get('profile_pic_url'), width=100)
            st.write(f"**Full Name:** {profile_data.get('full_name')}")
            st.write(f"**Headline:** {profile_data.get('headline')}")
            st.write(f"**Summary:** {profile_data.get('summary')}")
            st.write(f"**Location:** {profile_data.get('city')}, {profile_data.get('country_full_name')}")
            st.write(f"**Follower Count:** {profile_data.get('follower_count')}")

            st.subheader("Insights and Analysis")
            insights = analyze_profile(profile_data)
            for insight in insights:
                st.write(insight)

            if profile_data.get('experiences'):
                st.subheader("Experiences")
                for exp in profile_data['experiences']:
                    st.write(f"**{exp['title']}** at {exp['company'] if exp['company'] else 'N/A'}")
                    st.write(f"**Duration:** {exp['starts_at']['year']} - {'Present' if exp['ends_at'] is None else str(exp['ends_at']['year'])}")
                    st.write(f"**Description:** {exp['description'] if exp['description'] else 'N/A'}")
                    st.write("---")

            

        else:
            st.error("Failed to retrieve profile data.")
    else:
        st.error("Please enter a valid LinkedIn profile URL.")