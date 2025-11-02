"""Zensus Collector CLI."""

from pathlib import Path

import httpx
import typer
from rich import print as rprint
from rich.progress import Progress, SpinnerColumn, DownloadColumn, TransferSpeedColumn

app = typer.Typer()

# All gitterdaten files from the Zensus 2022 publication page
GITTERDATEN_FILES = [
    ("Zensus2022_Bevoelkerungszahl.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip"),
    ("Deutsche_Staatsangehoerige_ab_18_Jahren.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Deutsche_Staatsangehoerige_ab_18_Jahren.zip"),
    ("Auslaenderanteil_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_in_Gitterzellen.zip"),
    ("Auslaenderanteil_ab_18_Jahren.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_ab_18_Jahren.zip"),
    ("Zensus2022_Geburtsland_Gruppen_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Geburtsland_Gruppen_in_Gitterzellen.zip"),
    ("Zensus2022_Staatsangehoerigkeit_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Staatsangehoerigkeit_in_Gitterzellen.zip"),
    ("Zensus2022_Staatsangehoerigkeit_Gruppen_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Staatsangehoerigkeit_Gruppen_in_Gitterzellen.zip"),
    ("Zahl_der_Staatsangehoerigkeiten.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zahl_der_Staatsangehoerigkeiten.zip"),
    ("Durchschnittsalter_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittsalter_in_Gitterzellen.zip"),
    ("Alter_in_5_Altersklassen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_5_Altersklassen.zip"),
    ("Alter_in_10er-Jahresgruppen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_10er-Jahresgruppen.zip"),
    ("Anteil_unter_18-jaehrige_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_unter_18-jaehrige_in_Gitterzellen.zip"),
    ("Anteil_ab_65-jaehrige_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_ab_65-jaehrige_in_Gitterzellen.zip"),
    ("Alter_in_infrastrukturellen_Altersgruppen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_infrastrukturellen_Altersgruppen.zip"),
    ("Familienstand_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Familienstand_in_Gitterzellen.zip"),
    ("Religion.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Religion.zip"),
    ("Durchschnittliche_Haushaltsgroesse_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Haushaltsgroesse_in_Gitterzellen.zip"),
    ("Zensus2022_Groesse_des_privaten_Haushalts_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Groesse_des_privaten_Haushalts_in_Gitterzellen.zip"),
    ("Typ_der_Kernfamilie_nach_Kindern.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_der_Kernfamilie_nach_Kindern.zip"),
    ("Groesse_der_Kernfamilie.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Groesse_der_Kernfamilie.zip"),
    ("Typ_des_privaren_Haushalts_Lebensform.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_des_privaren_Haushalts_Lebensform.zip"),
    ("Typ_des_privaten_Haushalts_Familien.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_des_privaten_Haushalts_Familien.zip"),
    ("Seniorenstatus_eines_privaten_Haushalts.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Seniorenstatus_eines_privaten_Haushalts.zip"),
    ("Zensus2022_Durchschn_Nettokaltmiete.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Durchschn_Nettokaltmiete.zip"),
    ("Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip"),
    ("Eigentuemerquote_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Eigentuemerquote_in_Gitterzellen.zip"),
    ("Leerstandsquote_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Leerstandsquote_in_Gitterzellen.zip"),
    ("Marktaktive_Leerstandsquote_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Marktaktive_Leerstandsquote_in_Gitterzellen.zip"),
    ("Durchschnittliche_Wohnflaeche_je_Bewohner_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Wohnflaeche_je_Bewohner_in_Gitterzellen.zip"),
    ("Durchschnittliche_Flaeche_je_Wohnung_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Flaeche_je_Wohnung_in_Gitterzellen.zip"),
    ("Flaeche_der_Wohnung_10m2_Intervalle.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Flaeche_der_Wohnung_10m2_Intervalle.zip"),
    ("Wohnungen_nach_Gebaeudetyp_Groesse.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Gebaeudetyp_Groesse.zip"),
    ("Wohnungen_nach_Zahl_der_Raeume.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Zahl_der_Raeume.zip"),
    ("Gebaeude_nach_Baujahr_Jahrzehnte.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahr_Jahrzehnte.zip"),
    ("Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip"),
    ("Gebaeude_nach_Anzahl_der_Wohnungen_im_Gebaeude.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Anzahl_der_Wohnungen_im_Gebaeude.zip"),
    ("Gebaeude_mit_Wohnraum_nach_Gebaeudetyp_Groesse.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_Gebaeudetyp_Groesse.zip"),
    ("Zensus2022_Heizungsart.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Heizungsart.zip"),
    ("Gebaeude_mit_Wohnraum_nach_ueberwiegender_Heizungsart.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_ueberwiegender_Heizungsart.zip"),
    ("Zensus2022_Energietraeger.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Energietraeger.zip"),
    ("Gebaeude_mit_Wohnraum_nach_Energietraeger_der_Heizung.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_Energietraeger_der_Heizung.zip"),
    ("Gebaeude_nach_Baujahresklassen_in_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahresklassen_in_Gitterzellen.zip"),
    ("Auslaenderanteil_EU_nichtEU_Gitterzellen.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_EU_nichtEU_Gitterzellen.zip"),
    ("Shapefile_Zensus2022.zip", "https://www.destatis.de/static/DE/zensus/gitterdaten/Shapefile_Zensus2022.zip"),
]


@app.command()
def download_gitterdaten(
    output_dir: Path = typer.Option(
        Path("./data/gitterdaten"),
        "--output-dir",
        "-o",
        help="Directory to save downloaded files",
    ),
    skip_existing: bool = typer.Option(
        True,
        "--skip-existing/--overwrite",
        help="Skip files that already exist",
    ),
) -> None:
    """Download all Zensus 2022 gitterdaten (grid data) files."""
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    rprint(f"[cyan]Downloading {len(GITTERDATEN_FILES)} gitterdaten files to {output_dir}[/cyan]")

    downloaded = 0
    skipped = 0
    failed = 0

    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        DownloadColumn(),
        TransferSpeedColumn(),
    ) as progress:
        for filename, url in GITTERDATEN_FILES:
            output_path = output_dir / filename

            # Skip if file exists and skip_existing is True
            if output_path.exists() and skip_existing:
                rprint(f"[yellow]⊘ Skipping {filename} (already exists)[/yellow]")
                skipped += 1
                continue

            task = progress.add_task(f"[cyan]Downloading {filename}...", total=None)

            try:
                with httpx.stream("GET", url, follow_redirects=True, timeout=60.0) as response:
                    response.raise_for_status()
                    total = int(response.headers.get("content-length", 0))
                    progress.update(task, total=total)

                    with open(output_path, "wb") as f:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))

                progress.update(task, description=f"[green]✓ {filename}")
                downloaded += 1

            except Exception as e:
                progress.update(task, description=f"[red]✗ {filename} (error)")
                rprint(f"[red]Error downloading {filename}: {e!s}[/red]")
                failed += 1

            progress.remove_task(task)

    rprint("\n[bold cyan]Download Summary:[/bold cyan]")
    rprint(f"  [green]✓ Downloaded: {downloaded}[/green]")
    rprint(f"  [yellow]⊘ Skipped: {skipped}[/yellow]")
    rprint(f"  [red]✗ Failed: {failed}[/red]")


@app.command()
def main(name: str = "Chell") -> None:
    """Fire portal gun."""
