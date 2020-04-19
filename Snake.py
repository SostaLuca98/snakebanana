###############################################################################
# Inizio Codice
###############################################################################

## \todo: fullscreen
## \todo: rendere i livelli indipendenti
## \todo: pausa
## \todo: creare nemiki
## \todo: selezionare e creare livelli

import random
import pygame
import sys
import time
import os
from pygame.locals import *

## 1000 tick = 1000 millisecondi = 1 secondo



###############################################################################
# Impostazioni Generali di Gioco
###############################################################################



## Impostazioni Generali Manuali
FPS                  = 20    # velocita' di gioco
ALTEZZAFINESTRA      = 600   # altezza   finestra (600 per gioco a livelli)
LUNGHEZZAFINESTRA    = 1000  # lunghezza finestra (1000 per gioco a livelli)
DIMENSIONECELLE      = 20    # dimensione celle
BORDI                = False # presenza bordi
LIVELLI              = True  # presenza livelli
LABIRINTI            = 15    # livelli presenti
SUPERAMENTO          = 3    # punteggio per passare di livello
VITE                 = 5     # vite nel gioco a livelli

## Impostazioni Automatiche
assert BORDI == False   or LIVELLI == False    , "Non puoi usare sia i Bordi che i Livelli"
assert LUNGHEZZAFINESTRA % DIMENSIONECELLE == 0, "La Lunghezza della Finestra deve essere un multiplo della grandezza delle celle"
assert ALTEZZAFINESTRA   % DIMENSIONECELLE == 0, "L'Altezza    della Finestra deve essere un multiplo della grandezza delle celle"
CELLEORIZZONTALI = int(LUNGHEZZAFINESTRA / DIMENSIONECELLE)
CELLEVERTICALI = int(ALTEZZAFINESTRA / DIMENSIONECELLE)


## Colori Rosso Verde Blu
BIANCO       = (255, 255, 255)
NERO         = (  0,   0,   0)
ROSSO        = (255,   0,   0)
VERDE        = (  0, 255,   0)
VERDESCURO   = (  0, 155,   0)
GRIGIOSCURO  = ( 40,  40,  40)
BLU          = (  0,   0, 255)
AZZURRO      = ( 30, 144, 255)
GIALLO       = (255, 255,   0)
ROSA         = (255, 105, 180)
ROSASCURO    = (255,   0, 255)


## Impostazioni Colori E Variabili
COLORETITOLO1       = BIANCO
COLORETITOLO2       = VERDESCURO
COLORETITOLO3       = VERDE
COLOREGAMEOVER      = BIANCO
COLOREPUNTEGGIO     = GIALLO
COLORESCRITTEINFO   = GRIGIOSCURO
COLOREGRIGLIA       = GRIGIOSCURO
COLORESFONDO        = NERO
COLOREMELA          = ROSSO
COLORECORPOESTERNOB = VERDESCURO
COLORECORPOINTERNOB = VERDE
COLOREMURO          = BLU
COLOREMUROINTERNO   = AZZURRO
TESTA               = 0
SU                  = 'Su'
GIU                 = 'Giu'
SX                  = 'Sinistra'
DX                  = 'Destra'
LIVELLOINIZIALE     = 0


###############################################################################
# Avviamento del Programma e Costruzione Finestre
###############################################################################



## Programma Principale
def main():

    ## Inizializzazione e Variabili Globali
    pygame.init()
    global OROLOGIO, AREADIGIOCO, CARATTEREBASE
    OROLOGIO       = pygame.time.Clock()
    AREADIGIOCO    = pygame.display.set_mode((LUNGHEZZAFINESTRA, ALTEZZAFINESTRA))
    CARATTEREBASE  = pygame.font.Font('freesansbold.ttf', 18)


    ## Avvio Schermata di Inizio e settaggio Titolo
    pygame.display.set_caption('SNAKE!!!')
    mostraSchermataIniziale()


    ## Ciclo Principale
    while True:
        if not LIVELLI:
            mostraSchermataFinale(avviaGiocoStandard())
        elif   LIVELLI:
            mostraSchermataFinale(avviaGiocoLivelli())



