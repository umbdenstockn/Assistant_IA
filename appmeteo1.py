# application météo sans graphique, juste du texte et des données

import streamlit as st
import requests

st.title("Assistant météo")

url = "https://api.open-meteo.com/v1/forecast?latitude=48.5734&longitude=7.7521&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,showers_sum,snowfall_sum,windspeed_10m_max,windgusts_10m_max,weathercode&timezone=Europe/Paris"
response = requests.get(url)
data = response.json() 

daily = data["daily"]

dates = daily["time"]
temp_max = daily["temperature_2m_max"]
temp_min = daily["temperature_2m_min"]
pluie = daily["rain_sum"]
vent = daily["windspeed_10m_max"]
wethercode = daily["weathercode"]

codes_meteo = {
    0: "Ciel dégagé",

    1: "Principalement dégagé",
    2: "Partiellement nuageux",
    3: "Couvert",

    45: "Brouillard",
    48: "Brouillard givrant",

    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",

    56: "Bruine verglaçante légère",
    57: "Bruine verglaçante dense",

    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",

    66: "Pluie verglaçante légère",
    67: "Pluie verglaçante forte",

    71: "Chute de neige légère",
    73: "Chute de neige modérée",
    75: "Chute de neige forte",

    77: "Grains de neige",

    80: "Averses de pluie légères",
    81: "Averses de pluie modérées",
    82: "Averses de pluie violentes",

    85: "Averses de neige légères",
    86: "Averses de neige fortes",

    95: "Orage",

    96: "Orage avec grêle légère",
    99: "Orage avec forte grêle"
}

st.subheader("Météo du jour à Strasbourg")

st.write("Date :", dates[0])
st.write(codes_meteo.get(wethercode[0], "Code météo inconnu"))
st.write("Température max :", temp_max[0], "°C")
st.write("Température min :", temp_min[0], "°C")
st.write("Pluie :", pluie[0], "mm")
st.write("Vent max :", vent[0], "km/h")


st.subheader("Prévisions sur les 6 prochains jours")

for i in range(1, 7, 1):
    st.write("Date :", dates[i])
    st.write(codes_meteo.get(wethercode[i], "Code météo inconnu"))
    st.write("Température max :", temp_max[i], "°C")
    st.write("Température min :", temp_min[i], "°C")
    st.write("Pluie :", pluie[i], "mm")
    st.write("Vent max :", vent[i], "km/h")
    st.write("---")