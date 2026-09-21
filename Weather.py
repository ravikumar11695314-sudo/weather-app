
import streamlit as streamlit 
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="wide")

# Helper function to load Lottie JSON safely
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

# Reliable Lottie Links
LOTTIE_ANIMATIONS = {
    "Clear": "https://lottie.host/81f8f782-b7ca-4d56-b040-7e3995f7004d/G3vK89Qv4A.json",
    "Clouds": "https://lottie.host/880e4b85-5a7a-4066-834e-ee7e6ffea2d2/H27XgQx2pT.json",
    "Rain": "https://lottie.host/a61db4e9-0264-4bf8-b99b-31463bd9b2dd/c5L98kL5s2.json",
    "Drizzle": "https://lottie.host/a61db4e9-0264-4bf8-b99b-31463bd9b2dd/c5L98kL5s2.json",
    "Thunderstorm": "https://lottie.host/17e2ef30-4e09-42b4-a5e2-e1dce1b539a2/U4mB591pS2.json",
}

WEATHER_ICONS = {
    "Clear": "☀️", "Clouds": "☁️", "Rain": "🌧️", "Drizzle": "🌦️", "Thunderstorm": "⛈️", "Mist": "🌫️", "Fog": "🌫️"
}

st.markdown("<h1 style='text-align: center; color: #ffffff;'>🌤️ Weather Dashboard</h1>", unsafe_allow_html=True)

# CSS for styling metrics & search section
st.markdown(""" <style> .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); } div[data-testid="stMetric"] { background-color: rgba(255, 255, 255, 0.12); padding: 15px; border-radius: 16px; backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.2); } div[data-testid="stForm"] { border: none; } </style> """, unsafe_allow_html=True)

# CHOTA SEARCH BAR (Center Alignment with Form)
col_s1, col_s2, col_s3 = st.columns([1, 2, 1])

with col_s2:
    with st.form("search_form"):
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            city = st.text_input("City Name", "Delhi", label_visibility="collapsed", placeholder="Enter City Name...")
        with search_col2:
            submitted = st.form_submit_button("🔍 Search", use_container_width=True)

api_key = "bec6b1c3b6eff584500fb13dc0981aee"

if submitted or city:
    url_current = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url_current).json()

    if data.get("cod") == 200:
        main_cond = data['weather'][0]['main']

        st.markdown(f"## 📍 {city.capitalize()} ka Mausam")

        # 3-Column Layout
        col_left, col_center, col_right = st.columns([1, 2, 1])

        # LEFT SIDE
        with col_left:
            st.subheader("📊 Pressure & Visibility")
            st.metric("Pressure", f"{data['main']['pressure']} hPa")
            st.metric("Visibility", f"{data['visibility'] / 1000} km")

        # CENTER SIDE
        with col_center:
            lottie_url = LOTTIE_ANIMATIONS.get(main_cond, LOTTIE_ANIMATIONS["Clear"])
            lottie_json = load_lottieurl(lottie_url)
            
            if lottie_json:
                st_lottie(lottie_json, height=140, key="main_weather")
            else:
                icon = WEATHER_ICONS.get(main_cond, "🌤️")
                st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{icon}</h1>", unsafe_allow_html=True)

            st.markdown(f"<h1 style='text-align: center; margin:0;'>{data['main']['temp']} °C</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 18px;'>{data['weather'][0]['description'].title()}</p>", unsafe_allow_html=True)
            
            st.write("")
            m1, m2, m3 = st.columns(3)
            m1.metric("Feels Like", f"{data['main']['feels_like']} °C")
            m2.metric("Humidity", f"{data['main']['humidity']}%")
            m3.metric("Wind Speed", f"{data['wind']['speed']} m/s")

        # RIGHT SIDE
        with col_right:
            st.subheader("🌡️ Temperature Range")
            st.metric("Max Temp", f"{data['main']['temp_max']} °C")
            st.metric("Min Temp", f"{data['main']['temp_min']} °C")

        # 5-DAY FORECAST
        st.markdown("---")
        st.subheader("📅 5-Day Forecast")
        
        url_forecast = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
        forecast_data = requests.get(url_forecast).json()

        if forecast_data.get("cod") == "200":
            cols = st.columns(5)
            daily_list = [item for item in forecast_data['list'] if "12:00:00" in item['dt_txt']][:5]
            
            for idx, item in enumerate(daily_list):
                date_str = datetime.strptime(item['dt_txt'].split()[0], "%Y-%m-%d").strftime("%d %b")
                temp = item['main']['temp']
                desc_main = item['weather'][0]['main']
                f_icon = WEATHER_ICONS.get(desc_main, "🌡️")
                
                with cols[idx]:
                    st.metric(label=date_str, value=f"{temp}°C")
                    st.write(f"{f_icon} {desc_main}")
    else:
        st.error("City nahi mili!")
