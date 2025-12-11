# 🎓 Exam Simulator - Professional Edition v2.0

**Un simulatore d'esame desktop leggero, portatile e potente per prepararsi alle certificazioni IT (CCNA, CompTIA, ecc.) e non solo.**

![Screenshot](screenshot.png)
*(Suggerimento: Carica uno screenshot dell'app in azione e chiamalo screenshot.png per vederlo qui)*

## 📖 Descrizione

Questo repository contiene l'eseguibile (`.exe`) e i database delle domande per **Exam Simulator**. Non è necessaria alcuna installazione o configurazione complessa: scarica, avvia e inizia ad esercitarti.

Il software è stato progettato per simulare l'ambiente di test reale, con funzionalità avanzate per l'apprendimento e la revisione.

### 📦 Contenuto del Repository
* **ExamSimulator.exe**: Il programma principale (Versione 2.0).
* **Database CCNA 200-301**: Una raccolta completa di domande basate sul Volume 1 della guida ufficiale (Networking, IP, Switching, Wireless), suddivise per capitoli.
* **Modelli CSV**: File di esempio per creare i propri test.

---

## ✨ Funzionalità Principali

* **🚀 Portatile:** Nessuna installazione richiesta. Funziona su qualsiasi PC Windows.
* **📄 Supporto Multi-Formato:** Carica nativamente file **JSON** e **CSV (Excel)**.
* **⏱️ Simulazione Reale:**
    * **Modalità Esame:** Feedback nascosto fino alla fine, timer attivo.
    * **Modalità Allenamento:** Feedback immediato con spiegazioni dettagliate.
* **🛠️ Editor Integrato:** Crea e salva nuove domande direttamente dall'interno dell'applicazione.
* **🌙 Dark Mode:** Tema scuro per non affaticare la vista durante le sessioni notturne.
* **🔀 Shuffle Avanzato:** Mischia sia l'ordine delle domande che l'ordine delle risposte (A, B, C, D) per evitare la memorizzazione visiva.
* **👁️ Accessibilità:** Dimensione del testo regolabile (Piccolo, Medio, Grande).
* **📊 Reportistica:** Calcolo punteggio, soglia di superamento personalizzabile e possibilità di ripassare solo gli errori.

---

## 🚀 Come Iniziare

1.  Vai nella sezione **Releases** o scarica il file **`ExamSimulator.exe`** da questo repository.
2.  Scarica i file delle domande (es. `batch_ccna_vol1.json` o i singoli capitoli).
3.  Avvia `ExamSimulator.exe` (potrebbe apparire un avviso di Windows Defender la prima volta perché è un software non firmato: clicca su *Ulteriori informazioni -> Esegui comunque*).
4.  Clicca su **📂 Carica DB** e seleziona uno o più file `.json` o `.csv`.
5.  Premi **Start** (o imposta prima le preferenze su ⚙️).

---

## 📝 Come creare i propri esami

Puoi espandere il simulatore creando i tuoi quiz personali in tre modi:

### Metodo 1: Usare Excel / CSV (Consigliato per principianti) 📊
Il modo più semplice è usare Excel o Google Sheets.
1.  Crea un file con le seguenti colonne nella prima riga:
    `Capitolo`, `Argomento`, `Domanda`, `A`, `B`, `C`, `D`, `Risposta`, `Spiegazione`
2.  Compila le righe (vedi tabella sotto).
3.  Salva il file come **CSV (Comma Separated Values)**.
4.  Caricalo nel simulatore!

**Esempio struttura CSV:**

| Capitolo | Argomento | Domanda | A | B | C | D | Risposta | Spiegazione |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Cap 1 | Reti | Cos'è un IP? | Un cavo | Un indirizzo | Un PC | Un virus | B | L'IP è logico. |
| Cap 1 | Sicurezza | Protocolli sicuri? | Telnet | SSH | HTTP | HTTPS | B,D | SSH/HTTPS criptano. |

*Nota: Per le risposte multiple, separale con una virgola (es. "B,D"). Il software rileva automaticamente se usi la virgola o il punto e virgola.*

### Metodo 2: Editor Integrato 🛠️
1.  Apri il programma.
2.  Vai nel menu in alto: **Strumenti > Editor Domande**.
3.  Compila i campi (Domanda, Opzioni, Risposta, Spiegazione).
4.  Clicca **Aggiungi alla Sessione** per testarla subito o **Esporta in JSON** per salvare il file.

### Metodo 3: Formato JSON (Per sviluppatori) 💻
Se preferisci modificare il codice grezzo, usa questa struttura:

[
  {
    "id": "1",
    "capitolo": "Nome Capitolo",
    "argomento": "Argomento",
    "tipo": "singola",
    "domanda": "Testo della domanda...",
    "opzioni": [
      "A. Opzione 1",
      "B. Opzione 2",
      "C. Opzione 3",
      "D. Opzione 4"
    ],
    "risposta_corretta": "B",
    "spiegazione": "Dettagli sulla risposta..."
  },
  {
    "id": "2",
    "capitolo": "Nome Capitolo",
    "argomento": "Argomento",
    "tipo": "multipla",
    "domanda": "Esempio di domanda a risposta multipla...",
    "opzioni": [
      "A. Opzione 1",
      "B. Opzione 2",
      "C. Opzione 3",
      "D. Opzione 4"
    ],
    "risposta_corretta": ["A", "C"],
    "spiegazione": "Dettagli sulla risposta multipla..."
  }
]

## ⚙️ Impostazioni Disponibili

Cliccando sull'icona ingranaggio **⚙️**, puoi personalizzare:

* **Timer:** Attiva/Disattiva o cambia la durata (minuti).
* **Modalità Esame:** Nasconde i risultati fino alla fine ("Promosso/Bocciato").
* **Shuffle Risposte:** Mischia l'ordine di apparizione di A, B, C, D.
* **Soglia:** Cambia la percentuale richiesta per passare (Default 82% per CCNA).
* **Font:** Ingrandisci il testo per una migliore lettura.

---

## 👨‍💻 Credits

**Developed by David Aulicino**
*Versione Software: 2.0*

Questo software è distribuito gratuitamente per scopi educativi.