###############################################################################
# Avviamento Gioco Standard senza Livelli di Tipo Bordi o Senza Bordi
###############################################################################



## Funzione di Gioco Standard
def avviaGiocoStandard():

    ## Inizializza il Verme
    direzione = DX
    muri = []
    xinizio = random.randint(5, CELLEORIZZONTALI - 6)
    yinizio = random.randint(5, CELLEVERTICALI - 6)
    coordinateVerme = [{'x': xinizio,     'y': yinizio},
                       {'x': xinizio - 1, 'y': yinizio},
                       {'x': xinizio - 2, 'y': yinizio}]

    ## Inizializza la Mela e il Timer
    mela = prendiCasellaCasuale(muri,coordinateVerme)
    tempoInizio = time.time()

    ## Ciclo di Gioco Principale
    while True:

        ## Rilevazione Eventi e Cambio Direzione
        for evento in pygame.event.get():
            if evento.type == QUIT:
                termina()
            elif evento.type == KEYDOWN:
                if   (evento.key == K_LEFT  or evento.key == K_a) and direzione != DX:
                    direzione = SX
                elif (evento.key == K_RIGHT or evento.key == K_d) and direzione != SX:
                    direzione = DX
                elif (evento.key == K_UP    or evento.key == K_w) and direzione != GIU:
                    direzione = SU
                elif (evento.key == K_DOWN  or evento.key == K_s) and direzione != SU:
                    direzione = GIU
                elif evento.key == K_ESCAPE:
                    termina()

        ## Controlla se il Verme Colpisce un Bordo
        if BORDI:
            if bordoColpito(coordinateVerme):
                return False

        ## Controlla se il Verme si Colpisce
        for coordinataVerme in coordinateVerme[1:]:
            if  coordinataVerme['x'] == coordinateVerme[TESTA]['x']\
            and coordinataVerme['y'] == coordinateVerme[TESTA]['y']:
                return False

        ## Permette di Attraversare i Bordi
        if not BORDI:
            for coordinataVerme in coordinateVerme:
                coordinateVerme[TESTA]['x']=coordinateVerme[TESTA]['x']%CELLEORIZZONTALI
                coordinateVerme[TESTA]['y']=coordinateVerme[TESTA]['y']%CELLEVERTICALI


        ## Controlla se il Verme Mangia una Mela
        if  coordinateVerme[TESTA]['x'] == mela['x']\
        and coordinateVerme[TESTA]['y'] == mela['y']:
            ## Se si' -> Setta Nuova Mela
            mela = prendiCasellaCasuale(muri,coordinateVerme)
        else:
            ## Se no -> Toglie Coda
            del coordinateVerme[-1]


        ## Muove il Verme Aggiungendo una Nuova Testa
        if   direzione == SU:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'],     'y': coordinateVerme[TESTA]['y'] - 1}
        elif direzione == GIU:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'],     'y': coordinateVerme[TESTA]['y'] + 1}
        elif direzione == SX:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'] - 1, 'y': coordinateVerme[TESTA]['y']}
        elif direzione == DX:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'] + 1, 'y': coordinateVerme[TESTA]['y']}
        coordinateVerme.insert(0, nuovaTesta)

        ## Impostazioni Cronometro
        tempo = time.time()-tempoInizio

        ## Istruzioni di Disegno
        AREADIGIOCO.fill(COLORESFONDO)                # Sfondo
        disegnaGriglia()                              # Griglia
        disegnaVerme(coordinateVerme)                 # Verme
        disegnaMela(mela)                             # Mela
        scriviPunteggio(len(coordinateVerme) - 3)     # Punteggio
        scriviTempo(tempo)                            # Tempo
        scriviGioco()                                 # Modalita' di Gioco

        ## Aggiornamenti
        pygame.display.update()
        OROLOGIO.tick(FPS)



###############################################################################
# Avviamento del Gioco a Livelli
###############################################################################



