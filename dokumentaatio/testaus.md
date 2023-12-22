# Testausdokumentti

Ohjelmaa on testattu sitä kehittäessä etenkin manuaalisesti tapahtunein järjestelmätason testein. Yksikkö- ja integraatiotestit jäivät vähän viimetippaan mutta niitäkin on tehty.




## Järjestelmätestaus

Sovelluksen järjestelmätestaus toteutettu manuaalisesti.

### Asennus ja konfigurointi

Sovellus on haettu ja sitä on testattu sekä windowsilla, että virtuaalisessa Linux-ympäristössä [käyttöohjeen](https://github.com/kaarleol/ohte-chess/blob/main/dokumentaatio/kayttoohje.md) kuvaamalla tavalla.

Ohjelma ei tallenna paikallisesti mitään, joten tämän pitäisi olla riittävää.

### Toiminnallisuudet
Kaikki määrittelydokumentin ja käyttöohjeen listaamat toiminnallisuudet on käyty läpi käsin. On myös testattu että koodi ottaa huomioon virheelliset käyttäjän syötteet

### Sovellukseen jääneet laatuongelmat

Sovellus ei ota huomioon pattitilannetta eli tilannetta kun pelaajalla ei ole mitään laillisia siirtoja jäljellä. Näissä tilanteissa täytyy tasapeli hoitaa komennolla

Korotus tapahtuu autokorotuksella kuningattareksi, mikä on oikea siirto lähes aina, mutta shakissa yleisesti pelaajalla pitäisi olla vaihtoehto valita jotain muutakin. Tämän voi tarvittaessa toki muuttaa overridaamalla kuningattaren päälle jonkun muun nappulan
