# DFT

Izdelajte program, ki oceni odvisnost amplitude zvoka od razdalje izvora zvoka od mikrofona. Omogočite tudi zajem v stereo načinu in ocenite  časovne razlike med signaloma v levem in desnem kanalu pri različnih postavitvah izvora zvoka glede na mikrofon. Analizirajte vsaj štiri razdalje (npr. 1 m, 2 m, 3 m, 4 m – več je bolje) in vsaj štiri kote (npr. - Π/4, 0, Π/4, Π/2), ki jih daljica med izvorom in središčem mikrofona v vodoravni ravnini oklepa s pravokotnico na os, ki povezuje oba mikrofona (oba kanala). Pri tem lahko privzamete, da je izvor zvoka v isti višini kot mikrofon. 

Izdelan program preizkusite na lastnih zvočnih posnetkih konstantnega nekaj sekund dolgega žvižga (en sam ton s konstantno jakostjo). Signal posnemite sami, nato pa ga lahko zaradi zagotavljanja konstantnosti amplitude predvajate na mobilnem telefonu oz. drugem računalniku.  

Odgovorite na naslednja vprašanja:
 + Kako konstanta je amplitude vašega žvižganja pri konstantni razdalji izvora zvoka od mikrofona?
 + Koliko frekvenc je dejansko prisotnih v vašem žvižgu?
 + Kako se z razdaljo izvora spreminja amplituda konstantnega žvižga?
 + Kakšna je razlika med absolutno vrednostjo realnega posnetka zvoka (npr. abs(zvok) ) in absolutno vrednostjo analitičnega zapisa zvoka, ki ga iz realnega zvoka pridobimo s pomočjo Hilbertove transformacije (Hilbert transfrom), npr  abs(hilbert(zvok)))?
 + Ali lahko iz amplitude žvižga ocenite smer prihoda zvoka v mikrofon in kakšna je natančnost določitve pozicije izvora zvoka v prostoru?
 + Ali lahko iz razlike zakasnitev signalov v obeh kanalih ocenite smer zvoka in kaj za to potrebujete?
 + S kakšnim faznim zamikom bi prispel zvok v mikrofon, če predpostavimo, da je hitrost širjenja zvoka po zraku pri hišni temperaturi enaka 343 m/s? Kakšno prostorsko ločljivost omogoča analiza faznega zamika in od česa vse je ta ločljivost odvisna?