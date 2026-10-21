# Aprire il progetto BASF

Questa è la prima implementazione nativa Power BI, da verificare in Desktop.
Non è ancora un report collaudato. Non modifica il precedente file di preparazione.

Pacchetto corretto V2: estrailo in una cartella nuova. Non sovrascrivere la prima
prova già aperta o aggiornata da Power BI. Chiudi quella finestra prima di aprire
questo progetto. Se compare ancora l'avviso rosso sui metadati avanzati, non premere
«Aggiorna report»: mostra l'avviso per proseguire con la diagnosi.

1. Estrai tutto lo ZIP: tasto destro sullo ZIP > **Estrai tutto** > **Estrai**.
2. Nella cartella `BASF`, apri `assets`, fai doppio clic su
   `SpaceGrotesk-Medium.ttf` e premi **Installa**. Chiudi e riapri Power BI se era aperto.
3. Torna nella cartella `BASF` e fai doppio clic su **BASF.pbip**.
   Tieni accanto le cartelle `BASF.Report` e `BASF.SemanticModel`.
4. In Power BI Desktop premi **Home > Aggiorna** per caricare i dati incorporati.

Se il doppio clic non apre il progetto, apri Power BI Desktop e usa
**File > Apri > Sfoglia** per selezionare `BASF.pbip`.
Se compare un errore, conserva il testo completo: serve per correggere la
compatibilità della definizione. Non eliminare righe o misure per tentativi.

Al primo caricamento, senza selezione dell'anno, le schede devono mostrare il 2025:
Sales 59.657; EBITDA 5.618; EBIT 1.634; Net income 1.619; margine 11,0%;
OCF 5.610; FCF 1.342; investimenti 4.787; ROCE 5,8%.
I valori monetari sono in milioni di euro.

Prova il selettore con il 2024: Sales deve diventare 61.444, mentre i grafici
mantengono il periodo 2016–2025. Selezionando il 2016, ROCE deve restare vuoto.

Il file `verify_in_desktop.dax` contiene controlli da eseguire nella vista Query DAX.
Sono controlli preparati, ancora da eseguire nel motore di Power BI.

Non servono password, PostgreSQL o percorsi di file Excel per questo pacchetto:
contiene una copia esatta dei dati puliti già presenti nel repository.
Il refresh ricarica questa copia; non scarica nuovi dati BASF.

Il progetto su GitHub: https://github.com/Etnakid/basf-business-performance-analysis