## Funzione di Gioco A Livelli (Caselle 50*30)
def avviaGiocoLivelli():

    ## Si sposta nella directory dello script
    ## Fatto perche' con alcuni sistemi lo script non viene eseguito
    ## nella sua cartella, quindi il file snakeLivelli.txt non veniva trovato
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    ## Apre Legge e Interpreta il File Livelli
    livelli = leggiFileLivelli("snakeLivelli.txt")


    ## Elenco livelli Superati
    livelliSuperati = []
    livelloCorrente = LIVELLOINIZIALE
    vite = VITE - 1
    tempo = 0


    ## Avvia i Livelli
    while True:

        risoluzione,tempo = livello(livelloCorrente,vite,tempo,livelli)
        livelliSuperati.append(risoluzione)

        ## Controlla se il Livello e' stato Superato

        if not False in livelliSuperati:
            if livelloCorrente%5==4:
                vite += 1
            livelloCorrente += 1

        elif False in livelliSuperati:
            if vite == 0:
                return False
            elif vite > 0:
                livelliSuperati.pop()
                vite = vite-1

        ## Controlla se sono finiti i Livelli
        if livelloCorrente >= LABIRINTI:
            return True

def vitaInMeno(lvl, coordinateVerme, mela, labirinto, vite, tempoPrecedente):
    global COLORECORPOESTERNO, COLORECORPOINTERNO
    COLORECORPOESTERNO = ROSSO
    COLORECORPOINTERNO = GIALLO

    ## Istruzioni di Disegno
    AREADIGIOCO.fill(COLORESFONDO)                              # Sfondo
    disegnaGriglia()                                            # Griglia
    disegnaVerme(coordinateVerme)                               # Verme
    disegnaMela(mela)                                           # Mela
    disegnaMuri(labirinto)                                      # Muri del Livello
    punteggioRestante(SUPERAMENTO - len(coordinateVerme) + 3)   # Punteggio
    scriviLivello(lvl)                                          # Livello Corrente
    scriviVite(vite)                                            # Vite
    scriviTempo(tempoPrecedente)                                # Tempo


    pygame.display.update()
    pygame.time.wait(1000)
    COLORECORPOESTERNO = COLORECORPOESTERNOB
    COLORECORPOINTERNO = COLORECORPOINTERNOB

###############################################################################
# Avviamento dei Singoli Livelli
###############################################################################



