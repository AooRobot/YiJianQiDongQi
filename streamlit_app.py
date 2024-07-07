import streamlit as st
import subprocess
import os
import json
from typing import Dict
import base64

# Function to load apps from a JSON file
def load_apps() -> Dict[str, str]:
    if os.path.exists("apps.json"):
        with open("apps.json", "r") as f:
            return json.load(f)
    return {}

# Function to save apps to a JSON file
def save_apps(apps: Dict[str, str]):
    with open("apps.json", "w") as f:
        json.dump(apps, f)

# Function to launch an app
def launch_app(app_path: str):
    try:
        subprocess.Popen(app_path)
        st.success(f"Launched {app_path} successfully!")
    except FileNotFoundError:
        st.error(f"Could not find {app_path}. Make sure the path is correct.")

# Function to get base64 encoded image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Main function
def main():
    st.set_page_config(page_title="Sleek App Launcher", layout="wide")
    
    # Uncomment the following line and provide a path to a background image to set it
    # set_background('path_to_your_background_image.png')

    # Custom CSS
    st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: #1E90FF;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        transition-duration: 0.4s;
        cursor: pointer;
        border-radius: 12px;
        border: 2px solid #4CAF50;
    }
    .stButton>button:hover {
        background-color: white; 
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="big-font">Sleek App Launcher</p>', unsafe_allow_html=True)

    # Load existing apps
    apps = load_apps()

    # Sidebar for adding new apps
    with st.sidebar:
        st.header("Add New App")
        new_app_name = st.text_input("App Name")
        new_app_path = st.text_input("App Path")
        if st.button("Add App", key='add'):
            if new_app_name and new_app_path:
                apps[new_app_name] = new_app_path
                save_apps(apps)
                st.success(f"Added {new_app_name} to the launcher!")
            else:
                st.warning("Please enter both app name and path.")

    # Main area for launching apps
    if apps:
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Launch App")
            selected_app = st.selectbox("Select an application:", list(apps.keys()))
            if st.button("Launch App", key='launch'):
                launch_app(apps[selected_app])

        with col2:
            st.header("Manage Apps")
            app_to_remove = st.selectbox("Select an application to remove:", list(apps.keys()))
            if st.button("Remove App", key='remove'):
                del apps[app_to_remove]
                save_apps(apps)
                st.success(f"Removed {app_to_remove} from the launcher!")
                st.experimental_rerun()

        # Display all apps in a nice grid
        st.header("Your Apps")
        cols = st.columns(4)
        for idx, (app_name, app_path) in enumerate(apps.items()):
            with cols[idx % 4]:
                st.markdown(f"**{app_name}**")
                if st.button(f"Launch {app_name}", key=f'launch_{idx}'):
                    launch_app(app_path)

    else:
        st.info("No apps added yet. Use the sidebar to add some apps!")

if __name__ == "__main__":
    main()