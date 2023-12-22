# Testausdokumentti

Ohjelmaa on testattu sitä kehittäessä etenkin manuaalisesti tapahtunein järjestelmätason testein. Yksikkö- ja integraatiotestit jäivät vähän viimetippaan mutta niitäkin on tehty.

## Yksikkö- ja integraatiotestaus

### Sovelluslogiikka

Gameloopista vastaava App testataan TestApp-luokalla. Testaus on toteutettu suurimmaksiosin integraatiotestauksena sen oikeilla palveluilla (Board, Turn, LegalMove) poislukien IO:n josta tehtiin Mock-olio. Lisäksi luokan sisäisten funktioiden haaraumia on testattu yksikkötestauksella samaisessa testiluokassa

### Palvelut

Palveluluokkien Board, LegalMove ja Turn testaus on enimmäkseen toteutettu osana integraatiotestausta App-luokasta. 

Turn on myös yksikkötestattu omalla testiluokalla TestTurn

Myös Board-luokalle on tehty muutama yksikkötesti TestBoard-luokkaan mutta suurin osa testauksesta koostuu integraatiotestauksesta

### Testikattavuus

IO poisluettuna testauksen haaraumakattavuus on 89%

<img width="556" alt="image" src="https://github.com/kaarleol/ohte-chess/assets/127772376/7f390d64-0c24-448b-aa4a-cea3732d4aca">

IO jätettiin pois, sillä se koostui käytännössä vain print- ja input-komennoista. Lisäksi käyttäjälle olisi erittäin selvää jos tulostusta ei tapahtuisi.

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
