import streamlit as st
import matplotlib.pyplot as plt
import requests

st.title("Assistant météo")

url = url = "https://api.open-meteo.com/v1/forecast?latitude=48.5734&longitude=7.7521&daily=temperature_2m_max,temperature_2m_min,rain_sum,windspeed_10m_max,weathercode&timezone=Europe/Paris&forecast_days=10"
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


st.subheader("Prévisions sur les 10 prochains jours")

st.subheader("Températures sur 10 jours")

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(dates, temp_max, marker="o", label="Température max")
ax1.plot(dates, temp_min, marker="o", label="Température min")

ax1.set_xlabel("Date")
ax1.set_ylabel("Température (°C)")
ax1.set_title("Températures max/min à Strasbourg")
ax1.legend()
ax1.tick_params(axis="x", rotation=45)

st.pyplot(fig1)


fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.plot(dates, vent, marker="o")

ax2.set_xlabel("Date")
ax2.set_ylabel("Vent max (km/h)")
ax2.set_title("Vitesse maximale du vent")
ax2.tick_params(axis="x", rotation=45)

st.pyplot(fig2)



fig3, ax3 = plt.subplots(figsize=(10, 5))

ax3.bar(dates, pluie)

ax3.set_xlabel("Date")
ax3.set_ylabel("Pluie (mm)")
ax3.set_title("Quantité de pluie prévue")
ax3.tick_params(axis="x", rotation=45)

st.pyplot(fig3)

st.subheader("État du ciel sur 10 jours")

for i in range(10):
    description = codes_meteo.get(wethercode[i], "Météo inconnue")
    st.write(dates[i], ":", description)