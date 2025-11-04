#: Name of the application
APP_NAME = "zensus2pgsql"

#: All available data files
GITTERDATEN_FILES = (
    {
        "name": "bevoelkerungszahl",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip",
    },
    {
        "name": "deutsche_staatsangehoerige_ab_18_jahren",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Deutsche_Staatsangehoerige_ab_18_Jahren.zip",
    },
    {
        "name": "auslaenderanteil",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_in_Gitterzellen.zip",
    },
    {
        "name": "auslaenderanteil_ab_18_jahren",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_ab_18_Jahren.zip",
    },
    {
        "name": "geburtsland_gruppen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Geburtsland_Gruppen_in_Gitterzellen.zip",
    },
    {
        "name": "staatsangehoerigkeit",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Staatsangehoerigkeit_in_Gitterzellen.zip",
    },
    {
        "name": "staatsangehoerigkeit_gruppen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Staatsangehoerigkeit_Gruppen_in_Gitterzellen.zip",
    },
    {
        "name": "zahl_der_staatsangehoerigkeiten",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zahl_der_Staatsangehoerigkeiten.zip",
    },
    {
        "name": "durchschnittsalter",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittsalter_in_Gitterzellen.zip",
    },
    {
        "name": "alter_in_5_altersklassen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_5_Altersklassen.zip",
    },
    {
        "name": "alter_in_10er_jahresgruppen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_10er-Jahresgruppen.zip",
    },
    {
        "name": "anteil_unter_18_jaehrige",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_unter_18-jaehrige_in_Gitterzellen.zip",
    },
    {
        "name": "anteil_ab_65_jaehrige",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_ab_65-jaehrige_in_Gitterzellen.zip",
    },
    {
        "name": "alter_in_infrastrukturellen_altersgruppen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_in_infrastrukturellen_Altersgruppen.zip",
    },
    {
        "name": "familienstand",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Familienstand_in_Gitterzellen.zip",
    },
    {
        "name": "religion",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Religion.zip",
    },
    {
        "name": "durchschnittliche_haushaltsgroesse",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Haushaltsgroesse_in_Gitterzellen.zip",
    },
    {
        "name": "groesse_des_privaten_haushalts",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Groesse_des_privaten_Haushalts_in_Gitterzellen.zip",
    },
    {
        "name": "typ_der_kernfamilie_nach_kindern",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_der_Kernfamilie_nach_Kindern.zip",
    },
    {
        "name": "groesse_der_kernfamilie",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Groesse_der_Kernfamilie.zip",
    },
    {
        "name": "typ_des_privaren_haushalts_lebensform",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_des_privaren_Haushalts_Lebensform.zip",
    },
    {
        "name": "typ_des_privaten_haushalts_familien",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Typ_des_privaten_Haushalts_Familien.zip",
    },
    {
        "name": "seniorenstatus_eines_privaten_haushalts",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Seniorenstatus_eines_privaten_Haushalts.zip",
    },
    {
        "name": "durchschn_nettokaltmiete",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Durchschn_Nettokaltmiete.zip",
    },
    {
        "name": "durchschnittliche_nettokaltmiete_und_anzahl_der_wohnungen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip",
    },
    {
        "name": "eigentuemerquote",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Eigentuemerquote_in_Gitterzellen.zip",
    },
    {
        "name": "leerstandsquote",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Leerstandsquote_in_Gitterzellen.zip",
    },
    {
        "name": "marktaktive_leerstandsquote",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Marktaktive_Leerstandsquote_in_Gitterzellen.zip",
    },
    {
        "name": "durchschnittliche_wohnflaeche_je_bewohner",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Wohnflaeche_je_Bewohner_in_Gitterzellen.zip",
    },
    {
        "name": "durchschnittliche_flaeche_je_wohnung",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Flaeche_je_Wohnung_in_Gitterzellen.zip",
    },
    {
        "name": "flaeche_der_wohnung_10m2_intervalle",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Flaeche_der_Wohnung_10m2_Intervalle.zip",
    },
    {
        "name": "wohnungen_nach_gebaeudetyp_groesse",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Gebaeudetyp_Groesse.zip",
    },
    {
        "name": "wohnungen_nach_zahl_der_raeume",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Wohnungen_nach_Zahl_der_Raeume.zip",
    },
    {
        "name": "gebaeude_nach_baujahr_jahrzehnte",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahr_Jahrzehnte.zip",
    },
    {
        "name": "gebaeude_nach_baujahr_in_mikrozensus_klassen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahr_in_Mikrozensus_Klassen.zip",
    },
    {
        "name": "gebaeude_nach_anzahl_der_wohnungen_im_gebaeude",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Anzahl_der_Wohnungen_im_Gebaeude.zip",
    },
    {
        "name": "gebaeude_mit_wohnraum_nach_gebaeudetyp_groesse",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_Gebaeudetyp_Groesse.zip",
    },
    {
        "name": "heizungsart",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Heizungsart.zip",
    },
    {
        "name": "gebaeude_mit_wohnraum_nach_ueberwiegender_heizungsart",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_ueberwiegender_Heizungsart.zip",
    },
    {
        "name": "energietraeger",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Energietraeger.zip",
    },
    {
        "name": "gebaeude_mit_wohnraum_nach_energietraeger_der_heizung",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_mit_Wohnraum_nach_Energietraeger_der_Heizung.zip",
    },
    {
        "name": "gebaeude_nach_baujahresklassen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Gebaeude_nach_Baujahresklassen_in_Gitterzellen.zip",
    },
    {
        "name": "auslaenderanteil_eu_nichteu_gitterzellen",
        "url": "https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_EU_nichtEU_Gitterzellen.zip",
    },
)
