## Ohjelmistotekniikka, harjoitustyö

# ohte-chess

Harjoitustyön aihe on kahden henkilön pelattava shakki. Tällä hetkellä sovellus on avattavissa komentorivillä ja sinne piirretään kuvaa shakkilaudasta.

[Vaatimusmaarittely](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/vaatimusmaarittely.md)

[Työaikakirjanpito](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/tyoaikakirjanpito.md)

[Changelog](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/changelog.md)

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