## Livello Singolo
def livello(livello,vite,tempoPrecedente,livelli):


    ## Inizializza la Mela e i Muri e il Verme
    xinizio = livelli[livello]["testaSerpente"][0]
    yinizio = livelli[livello]["testaSerpente"][1]
    muri    = livelli[livello]["muri"]
    noSpawn = livelli[livello]["noSpawn"]
    labirinto = creaLabirinto(muri)
    direzione = DX
    coordinateVerme = [{'x': xinizio,     'y': yinizio},
                       {'x': xinizio - 1, 'y': yinizio},
                       {'x': xinizio - 2, 'y': yinizio}]
    mela = prendiCasellaCasuale(noSpawn,coordinateVerme)


    ## Inizializza il Livello

    AREADIGIOCO.fill(COLORESFONDO)                              # Sfondo
    disegnaGriglia()                                            # Griglia
    disegnaVerme(coordinateVerme)                               # Verme
    disegnaMela(mela)                                           # Mela
    disegnaMuri(labirinto)                                      # Muri del Livello
    punteggioRestante(SUPERAMENTO-len(coordinateVerme) + 3)     # Punteggio
    scriviLivello(livello)                                      # Livello Corrente
    scriviVite(vite)                                            # Vite
    scriviTempo(tempoPrecedente)                                # Tempo Trascorso
    scriviInfo()                                                # Premi un Tasto
    pygame.display.update()
    pygame.time.wait(1000)

    while True:
        if controllaTasto():
            pygame.event.get()
            break

    while True:
        if controllaTasto():
            pygame.event.get()
            break

    ## Inizializza Cronometro
    tempoGioco = 0
    tempoInizio = time.time()

    ## Ciclo di Gioco Principale
    while len(coordinateVerme)<SUPERAMENTO+3:

        ## Rilevazione Eventi e Cambio Direzione
        for evento in pygame.event.get():
            if evento.type == QUIT:
                termina()
            elif evento.type == KEYDOWN:
                if   (evento.key == K_LEFT  or evento.key == K_a) and direzione != DX:
                    direzione = SX
                elif (evento.key == K_RIGHT or evento.key == K_d) and direzione != SX:
                    direzione = DX
                elif (evento.key == K_UP    or evento.key == K_w) and direzione != GIU:
                    direzione = SU
                elif (evento.key == K_DOWN  or evento.key == K_s) and direzione != SU:
                    direzione = GIU
                elif evento.key == K_ESCAPE:
                    termina()

        ## Muove il Verme Aggiungendo una Nuova Testa
        if direzione == SU:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'], 'y': coordinateVerme[TESTA]['y'] - 1}
        elif direzione == GIU:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'], 'y': coordinateVerme[TESTA]['y'] + 1}
        elif direzione == SX:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'] - 1, 'y': coordinateVerme[TESTA]['y']}
        elif direzione == DX:
            nuovaTesta = {'x': coordinateVerme[TESTA]['x'] + 1, 'y': coordinateVerme[TESTA]['y']}
        coordinateVerme.insert(0, nuovaTesta)

        ## Controlla se il Verme si Colpisce
        for coordinataVerme in coordinateVerme[1:]:
            if  coordinataVerme['x'] == coordinateVerme[TESTA]['x']\
            and coordinataVerme['y'] == coordinateVerme[TESTA]['y']:
                vitaInMeno(livello, coordinateVerme, mela, labirinto,  vite, tempoPrecedente+tempoGioco)
                return False, tempoPrecedente+tempoGioco

        ## Controlla se il Verme Colpisce un Muro
        for muro in labirinto:
            if muro['x'] == coordinateVerme[TESTA]['x'] \
            and muro['y'] == coordinateVerme[TESTA]['y']:
                vitaInMeno(livello, coordinateVerme, mela, labirinto, vite, tempoPrecedente + tempoGioco)
                return False, tempoPrecedente + tempoGioco

        ## Permette di Attraversare i Bordi
        if not BORDI:
            for coordinataVerme in coordinateVerme:
                coordinateVerme[TESTA]['x']=coordinateVerme[TESTA]['x']%CELLEORIZZONTALI
                coordinateVerme[TESTA]['y']=coordinateVerme[TESTA]['y']%CELLEVERTICALI


        ## Controlla se il Verme Mangia una Mela
        if  coordinateVerme[TESTA]['x'] == mela['x']\
        and coordinateVerme[TESTA]['y'] == mela['y']:
            ## Se si' -> Setta Nuova Mela
            mela = prendiCasellaCasuale(muri,coordinateVerme)
        else:
            ## Se no -> Toglie Coda
            del coordinateVerme[-1]

        ## Istruzioni Cronometro
        tempoGioco = time.time()-tempoInizio

        ## Istruzioni di Disegno
        AREADIGIOCO.fill(COLORESFONDO)                              # Sfondo
        disegnaGriglia()                                            # Griglia
        disegnaVerme(coordinateVerme)                               # Verme
        disegnaMela(mela)                                           # Mela
        disegnaMuri(labirinto)                                      # Muri del Livello
        punteggioRestante(SUPERAMENTO-len(coordinateVerme) + 3)     # Punteggio
        scriviLivello(livello)                                      # Livello Corrente
        scriviVite(vite)                                            # Vite
        scriviTempo(tempoPrecedente+tempoGioco)                     # Tempo

        ## Aggiornamenti
        pygame.display.update()
        OROLOGIO.tick(FPS)

    ## Controlla se il Livello e' stato Superato
    if   len(coordinateVerme)<=SUPERAMENTO+2:
        return False, tempoPrecedente+tempoGioco
    else:
        return True, tempoPrecedente+tempoGioco



###############################################################################
# Funzioni di Verifica e Gestione Eventi da Utente
###############################################################################



## Controlla Primo Inserimento
def controllaTasto():
    if len(pygame.event.get(QUIT)) > 0:
        termina()

    evento = pygame.event.get(KEYUP)
    if len(evento) == 0:
        return None
    if evento[0].key == K_ESCAPE:
        termina()
    return evento[0].key



