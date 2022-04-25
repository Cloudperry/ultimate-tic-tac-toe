# Ultimate Tic-tac-toe
Kahdestaan pelattava [Ultimate Tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe). Ultimate Tic-tac-toe on versio ristinollasta, jossa pelilauta on 9x9 ja edellisen pelaajan siirto määrää seuraavan siirron sallitut ruudut.

Sovelluksen ominaisuudet:
1. Etusivu kertoo pelin säännöt ja sisältää kaikki olennaiset linkit sovelluksen eri sivuille. 
2. Etusivu sisältää dataa tämänhetkisestä pelaajamäärästä tai aktiivisten pelien määrästä tms. 
3. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
4. Käyttäjä voi lisätä muita käyttäjiä kaverikseen.
5. Käyttäjä voi luoda uuden julkisen tai vain kavereille näkyvän peliaulan sekä liittyä muiden luomiin peleihin joko katsojana tai pelaajana.
6. Aulan luoja voi poistaa käyttäjän aulasta tai antaa aulan toiselle käyttäjälle.
7. Aulan omistaja voi luoda peliin liittymistä varten linkin.
8. Aulassa pelaajat voivat lähettää viestejä.
9. Pelatessa pelaajalle näytetään kyseisen vuoron sallitut ruudut ja pelaaja voi sijoittaa ristin/nollan haluamaansa ruutuun.
10. Pelilauta päivittyy, kun vastustaja sijoittaa oman ristin/nollan.
11. Käyttäjä voi katsoa omasta pelihistoriasta kuinka paljon pelejä on voittanut ja hävinnyt sekä joitain perustilastoja.
12. Käyttäjä voi vaihtaa oman salasanan ja asettaa oman pelihistorian/tilastojen näkyvyyden muille käyttäjille.

Sovellus on testattavissa [Herokussa](https://tsoha-ultimate-tic-tac-toe.herokuapp.com/)

Sovelluksen tila 24.4.2022:
Korvasin ominaisuudessa 5 peliaulan pääsykoodin mahdollisuudella asettaa aulan näkyväksi vain kavereille. Tein tietokantaan melko paljon muutoksia, ja samalla loin kaikki taulut uudestaan. Ominaisuuksista 1, 2, 3, 4, 11 ja 12 on toteutettu. Ominaisuutta 11 ei voi testata herokussa luoduilla tileillä, koska pelinäkymää/tilastojen tallentamista ei ole vielä toteutettu. Sitä voi kuitenkin testata käyttäjätilillä Roni1, jonka salasana on 123 (lisäsin sen pelihistoriatauluun käsin pelejä). Ominasuudet 5, 6 ja 7 on suunniteltu tosi pitkälle asti ja niiden perustoteutuksessa kestäisi n. muutama tuntia. Ominaisuuksien 8, 9 ja 10 toteutus voi olla hieman hankalampaa, mutta luulisin niiden ensimmäisten versioiden valmistuvan ensi viikon aikana. Saatan lisätä kaverilistaan vielä ominaisuuksia, kuten esim. kaverin kutsumisen peliin. Isoin sovelluksessa tällä hetkellä oleva ongelma on, että virheviestejä näyttävillä sivuilla viestin tultua sivun päivittäminen aiheuttaa lomakkeenn uudelleenlähetyksen (johtuu render_template kutsusta post pyynnössä). Olen miettinyt ratkaisun tähän ongelmaan ja se on ensimmäinen asia, jonka teen jatkaessani sovelluksen tekoa. Jos dynaamisessa pelinäkymässä tulee hankaluuksia, löysin tavan päivittää sivua tietyin väliajoin pelkällä javascriptillä (sen avulla sivun ei täytyisi olla dynaaminen). Alunperin tavoitteena tähän välipalautukseen oli saada tehtyä kaikki ominaisuudet paitsi 9 ja 10, mutta aloitin tekemisen niin myöhään, että en ehtinyt tekemään ihan niin paljon. Ominaisuuksiin 9 ja 10 liittyen ehdin suunnitella Websocket protokollaa ja käyttöliittymää jonkin verran, mutta muuta niihin liittyvää en ole tehnyt vielä.
