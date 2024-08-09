# LinkedIn Profile Analyzer

## Overview

LinkedIn Profile Analyzer is a Streamlit-based web application that allows users to analyze LinkedIn profiles using the Proxycurl API. The app provides insights, visualizations, and a comprehensive breakdown of a LinkedIn profile's content.

![image](https://github.com/user-attachments/assets/737121bb-18c4-46e6-9cd7-ae151ecec4d5)


## Features

- Profile summary display
- Profile completeness score
- Interactive radar chart for profile completeness
- Experience timeline
- Skills breakdown
- Metric cards for key profile insights
- Responsive design for various screen sizes

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Streamlit
- Plotly
- Streamlit-extras
- Requests

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/linkedin-profile-analyzer.git
   cd linkedin-profile-analyzer
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Proxycurl API key:
   - Create a `.streamlit/secrets.toml` file in the project directory
   - Add your API key to the file:
     ```
     [proxycurl]
     api_key = "your_api_key_here"
     ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Enter a LinkedIn profile URL in the input field and click "Analyze Profile"

4. View the analysis results, including profile summary, insights, and visualizations

## Configuration

You can customize the app's appearance by modifying the custom CSS in the `st.markdown()` function at the beginning of the script.

## Contributing

Contributions to the LinkedIn Profile Analyzer are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - https://piyushmahajan.vercel.app/
