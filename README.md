# Ultimate Tic-tac-toe
Kahdestaan pelattava [Ultimate Tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe). Ultimate Tic-tac-toe on versio ristinollasta, jossa pelilauta on 9x9 ja edellisen pelaajan siirto määrää seuraavan siirron sallitut ruudut.

Sovelluksessa olevat ominaisuudet:
1. Etusivu kertoo pelin säännöt ja sisältää kaikki olennaiset linkit sovelluksen eri sivuille. 
2. Etusivu sisältää dataa tämänhetkisestä pelaajamäärästä tai aktiivisten pelien määrästä tms. 
3. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
4. Käyttäjä voi lisätä muita käyttäjiä kaverikseen.
5. Käyttäjä voi luoda uuden julkisen tai listalta piilotetun peliaulan.
6. Käyttäjä voi liittyä muiden luomiin peleihin.
7. Aulan luoja voi poistaa käyttäjän aulasta.
8. Aulan omistaja voi luoda peliin liittymistä varten linkin.
9. Aulassa pelaajat voivat lähettää viestejä.
10. Pelatessa pelaajalle näytetään kyseisen vuoron sallitut ruudut 
11. Pelaaja voi sijoittaa ristin/nollan mihin tahansa sallituista ruuduista.
12. Pelilauta päivittyy, kun vastustaja sijoittaa oman ristin/nollan.
13. Pelaajalle ilmoitetaan voitosta tai häviöstä.
14. Käyttäjä voi katsoa omasta pelihistoriasta, kuinka paljon pelejä on voittanut ja hävinnyt.
15. Käyttäjä voi vaihtaa oman salasanan.
14. Käyttäjä voi asettaa oman profiilin näkyvyyden muille käyttäjille.

Sovellus on testattavissa [Herokussa](https://ultimate-tic-tac-toe-test.herokuapp.com/)

Sovelluksen tila 8.10.2022 (9.10.2022):
Siirsin sovelluksen heroku palvelimen eurooppaan ja samalla urlia oli pakko muuttaa. Sovelluksessa on kaikki yllä mainituista ominaisuuksista, mutta käytännössä 14 on hyödytön, koska muiden profiileja ei ole vielä mahdollista katsoa. Sovelluksen koodin laatu ei ole erityisen hyvä (lähinnä pidän sovellusta turhan isona, ja siinä on päällekkäistä koodia). Pahimmat tietoturvaongelmat pitäisi olla korjattu. Sovelluksessa voi kuitenkin monissa paikoissa lähettää käsin pyyntöjä, joita käyttöliittymän lomakkeet tarkoituksella eivät salli. Näin olisi ehkä mahdollista esim. poistaa aula, jota ei omista. Kaverilista olisi hyvä olla automaattisesti päivittyvä, mutta en vielä ehtinyt lisäämään sitä. Sovelluksen automaattisesti päivittyvät sivut (lista peliauloista, peliaulan asetukset, itse peli) on tehty käyttäen server-sent eventtejä flask-sse kirjastolla.

Suunnitellut ominaisuudet:
1. Käyttäjä voi katsella toisen käyttäjän profiilia, jos sen näkyvyys on julkinen.
2. Aulan voi asettaa näkyväksi vain kavereille (on jo sovelluksessa, mutta filtteröinti ei ole toteutettu).
3. Kaverin voi kutsua peliin kaverilistalta, ja kaveri saa kutsusta ilmoituksen.
4. Lisää tilastoja.
5. Paremman näköinen käyttöliittymä.
6. Automaattisesti päivittyvä kaverilista.
