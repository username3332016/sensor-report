"""Interface en ligne de commande (click)."""
import click

from sensor_report import __version__
from sensor_report.analysis import find_anomalies, load_readings, summary_by_sensor
from sensor_report.plotting import plot_daily_temperature


def read_or_exit(path):
    """Charge le fichier et affiche une erreur claire si le CSV est invalide."""
    try:
        return load_readings(path)
    except ValueError as error:
        raise click.ClickException(str(error))


@click.group()
@click.version_option(__version__, prog_name="sensor-report")
def main():
    """Analyse de mesures de capteurs à partir d'un fichier CSV."""


@main.command()
@click.argument("csv_file", type=click.Path(exists=True, dir_okay=False))
def summary(csv_file):
    """Affiche des statistiques par capteur."""
    df = read_or_exit(csv_file)
    click.echo(summary_by_sensor(df).to_string())


@main.command()
@click.argument("csv_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--column", default="temperature", show_default=True,
              type=click.Choice(["temperature", "humidity"]),
              help="Grandeur à analyser.")
@click.option("--threshold", default=3.0, show_default=True,
              help="Seuil du z-score au-delà duquel une mesure est anormale.")
def anomalies(csv_file, column, threshold):
    """Liste les mesures anormales (z-score élevé)."""
    df = read_or_exit(csv_file)
    found = find_anomalies(df, column, threshold)
    if found.empty:
        click.echo("Aucune anomalie trouvée.")
    else:
        click.echo(found.to_string(index=False))


@main.command()
@click.argument("csv_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--output", "-o", default="report.png", show_default=True,
              help="Nom de l'image à créer.")
def plot(csv_file, output):
    """Crée un graphique de la température moyenne par jour."""
    df = read_or_exit(csv_file)
    plot_daily_temperature(df, output)
    click.echo("Graphique enregistré dans " + output)
