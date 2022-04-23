# Ultimate Tic-tac-toe
Kahdestaan pelattava [Ultimate Tic-tac-toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe). Ultimate Tic-tac-toe on versio ristinollasta, jossa pelilauta on 9x9 ja edellisen pelaajan siirto määrää seuraavan siirron sallitut ruudut.

Sovelluksen ominaisuudet:
1. Etusivu kertoo pelin säännöt ja sisältää kaikki olennaiset linkit sovelluksen eri sivuille. 
2. Etusivu sisältää dataa tämänhetkisestä pelaajamäärästä tai aktiivisten pelien määrästä tms. 
3. Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
4. Käyttäjä voi lisätä muita käyttäjiä kaverikseen.
5. Käyttäjä voi luoda uuden peliaulan pääsykoodilla tai ilman sekä liittyä muiden luomiin peleihin joko katsojana tai pelaajana.
6. Aulan luoja voi poistaa käyttäjän aulasta tai antaa aulan toiselle käyttäjälle.
7. Aulan omistaja voi luoda peliin liittymistä varten linkin.
8. Aulassa pelaajat voivat lähettää viestejä.
9. Pelatessa pelaajalle näytetään kyseisen vuoron sallitut ruudut ja pelaaja voi sijoittaa ristin/nollan haluamaansa ruutuun.
10. Pelilauta päivittyy, kun vastustaja sijoittaa oman ristin/nollan.
11. Käyttäjä voi katsoa omasta pelihistoriasta kuinka paljon peleja on voittanut ja hävinnyt sekä joitain perustilastoja.
12. Käyttäjä voi vaihtaa oman salasanan ja asettaa oman pelihistorian/tilastojen näkyvyyden muille käyttäjille.

Sovellus on testattavissa [Herokussa](https://tsoha-ultimate-tic-tac-toe.herokuapp.com/)

Sovelluksen tila 4.4.2022:  
Ominaisuuksista 1 ja 3 on toteutettu. Sovelluksen teossa tuli jonkin verran hankaluuksia vastaan, koska tajusin pelinäkymän päivittämisen pelimerkkejä sijoitettaessa olevan mahdotonta pelkällä Flaskilla (staattisilla sivuilla). Päivittämiseen voisin käyttää joko Websocketteja tai Server-sent eventtejä. Tällä hetkellä suunnitelma on käyttää pelinäkymään [tätä ui kirjastoa](https://github.com/treeform/fidget) ja käyttää Websocketteja [tällä kirjastolla](https://github.com/stisa/jswebsockets). En haluaisi käyttää Javascriptiä/HTML:ää, koska en osaa niitä enkä pidä Javascriptistä. Testasin edellä mainitun ui kirjaston toimivuuden selaimessa ja testaan seuraavaksi Websocket kirjastoa Flaskin kanssa. Tarkoituksena olisi siis päivittää pelilautaa dynaamisesti (lataamatta sivua uudelleen) Websocket viestin tullessa. Pelilogiikan ajattelin laittaa kuitenkin palvelimen puolelle huijaamisen estämiseksi. Pelinäkymän lisäksi saattaisin tehdä kaverilistan ja peliaulanäkymän jollain dynaamista päivitystä tukevalla teknologialla. (Sovelluksen teko hidastui myös, koska sain koronan.) Päätin myös, että en varastoi pelin tilaa tietokannassa (katso schema.sql kommentti). Onkohan tämä hyvä idea?
