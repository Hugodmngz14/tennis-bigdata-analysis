# Análisis Big Data de Tenis

## Descripción del proyecto
Este proyecto analiza la relación entre la altura de los jugadores y distintas métricas relacionadas con el saque en el tenis profesional ATP.

El proyecto incluye:
- Pipeline ETL
- Limpieza y transformación de datos
- Modelo dimensional
- Análisis SQL
- Consultas analíticas con PySpark
- Análisis exploratorio de datos (EDA)

---

## Tecnologías utilizadas
- Python
- Pandas
- SQLite
- PySpark
- Google Colab
- Seaborn
- Matplotlib

---

## Fuente de datos
Dataset ATP de Jeff Sackmann:
https://github.com/JeffSackmann/tennis_atp

---

## Objetivos principales
- Analizar si la altura influye en el rendimiento del saque
- Estudiar la generación de aces según grupos de altura
- Comparar el rendimiento del saque según la superficie
- Construir un modelo dimensional tipo Data Warehouse
- Realizar consultas analíticas usando PySpark

---

## Principales conclusiones
- La altura presenta una correlación débil con el porcentaje de primer saque
- Los jugadores más altos tienden a generar más aces
- El tipo de superficie influye significativamente en el rendimiento del saque
- Las pistas de hierba favorecen más a los grandes sacadores

---

## Estructura del repositorio

```text
01_eda_inicial.ipynb
02_etl_pipeline_final.ipynb
03_pyspark_cubo_colab.ipynb

dim_player.csv
dim_surface.csv
dim_time.csv
dim_tournament.csv
```

---

## Nota sobre la tabla FACT

El archivo `fact_serve.csv` no se incluye en el repositorio debido a limitaciones de tamaño.

Puede regenerarse ejecutando el notebook:

`02_etl_pipeline_final.ipynb`
