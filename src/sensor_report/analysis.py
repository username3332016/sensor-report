"""Fonctions d'analyse des mesures (pandas)."""
import pandas as pd

# Colonnes obligatoires dans le fichier CSV
REQUIRED_COLUMNS = ["timestamp", "sensor_id", "temperature", "humidity"]


def load_readings(path):
    """Lit le CSV et renvoie un DataFrame propre (dates converties, lignes invalides retirées)."""
    df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Colonnes manquantes dans le CSV : " + ", ".join(missing))

    # Conversion des dates ; les dates illisibles deviennent NaT puis sont retirées
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # Idem pour les nombres : une valeur non numérique devient NaN
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")

    df = df.dropna(subset=["timestamp", "sensor_id"])
    return df.sort_values("timestamp").reset_index(drop=True)


def summary_by_sensor(df):
    """Statistiques (nombre, moyenne, min, max) de chaque capteur."""
    grouped = df.groupby("sensor_id")
    result = grouped.agg(
        mesures=("timestamp", "count"),
        temp_moy=("temperature", "mean"),
        temp_min=("temperature", "min"),
        temp_max=("temperature", "max"),
        hum_moy=("humidity", "mean"),
    )
    return result.round(2)


def find_anomalies(df, column, threshold=3.0):
    """Renvoie les mesures dont le z-score (par capteur) dépasse le seuil."""
    if column not in ("temperature", "humidity"):
        raise ValueError("La colonne doit être 'temperature' ou 'humidity'.")

    anomalies = []
    for sensor, group in df.groupby("sensor_id"):
        values = group[column].dropna()
        std = values.std()
        # Si l'écart-type est nul ou inconnu, on ne peut pas calculer de z-score
        if pd.isna(std) or std == 0:
            continue
        zscores = (values - values.mean()) / std
        outliers = group.loc[zscores[zscores.abs() > threshold].index]
        anomalies.append(outliers)

    if not anomalies:
        return df.iloc[0:0]
    return pd.concat(anomalies).sort_values("timestamp")


def daily_mean(df, column="temperature"):
    """Moyenne journalière de la colonne choisie, pour chaque capteur."""
    tmp = df.copy()
    tmp["jour"] = tmp["timestamp"].dt.date
    return tmp.groupby(["jour", "sensor_id"])[column].mean().unstack()
