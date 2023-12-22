### Käyttöohje

Lataa projektin viimeisimmän [releasen](https://github.com/kaarleol/ohte-chess/releases/tag/1.0.0) lähdekoodi githubin Assets osion alta Source code

Siirry ladatuissa tiedostoissa ohte-chess -kansioon, joka sisältää itse sovelluksen.

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

Siirtoja voi tehdä shakin sääntöjä noudattamalla kirjaamalla lähtöruudun ja sen jälkeen maaliruuddun

```bash
d2
```
```bash
d4
```
