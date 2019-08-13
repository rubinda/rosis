# Stiskanje in čiščenje slik s pomočjo diskretne valčne transformacije 
S pomočjo diskretne valčne transformacije boste izdelali  postopek za stiskanje slik.

S pomočjo poljubne knjižnice izračunajte diskretno valčno transformacijo (DVT) slike. Izberite najprimernejši valček za vašo sliko. Število nivojev dekompozicije določite sami. Dobro preverite, kako so v izhodu DVT-ja zapisane podrobnosti in približki vhodne slike. 

Nad rezultatom DVT uporabite ali trdo ali mehko odstranjevanje motenj in visokih frekvenc ([soft ali hard thresholding](http://www.numerical-tours.com/matlab/denoisingwav_1_wavelet_1d/)), pri čemer testirajte različne pragovne vrednosti odstranjevanja. S pomočjo inverzne DVT spremenjene valčne koeficiente preslikajte nazaj v prostorsko domeno slik in jih primerjajte z originalno  sliko:
1. Testirajte vsaj štiri različne slike, ki naj bodo čimbolj različne. 
2. Vsaki sliki določite optimalni valček (testirajte vsaj tri različne valčke) in optimalen prag rezanja (testirajte vsaj štiri različne pragove rezanja). 
3. Ocenite stopnjo stiskanja in kvaliteto rekonstrukcije s pomočjo inverzne  DVT. Podobnosti oz. odstopanja med originalno in rekonstruirano sliko merite s [korelacijskim koeficientom](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) in normalizirano kvadratično napako ([normalized root-mean-square deviation](https://en.wikipedia.org/wiki/Root-mean-square_deviation#Normalized_root-mean-square_deviation)).
4. Za izbrane pragove rezanja ocenite razliko med mehkim in trdim pragovnim odstranjevanjem motenj. 
5. Postopke testiranja na izbrani sliki (lahko je ena sama) ponovite ob prisotnosti 20 dB belega šuma, ki ga tvorite sami.

V  arhivu ZIP oddajte nove datoteke in poročilo porocilo.pdf, ki naj vsebuje komentirane ključne izseke programske kode,  opis uporabe izbrane knjižnice za delo z valčki (če ste jo uporabili) ter opis testiranja rešitve nad izbranimi slikami.  V poročilu navedite tudi število koeficientov DVT, ki so nad izbrano pragovno vrednostjo in opredelite napako med originalno in rekonstruirano sliko. Oddajte tudi izvorno kodo programskih rešitev, saj se bo na njej vršila avtomatska detekcija plagiatov. Vse skupaj oddajte v arhivu naloga.zip.