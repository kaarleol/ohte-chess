## Ohjelmistotekniikka, harjoitustyö

# ohte-chess

Harjoitustyön aihe on kahden henkilön pelattava shakki. Tällä hetkellä sovellus on avattavissa komentorivillä ja sinne piirretään kuvaa shakkilaudasta.

[Vaatimusmaarittely](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Työaikakirjanpito](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/tyoaikakirjanpito.md)

[Changelog](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/changelog.md)

[Uusin release](https://github.com/kaarleol/ohte-chess/releases/tag/1.0.0)
## Asennus

1. Asenna riippuvuudet ohte-chess-kansiossa komennolla:

```bash
poetry install
```

2. Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Komentorivitoiminnot

### Ohjelman suorittaminen

Ohjelman pystyy suorittamaan komennolla:

```bash
poetry run invoke start
```

### Testaus

Testit suoritetaan komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Raportti generoituu _htmlcov_-hakemistoon.

### Pylint

Tiedoston [.pylintrc](./.pylintrc) määrittelemät tarkistukset voi suorittaa komennolla:

```bash
poetry run invoke lint
```

### Pelin sisällä

Poistu pelistä:

```bash
exit
```

Listaus komennoista:

```bash
help
```

Peru nappulan valinta:

```bash
cancel
```

Uusi peli:

```bash
new
```

Tasapeli:

```bash
draw
```

Luovuta:

```bash
resign
```

Tee muutoksia lautaan pelin tilasta välittämättä:

```bash
override
```

