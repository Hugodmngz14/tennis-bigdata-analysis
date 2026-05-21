import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Tenis Big Data",
    layout="wide"
)

st.title("Dashboard Big Data - Rendimiento del saque en tenis ATP")

st.write("""
Este dashboard analiza la relación entre la altura de los jugadores y distintas métricas del saque:
porcentaje de primer saque, aces y dobles faltas.
""")

@st.cache_data
def load_data():
    fact = pd.read_csv("fact_serve_sample.csv")
    players = pd.read_csv("dim_player.csv")
    surfaces = pd.read_csv("dim_surface.csv")
    time = pd.read_csv("dim_time.csv")
    tournaments = pd.read_csv("dim_tournament.csv")

    data = fact.merge(players, on="player_key", how="left")
    data = data.merge(surfaces, on="surface_key", how="left")
    data = data.merge(time, on="time_key", how="left")
    data = data.merge(tournaments, on="tournament_key", how="left")

    return data

data = load_data()

st.sidebar.header("Filtros")

surface_filter = st.sidebar.multiselect(
    "Selecciona superficie",
    options=data["surface"].dropna().unique(),
    default=data["surface"].dropna().unique()
)

height_filter = st.sidebar.multiselect(
    "Selecciona grupo de altura",
    options=data["height_group"].dropna().unique(),
    default=data["height_group"].dropna().unique()
)

filtered_data = data[
    (data["surface"].isin(surface_filter)) &
    (data["height_group"].isin(height_filter))
]

st.subheader("Indicadores principales")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Registros analizados", len(filtered_data))
col2.metric("Altura media", round(filtered_data["height"].mean(), 2))
col3.metric("Aces medios", round(filtered_data["aces"].mean(), 2))
col4.metric("Primer saque medio", round(filtered_data["first_serve_pct"].mean(), 2))

st.subheader("Aces medios por grupo de altura")

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtered_data,
    x="height_group",
    y="aces",
    order=["<180", "180-190", "190-200", "200+"],
    ax=ax1
)
ax1.set_xlabel("Grupo de altura")
ax1.set_ylabel("Media de aces")
st.pyplot(fig1)

st.subheader("Porcentaje de primer saque por grupo de altura")

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtered_data,
    x="height_group",
    y="first_serve_pct",
    order=["<180", "180-190", "190-200", "200+"],
    ax=ax2
)
ax2.set_xlabel("Grupo de altura")
ax2.set_ylabel("Porcentaje medio de primer saque")
st.pyplot(fig2)

st.subheader("Aces medios por superficie")

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtered_data,
    x="surface",
    y="aces",
    ax=ax3
)
ax3.set_xlabel("Superficie")
ax3.set_ylabel("Media de aces")
st.pyplot(fig3)

st.subheader("Dobles faltas por grupo de altura")

fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=filtered_data,
    x="height_group",
    y="double_faults",
    order=["<180", "180-190", "190-200", "200+"],
    ax=ax4
)
ax4.set_xlabel("Grupo de altura")
ax4.set_ylabel("Media de dobles faltas")
st.pyplot(fig4)

st.subheader("Tabla de datos filtrada")

st.dataframe(filtered_data.head(100))

st.subheader("Conclusiones principales")

st.write("""
- La altura no muestra una relación fuerte con el porcentaje de primer saque.
- Los jugadores más altos tienden a generar más aces.
- La superficie influye claramente en el rendimiento del saque.
- El análisis permite comparar grupos de altura y superficies de forma visual.
""")
