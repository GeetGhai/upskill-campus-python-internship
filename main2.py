import streamlit as st
import requests

def shorten_link(full_link, link_name):
    API_KEY = 'e030b7c22881d174e98166f7b9ba3b31b5fd3'  # Ensure your API key is correct
    Base_api = 'https://cutt.ly/api/api.php'

    payload = {'key': API_KEY, 'short': full_link, 'name': link_name}
    
    try:
        response = requests.get(Base_api, params=payload)
        
        # Check if the response is in JSON format
        try:
            data = response.json()
            st.write(f"Response status code: {response.status_code}")
            st.write(f"Response content: {data}")  # Debug: Show JSON content
        except ValueError:  # Response is not JSON
            st.error(f"Non-JSON response received: {response.text}")
            return "Error: Received a non-JSON response from the API.", ""

        # Ensure that the response has the expected structure
        if 'url' not in data or 'status' not in data['url']:
            st.error(f"Unexpected response structure: {data}")
            return "Unexpected response structure from the API.", ""

        if data['url']['status'] == 7:  # Status code 7 indicates the link was shortened successfully
            title = data['url']['title']
            short_link = data['url']['shortLink']
            return f"Title: {title}", f"Shortened Link: {short_link}"
        else:
            # Specific error handling based on status codes from Cuttly API
            status = data['url']['status']
            if status == 1:
                return "Error: The shortened link has not passed the validation. Please check the link format.", ""
            elif status == 2:
                return "Error: The entered link is not a valid URL.", ""
            elif status == 3:
                return "Error: The link name is already taken. Please choose a different name.", ""
            elif status == 4:
                return "Error: You have exceeded the maximum number of allowed API requests.", ""
            elif status == 5:
                return "Error: The link for shortening is from a blocked domain.", ""
            else:
                return f"Unexpected error status: {status}.", ""
    except requests.exceptions.RequestException as e:
        return f'An error occurred: {e}', ''
    except KeyError as e:
        return f'Key error: {e}', ''

# Streamlit App Interface
st.title('URL Shortener')

# Input fields
full_link = st.text_input('Enter the full link:')
link_name = st.text_input('Enter a name for your link:')

if st.button('Shorten Link'):
    if full_link and link_name:
        title, short_link = shorten_link(full_link, link_name)
        if "Error" in title:
            st.error(title)  # Display errors with Streamlit's error message
        else:
            st.success(title)  # Display success messages
            st.write(short_link)
    else:
        st.error('Please provide both a link and a name.')
