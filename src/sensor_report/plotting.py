"""Création du graphique avec matplotlib."""
import matplotlib

matplotlib.use("Agg")  # pas de fenêtre : on enregistre seulement dans un fichier
import matplotlib.pyplot as plt

from sensor_report.analysis import daily_mean


def plot_daily_temperature(df, output_path):
    """Trace la température moyenne par jour pour chaque capteur et enregistre l'image."""
    means = daily_mean(df, "temperature")

    fig, ax = plt.subplots(figsize=(8, 4))
    for sensor in means.columns:
        ax.plot(means.index, means[sensor], marker="o", label=str(sensor))

    ax.set_title("Température moyenne par jour")
    ax.set_xlabel("Jour")
    ax.set_ylabel("Température (°C)")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
