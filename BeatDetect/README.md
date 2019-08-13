# Detekcija ritma v glasbi
S pomočjo diskretne valčne transformacije boste izdelali  postopek za detekcijo ritma basov v glasbi. Postopek detekcije ritma se bo izvajal paketno (ang. ofline), po pritisku na poseben gumb, saj je postopek obdelave za procesno enoto dokaj zahteven. 

Postopek detekcije ritma je povzet po opisu v članku Musical Genre Classification of Audio Signals, v 3. poglavju (Feature Extraction), podpoglavje C. Sestoji iz naslednjih korakov:

## 1. Odstranjevanje drugega kanala v primeru stereo zapisa

## 2. Izračun diskretne valčne transformacije nad signalom
S pomočjo poljubne knjižnice izračunajte diskretno valčno transformacijo (DVT) signala. Uporabite Daubechies-ev valček 4. stopnje ('db4'). Število nivojev dekompozicije določite sami, pazite le, da boste z izbranim nivojem dobro zaznali base v glasbi. Dobro preverite, kako so v izhodu DVT-ja zapisani izhodni signali (podrobnosti in približek vhodnega signala). Izhodne signale prevzorčite nazaj  na osnovno vzorčevalno frekvenco.

>Za DVT niti ne potrebujete knjižnice. Za posamezen valček potrebujete le koeficinete visokih in nizkih filtrov valčka. Tvorite jih lahko npr. s pomočjo matlabove funkcije wfilters('ime_valčka'), kjer je ime_valčka npr 'db4', 'haar' itd.  
```[LO_D,HI_D,LO_R,HI_R] = wfilters('db2')
LO_D =      -0.13          0.22          0.84          0.48
HI_D =      -0.48          0.84         -0.22         -0.13
LO_R =       0.48          0.84          0.22         -0.13
HI_R =      -0.13         -0.22          0.84         -0.48
```
>Z zgoraj podanimi koeficienti filtrov LO_D in HI_D lahko prvi nivo dekompozicije z DVT zapišemo s for zanko:
```matlab
for( n = 0; n < N/2; n++ )
  {
    yh[n] = x[2n+0]*HI_D[3] + x[2n+1]*HI_D[2] + x[2n+2]*HI_D[1] + x[2n+3]*HI_D[0];
    yl[n] = x[2n+0]*LO_D[3] + x[2n+1]*LO_D[2] + x[2n+2]*LO_D[1] + x[2n+3]*LO_D[0];
  }
```
>kjer je x vhodni signal, yh podrobnosti signala po prvi stopnji DVT in yl približek signala po prvi stopnji DVT. N je število vzorcev signala x. Bolj podroben opis zgoraj podane implementacije najdete tukaj. Matlabovo kodo, ki DVT implementira s pomočjo for zanke in valčkom db4 najdete tukaj. 

Izberite **EN SAM** izhodni signal (podrobnosti ali približek na "določeni" stopnji) - tisti, ki najbolje kodira ritem v glasbi. Ne pozabite na stopnjo podvzorčenja  izhodnega signala DVT (v primerjavi z osnovno vzorčevalno frekvenco)! 

## 3. Izračun enostavne ovojnice
Za izbran izhodni signal izračunajte enostavno ovojnico (implementirajte funkcijo y=ovojnica(signal)), ki sestoji iz naslednjih korakov:
    
### 3.1 Izračun absolutne vrednosti signala
Vsem vzorcem v signalu pripišemo pozitivni predznak: `z[n] = abs(y[n])`.  

### 3.2 Filtriranje ovojnice z nizkoprepustnim enopolnim filtrom
`w[n] = (1-a)z[n] + aw[n-1]`, kjer je `a=0.99`. S tem zgladimo ovojnico.

### 3.3 Podvzorčenje ovojnice 
`w[n] = w[Factor*n]`, kjer je navadno `Factor=16`. S tem pohitrimo kasnješe korake algoritma.

### 3.4 Odstranitev srednje vrednosti
Od signala odštejemo njegovo srednjo vrednost (mean).

## 4. Izračun ritma

Z namenom, da bi zajeli dinamiko ritma, bomo korake od 4.1 do 4.3 izvedli na pet sekund dolgih odsekih ovojnice. V ta namen bomo najprej obdelali prvih 5 sekund ovojnice (t.j. izvedli bomo vse korake 4.1-4.3 na odseku od 0. do 5. sekunde ovojnice), nato pa se bomo  pomaknili za eno sekundo naprej in obdelali naslednji pet-sekundni interval (t.j. izvedli bomo vse korake od 4.1 do 4.3 nad intervalom od 1. do 6. sekunde). Ta postopek bomo ponavljali do konca glasbenega posnetka.  

w = izbran odsek ovojnice. 

### 4.1 Izračun avtokorelacije ovojnice
S pomočjo avtokorelacije odseka ovojnice w bomo dobili trenutke udarcev (beats) v obravnavanem zvočnem signalu (udarci so predstavljeni z vrhovi v avtokorelaciji odseka ovojnice). Za zgled lahko uporabite matlabovo funkcijo xcorr (preberite matlabovo pomoč). Pri izračunu autokorelacije si lahko pomagate tudi z naslednjim implementacijskim trikom (zapisano v notaciji matlaba): 
```matlab
w_corr = ifft(abs(fft(w)).^2));
w_corr = w_corr(1:2*Fsamp/Factor); % Fsamp - frekvenca vzorčenja, Factor - faktor podvzorčenja iz koraka 3.3
```
kjer je abs(w) funkcija, ki vrne vektor absolutnih vrednosti posameznih elementov vhodnega kompleksnega vektorja w, operacija  w.^2 pa izračuna vektor kvadratov posameznih elementov kompleksnega vektorja w (preverite ukaza v matlabu ali octave).  Prav tako je priporočljivo, da iz izračunane avtokorelacije odstranimo vrhe, ki so zelo majhni (npr. manjši od 1/40 maksimalnega vrha).

### 4.2. Iskanje vrhov
Maksimumi v avtokoreliranem signalu w_corr predstavljajo trenutke "udarcev" ritma. Pri iskanju maksimumov je priporočljivo določiti tudi minimalno razdaljo med sosednjima maksimumoma, ki predstavlja zgornjo dopustno mejo ritma. Ta naj bo v našem primeru okoli 5 udarcev na sekundo (5 Hz).

### 4.3. Izračun ritma celega signala s pomočjo povprečenja časovnih razlik med sosednjimi vrhovi v w_corr
V zadnjem koraku s pomočjo časovni razlik med sosednjimi udarci (maksimumi) v w_corr izračunamo povprečen ritem za izbrani odsek ovojnice. V izhodno polje hranimo tako trenutni ritem, kot tudi časovno pozicijo odseka ovojnice (v sekundah). Ne pozabite kompenzirati podvzorčenje iz koraka 3.3!

Rezultat postopka naj bo izrisan graf, ki prikazuje ritem glasbe/posnetka v odvisnosti od časa (na celem zvočnem signalu!). Ne pozabite na oznake osi (x os "čas (s)", y os "udarci na minuto" )! 
Beats per minute

Postopek poskusite na primeru zvočnega izseka pesmi Staying Alive skupine Bee Gees, ki predstavlja šolski primer konstantnega ritma. Rezultat je konstanten ritem okoli 103 bpm (udarcev na minuto).