## Termina  il Gioco
def termina():
    pygame.quit()
    sys.exit()



###############################################################################
# Funzioni di Verifica Avvenimenti in Gioco
###############################################################################



## Controlla se il Verme Colpisce un Bordo
def bordoColpito(coordinateVerme):
    if coordinateVerme[TESTA]['x'] == -1\
    or coordinateVerme[TESTA]['x'] == CELLEORIZZONTALI\
    or coordinateVerme[TESTA]['y'] == -1\
    or coordinateVerme[TESTA]['y'] == CELLEVERTICALI:
        return True
    else:
        return False



###############################################################################
# Funzioni di Creazione Elementi di Gioco
###############################################################################



## Sceglie una Casella Casuale per la Mela
def prendiCasellaCasuale(noSpawn,coordinateVerme):

    x = random.randint(0, CELLEORIZZONTALI - 1)
    y = random.randint(0, CELLEVERTICALI   - 1)
    
    while [x,y] in noSpawn or [x,y] in coordinateVerme:
        x = random.randint(1, CELLEORIZZONTALI - 2)
        y = random.randint(1, CELLEVERTICALI   - 2)
    return {'x': x,
            'y': y}




## Costruisce il Labirinto
def creaLabirinto(muri):

    labirinto = [] 
    
    for muro in range(len(muri)):
        labirinto.append({'x':muri[muro][0],'y':muri[muro][1]})
          
    return labirinto



###############################################################################
# Funzioni di Calcolo
###############################################################################



