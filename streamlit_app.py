import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Tenis ATP",
    layout="wide"
)

# =========================
# CARGA DE DATOS
# =========================

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

# =========================
# TÍTULO
# =========================

st.title("Dashboard Big Data: Rendimiento del saque en tenis ATP")

st.markdown("""
Análisis interactivo sobre la relación entre la **altura de los jugadores** y diferentes métricas del saque:
porcentaje de primer saque, aces, dobles faltas y rendimiento según superficie.
""")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("Filtros del análisis")

surface_filter = st.sidebar.multiselect(
    "Superficie",
    options=sorted(data["surface"].dropna().unique()),
    default=sorted(data["surface"].dropna().unique())
)

height_filter = st.sidebar.multiselect(
    "Grupo de altura",
    options=["<180", "180-190", "190-200", "200+"],
    default=["<180", "180-190", "190-200", "200+"]
)

year_filter = st.sidebar.multiselect(
    "Año",
    options=sorted(data["year"].dropna().unique()),
    default=sorted(data["year"].dropna().unique())
)

filtered = data[
    (data["surface"].isin(surface_filter)) &
    (data["height_group"].isin(height_filter)) &
    (data["year"].isin(year_filter))
]

# =========================
# KPIs
# =========================

st.subheader("Indicadores principales")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Registros", f"{len(filtered):,}")
col2.metric("Jugadores", filtered["player_name"].nunique())
col3.metric("Altura media", round(filtered["height"].mean(), 1))
col4.metric("Aces medios", round(filtered["aces"].mean(), 2))
col5.metric("Primer saque medio", f"{round(filtered['first_serve_pct'].mean(), 2)}%")

st.divider()

# =========================
# PESTAÑAS
# =========================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen ejecutivo",
    "Altura y saque",
    "Superficies",
    "Jugadores",
    "Datos"
])

# =========================
# TAB 1
# =========================

with tab1:
    st.subheader("Visión general del rendimiento del saque")

    col1, col2 = st.columns(2)

    avg_by_height = filtered.groupby("height_group", as_index=False)[
        ["aces", "first_serve_pct", "double_faults"]
    ].mean()

    with col1:
        fig = px.bar(
            avg_by_height,
            x="height_group",
            y="aces",
            title="Aces medios por grupo de altura",
            labels={"height_group": "Grupo de altura", "aces": "Aces medios"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            avg_by_height,
            x="height_group",
            y="first_serve_pct",
            title="Porcentaje medio de primer saque por grupo de altura",
            labels={"height_group": "Grupo de altura", "first_serve_pct": "% primer saque"}
        )
        st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Conclusión inicial: la altura no parece explicar por sí sola el porcentaje de primer saque, "
        "pero sí muestra una relación más clara con la generación de aces."
    )

# =========================
# TAB 2
# =========================

with tab2:
    st.subheader("Análisis de altura y métricas del saque")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            filtered,
            x="height",
            y="first_serve_pct",
            color="surface",
            opacity=0.5,
            title="Altura vs porcentaje de primer saque",
            labels={
                "height": "Altura",
                "first_serve_pct": "% primer saque",
                "surface": "Superficie"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(
            filtered,
            x="height",
            y="aces",
            color="surface",
            opacity=0.5,
            title="Altura vs número de aces",
            labels={
                "height": "Altura",
                "aces": "Aces",
                "surface": "Superficie"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    corr = filtered[["height", "first_serve_pct", "aces", "double_faults"]].corr()

    st.markdown("### Matriz de correlación")

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlación entre altura y métricas del saque",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 3
# =========================

with tab3:
    st.subheader("Comparativa por superficie")

    surface_summary = filtered.groupby("surface", as_index=False).agg(
        aces_medios=("aces", "mean"),
        primer_saque_medio=("first_serve_pct", "mean"),
        dobles_faltas_medias=("double_faults", "mean"),
        registros=("aces", "count")
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            surface_summary,
            x="surface",
            y="aces_medios",
            title="Aces medios por superficie",
            labels={"surface": "Superficie", "aces_medios": "Aces medios"}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(
            surface_summary,
            x="surface",
            y="primer_saque_medio",
            title="Primer saque medio por superficie",
            labels={"surface": "Superficie", "primer_saque_medio": "% primer saque"}
        )
        st.plotly_chart(fig, use_container_width=True)

    height_surface = filtered.groupby(
        ["height_group", "surface"], as_index=False
    )["aces"].mean()

    fig = px.bar(
        height_surface,
        x="height_group",
        y="aces",
        color="surface",
        barmode="group",
        title="Aces medios por grupo de altura y superficie",
        labels={
            "height_group": "Grupo de altura",
            "aces": "Aces medios",
            "surface": "Superficie"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# TAB 4
# =========================

with tab4:
    st.subheader("Ranking de jugadores")

    min_matches = st.slider(
        "Número mínimo de registros por jugador",
        min_value=1,
        max_value=50,
        value=5
    )

    player_summary = filtered.groupby("player_name", as_index=False).agg(
        altura=("height", "mean"),
        registros=("aces", "count"),
        aces_medios=("aces", "mean"),
        primer_saque_medio=("first_serve_pct", "mean"),
        dobles_faltas_medias=("double_faults", "mean")
    )

    player_summary = player_summary[player_summary["registros"] >= min_matches]

    top_aces = player_summary.sort_values("aces_medios", ascending=False).head(15)

    fig = px.bar(
        top_aces,
        x="aces_medios",
        y="player_name",
        orientation="h",
        title="Top 15 jugadores por aces medios",
        labels={
            "aces_medios": "Aces medios",
            "player_name": "Jugador"
        }
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(player_summary.sort_values("aces_medios", ascending=False))

# =========================
# TAB 5
# =========================

with tab5:
    st.subheader("Datos filtrados")

    st.dataframe(filtered)

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Descargar datos filtrados",
        data=csv,
        file_name="datos_filtrados_tenis.csv",
        mime="text/csv"
    )

# =========================
# CONCLUSIÓN FINAL
# =========================

st.divider()

st.markdown("""
### Conclusión general

El análisis muestra que la altura no tiene una relación fuerte con el porcentaje de primeros saques,
pero sí parece estar más relacionada con la generación de aces. Además, la superficie introduce
diferencias importantes en el rendimiento del saque, especialmente en pistas rápidas.
""")
