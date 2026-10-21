# Aprire il progetto BASF

Questo è il report nativo BASF approvato dopo la verifica in Power BI Desktop.
Sono stati controllati il 2025, il cambio al 2024 e il ROCE 2016 mancante.
Il proprietario del progetto ha eseguito la query DAX e comunicato 22 risultati PASS.
Il PDF originale e le immagini finali del portfolio sono ancora da esportare.

Mantieni insieme il file PBIP e le due cartelle del report e del modello.
Il precedente file di preparazione non viene modificato.

1. Estrai tutto lo ZIP: tasto destro sullo ZIP > **Estrai tutto** > **Estrai**.
2. Nella cartella `BASF`, fai doppio clic su **BASF.pbip**.
   Tieni accanto le cartelle `BASF.Report` e `BASF.SemanticModel`.
3. In Power BI Desktop premi **Home > Aggiorna** per caricare i dati incorporati.

Il titolo, il logo, le foto sfumate, le nove superfici arrotondate, le etichette e
le unità sono già nello sfondo incluso: non devi ricrearli manualmente.
I numeri e i grafici sono visual nativi e interattivi, non immagini.

Il font del titolo è già incorporato nello sfondo. Per richiedere lo stesso font
anche sui valori, puoi installare `assets/SpaceGrotesk-Medium.ttf` e riaprire Power BI.
Senza installarlo, il progetto prevede Segoe UI come riserva per il testo nativo.

Se il doppio clic non apre il progetto, apri Power BI Desktop e usa
**File > Apri > Sfoglia** per selezionare `BASF.pbip`.
Se compare un errore, conserva il testo completo: serve per correggere la
compatibilità della definizione. Non eliminare righe o misure per tentativi.

Al primo caricamento il selettore deve mostrare 2025 e le schede devono riportare:
Sales 59.657; EBITDA 5.618; EBIT 1.634; Net income 1.619; margine 11,0%;
OCF 5.610; FCF 1.342; investimenti 4.787; ROCE 5,8%.
I valori monetari sono in milioni di euro.

Prova il selettore con il 2024: Sales deve diventare 61.444, mentre i grafici
mantengono il periodo 2016–2025. Selezionando il 2016, ROCE deve restare vuoto.

Il file `verify_in_desktop.dax` contiene controlli da eseguire nella vista Query DAX.
I 22 controlli risultano PASS secondo la verifica comunicata dal proprietario.
Puoi rieseguirli dopo ogni modifica al modello.

Non servono password, PostgreSQL o percorsi di file Excel per questo pacchetto:
contiene una copia esatta dei dati puliti già presenti nel repository.
Il refresh ricarica questa copia; non scarica nuovi dati BASF.

Il progetto su GitHub: https://github.com/Etnakid/basf-business-performance-analysis