## Converte in formato ore/minuti/secondi
def convertiTempo(tempo):
    secondi  = int(tempo   // 1)
    minuti   = int(secondi // 60)
    ore      = int(secondi // 3600)
    minuti   = int(minuti  - 60*ore)
    secondi  = int(secondi - 60*minuti-3600*ore)
    if ore > 0:
        tempodigioco = str(" {} h {} min {} sec ").format(ore,minuti,secondi)
    elif ore == 0:
        if minuti > 0:
            tempodigioco = str(" {} min {} sec ").format(minuti,secondi)
        elif minuti == 0:
            tempodigioco = str(" {} sec ").format(secondi)
    return tempodigioco




###############################################################################
# Funzioni di Creazione Scritte di Gioco
###############################################################################



## Mostra Scritta di Info
def scriviInfo():
    areaInfo = CARATTEREBASE.render('Premi un Tasto per Iniziare!', True, COLORESCRITTEINFO)
    rettangoloInfo = areaInfo.get_rect()
    rettangoloInfo.topleft = (LUNGHEZZAFINESTRA - 250, ALTEZZAFINESTRA - 30)
    AREADIGIOCO.blit(areaInfo, rettangoloInfo)



## Mostra Scritta Game Over
def mostraSchermataFinale(vittoria):
    carattereScritta = pygame.font.Font('freesansbold.ttf', 150)

    if vittoria:
        areaGame = carattereScritta.render('Hai', True, COLOREGAMEOVER)
        areaOver = carattereScritta.render('Vinto', True, COLOREGAMEOVER)

    if not vittoria:
        areaGame = carattereScritta.render('Game', True, COLOREGAMEOVER)
        areaOver = carattereScritta.render('Over', True, COLOREGAMEOVER)

    
    rettangoloGame = areaGame.get_rect()
    rettangoloOver = areaOver.get_rect()
    rettangoloGame.midtop = (LUNGHEZZAFINESTRA / 2, 20)
    rettangoloOver.midtop = (LUNGHEZZAFINESTRA / 2, rettangoloGame.height + 20 + 25)

    AREADIGIOCO.blit(areaGame, rettangoloGame)
    AREADIGIOCO.blit(areaOver, rettangoloOver)
    scriviInfo()
    
    pygame.display.update()
    pygame.time.wait(500)
    controllaTasto()

    while True:
        if controllaTasto():
            pygame.event.get() 
            return



## Mostra Punteggio
def scriviPunteggio(punteggio):
    areaPunteggio = CARATTEREBASE.render('Punteggio: %s' % (punteggio), True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (LUNGHEZZAFINESTRA - 140, 10)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)

    

## Mostra Tempo
def scriviTempo(punteggio):
    punteggio=convertiTempo(punteggio)
    areaPunteggio = CARATTEREBASE.render('Durata: %s' % (punteggio), True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (10, ALTEZZAFINESTRA -30)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)



## Mostra Vite
def scriviVite(punteggio):
    areaPunteggio = CARATTEREBASE.render('Vite Attuali: %s' % (punteggio+1), True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (LUNGHEZZAFINESTRA - 190, 30)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)



## Mostra la Modalita' di Gioco
def scriviGioco():
    if BORDI:
        areaPunteggio = CARATTEREBASE.render('Bordi On', True, COLOREPUNTEGGIO)
    if not BORDI:
        areaPunteggio = CARATTEREBASE.render('Bordi Off', True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (10, 10)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)



## Mostra il Livello Corrente
def scriviLivello(livello):
    livello=livello+1
    areaPunteggio = CARATTEREBASE.render('Livello %s' % (livello), True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (10, 10)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)



## Mostra Mele Mancanti
def punteggioRestante(punteggio):
    areaPunteggio = CARATTEREBASE.render('Mele Necessarie: %s' % (punteggio), True, COLOREPUNTEGGIO)
    rettangoloPunteggio = areaPunteggio.get_rect()
    rettangoloPunteggio.topleft = (LUNGHEZZAFINESTRA - 190, 10)
    AREADIGIOCO.blit(areaPunteggio, rettangoloPunteggio)


    
###############################################################################
# Funzioni di Creazione Schermate
###############################################################################



## Mostra la Schermata di Avvio
def mostraSchermataIniziale():
    carattereTitolo = pygame.font.Font('freesansbold.ttf', 100)
    areaTitolo1     = carattereTitolo.render('Snake!', True, COLORETITOLO1, COLORETITOLO2)
    areaTitolo2     = carattereTitolo.render('Snake!', True, COLORETITOLO3)
    gradi1 = 0
    gradi2 = 0
    
    while True:
        
        AREADIGIOCO.fill(COLORESFONDO)
        areaRuotata1 = pygame.transform.rotate(areaTitolo1, gradi1)
        rettangoloR1 = areaRuotata1.get_rect()
        rettangoloR1.center = (LUNGHEZZAFINESTRA / 2, ALTEZZAFINESTRA / 2)
        AREADIGIOCO.blit(areaRuotata1, rettangoloR1)

        areaRuotata2 = pygame.transform.rotate(areaTitolo2, gradi2)
        rettangoloR2 = areaRuotata2.get_rect()
        rettangoloR2.center = (LUNGHEZZAFINESTRA / 2, ALTEZZAFINESTRA / 2)
        AREADIGIOCO.blit(areaRuotata2, rettangoloR2)

        scriviInfo()

        if controllaTasto():
            pygame.event.get()
            return
        
        pygame.display.update()
        OROLOGIO.tick(FPS)
        gradi1 += 3         # ruota di 3 gradi
        gradi2 += 7         # ruota di 7 gradi



###############################################################################
# Funzioni di Disegno Elementi di Gioco
###############################################################################



## Disegna il Verme
def disegnaVerme(coordinateVerme):
    COLORECORPOESTERNO = COLORECORPOESTERNOB
    COLORECORPOINTERNO = COLORECORPOINTERNOB
    for coordinate in coordinateVerme:
        x = coordinate['x'] * DIMENSIONECELLE
        y = coordinate['y'] * DIMENSIONECELLE
        corpoEsterno = pygame.Rect(x, y, DIMENSIONECELLE, DIMENSIONECELLE)
        pygame.draw.rect(AREADIGIOCO, COLORECORPOESTERNO, corpoEsterno)
        corpoInterno = pygame.Rect(x + 4, y + 4, DIMENSIONECELLE - 8, DIMENSIONECELLE - 8)
        pygame.draw.rect(AREADIGIOCO, COLORECORPOINTERNO, corpoInterno)



## Disegna la Mela
def disegnaMela(coordinate):
    x = coordinate['x'] * DIMENSIONECELLE
    y = coordinate['y'] * DIMENSIONECELLE
    posizioneMela = pygame.Rect(x, y, DIMENSIONECELLE, DIMENSIONECELLE)
    pygame.draw.rect(AREADIGIOCO, COLOREMELA, posizioneMela)



## Disegna i Muri
def disegnaMuri(muri):
    for muro in range(len(muri)):
        x = muri[muro]['x'] * DIMENSIONECELLE
        y = muri[muro]['y'] * DIMENSIONECELLE
        posizioneMuro = pygame.Rect(x, y, DIMENSIONECELLE, DIMENSIONECELLE)
        pygame.draw.rect(AREADIGIOCO, COLOREMURO, posizioneMuro)
        posizioneMuroInterno = pygame.Rect(x + 4, y + 4, DIMENSIONECELLE - 8, DIMENSIONECELLE - 8)
        pygame.draw.rect(AREADIGIOCO, COLOREMUROINTERNO, posizioneMuroInterno)



## Disegna la Griglia
def disegnaGriglia():
    
    ## Disegna le righe Verticali
    for x in range(0, LUNGHEZZAFINESTRA, DIMENSIONECELLE): 
        pygame.draw.line(AREADIGIOCO, COLOREGRIGLIA, (x, 0), (x, ALTEZZAFINESTRA))
    ## Disegna le righe Orizzontali
    for y in range(0, ALTEZZAFINESTRA, DIMENSIONECELLE): 
        pygame.draw.line(AREADIGIOCO, COLOREGRIGLIA, (0, y), (LUNGHEZZAFINESTRA, y))



###############################################################################
# Impostazioni Generali di Gioco
###############################################################################



## Apre Legge e Interpreta il File Livelli
def leggiFileLivelli(nomeFile):

    # Controlla l'Esistenza del File e lo Apre
    assert os.path.exists(nomeFile), 'Non e\' Stato trovato il File: %s' % (nomeFile)
    fileMappe = open(nomeFile, 'r')
    # Legge una Linea alla Volta e le Separa e Chiude il File
    contenutoFile = fileMappe.readlines() + ['\r\n']
    fileMappe.close()


    # Crea le Variabili che Conterranno le Informazioni
    livelloNum = 0          # Segna il Numero del Livello
    livelli = []            # Contiene i Livelli
    lineeMappa = []         # Contiene le Linee Singole dei Livelli
    oggettiMappa = []       # Risultato che Contiene lo Schema del Livello


    # Ciclo che Opera su Ogni Linea del File
    for lineaNum in range(len(contenutoFile)):

        # Elimina gli Spazi Bianchi a Fine Riga
        linea = contenutoFile[lineaNum].rstrip('\r\n')

        
        # Permette di Ignorare le Linee che Iniziano per ";" Rendendole Commenti
        if   ';' in linea:
            linea = linea[:linea.find(';')]

            
        # Prende le Linee che non Iniziano per ";" o "" che sono le Parti di Mappa e le Aggiunge alle Linee di Mappa
        if   linea != '':
            lineeMappa.append(linea)


        # Quando Trova una Linea Vuota (Fine Livello) inizia a Creare il Livello
        elif linea == '' and len(lineeMappa) > 0:
            

            # Trova La Line piu' Lunga
            lunghezzaMassima = -1
            for i in range(len(lineeMappa)):
                if len(lineeMappa[i]) > lunghezzaMassima:
                    lunghezzaMassima = len(lineeMappa[i])
                    

            # Aggiunge Spazi nelle Righe Corte
            for i in range(len(lineeMappa)):
                lineeMappa[i] += ' ' * (lunghezzaMassima - len(lineeMappa[i]))
                

            # Rende le singole Linee una Mappa in una Matrice
            for x in range(len(lineeMappa[0])):
                oggettiMappa.append([])
            for y in range(len(lineeMappa)):
                for x in range(lunghezzaMassima):
                    oggettiMappa[x].append(lineeMappa[y][x])
                    

            # Inizializza le Variabili di Testa serpente, Muri e no Spawn
            xInizio = None       # x Testa serpente                         -> "@"
            yInizio = None       # y Testa serpente                         -> "@"
            muri    = []         # lista di [x, y] per i Muri               -> "$"
            noSpawn = []         # lista di [x, y] per i Punti di noSpawn   -> "%"
            

            # Controlla tutti gli Spazi Cercando "@","$","%"
            for x in range(lunghezzaMassima):
                for y in range(len(oggettiMappa[x])):

                    # '@' e' la Testa del serpente
                    if oggettiMappa[x][y] in ('@'):
                        xInizio = x-1
                        yInizio = y-1

                    # '$' e' un Muro    
                    if oggettiMappa[x][y] in ('$'):
                        muri.append([x-1, y-1])

                    # '$' e' un Muro, "%" e' un Punto di No Spawn
                    if oggettiMappa[x][y] in ('$', '%'):
                        noSpawn.append([x-1, y-1])

            # Controlla che ci Sia lo Spawn della Testa:
            assert xInizio != None and yInizio != None, 'Il Livello %s (nella linea %s) nel File %s non ha un "@" o un "+" per Segnare la Partenza.' % (livelloNum+1, lineaNum, nomeFile)
        

            # Crea l'Output con la Mappa, i Muri, i Punti di No Spawn e la Testa del Serpente
            livelloSingolo = {'oggettiMappa': oggettiMappa,\
                              'muri': muri,\
                              'noSpawn': noSpawn,\
                              'testaSerpente': (xInizio, yInizio)}
            livelli.append(livelloSingolo)

            # Resetta le Variabili per il Livello Successivo
            lineeMappa = []
            oggettiMappa = []
            livelloNum += 1
            
    return livelli


###############################################################################
# Esecuzione del Programma
###############################################################################



## Programma Svolto
if __name__ == '__main__':
    main()



###############################################################################
# Fine Codice
###############################################################################

## Cambia Dimensione Finestra
def ridimensiona():
    global SCHERMOINTERO
    global CAMERAX, CAMERAY
    if SCHERMOINTERO:
        CAMERAX, CAMERAY = CAMERAX+6*DIMENSIONECELLE, CAMERAY+3*DIMENSIONECELLE
        AREADIGIOCO = schermoNormale()
    if not SCHERMOINTERO:
        CAMERAX, CAMERAY = CAMERAX-6*DIMENSIONECELLE, CAMERAY-3*DIMENSIONECELLE
        AREADIGIOCO = schermoIntero()
    SCHERMOINTERO = not SCHERMOINTERO



## Finestra da Normale a Full
def schermoIntero():
    global ALTEZZAFINESTRA, LUNGHEZZAFINESTRA
    dimensioniSchermo   =  LUNGHEZZASCHERMO, ALTEZZASCHERMO                 
    LUNGHEZZAFINESTRA   =  LUNGHEZZASCHERMO
    ALTEZZAFINESTRA     =  ALTEZZASCHERMO
    return pygame.display.set_mode((dimensioniSchermo))



## Finestra da Full a Normale
def schermoNormale():
    global ALTEZZAFINESTRA, LUNGHEZZAFINESTRA
    dimensioniSchermo   = LUNGHEZZAFINESTRABASE, ALTEZZAFINESTRABASE
    ALTEZZAFINESTRA     = ALTEZZAFINESTRABASE
    LUNGHEZZAFINESTRA   = LUNGHEZZAFINESTRABASE
    return pygame.display.set_mode((dimensioniSchermo))



## Finestra Normale alla Prima Apertura
def schermoIniziale():
    global ALTEZZAFINESTRA, LUNGHEZZAFINESTRA
    dimensioniSchermo   = LUNGHEZZAFINESTRABASE, ALTEZZAFINESTRABASE
    ALTEZZAFINESTRA     = ALTEZZAFINESTRABASE
    LUNGHEZZAFINESTRA   = LUNGHEZZAFINESTRABASE
    return pygame.display.set_mode((dimensioniSchermo))


