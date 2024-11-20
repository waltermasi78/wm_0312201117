# Sistema di Prenotazione Tavoli

Un'applicazione web per la gestione delle prenotazioni tavoli nei ristoranti, sviluppata con **Python** e il framework **Flask**. Il progetto integra un sistema di autenticazione a due livelli (cliente e amministratore) per una gestione sicura e organizzata delle prenotazioni.

## Funzionalità Principali
- Prenotazione tavoli con selezione di **data**, **ora** e **numero di persone**.
- Pagina "Lista Prenotazioni" per i ristoratori, con possibilità di visualizzare e cancellare prenotazioni.
- Sistema di autenticazione a due livelli (cliente e admin).
- Utilizzo di un **database relazionale** per la gestione delle prenotazioni.
- **Testing delle API REST** con metodi `GET`, `POST` e `DELETE` tramite [Postman](https://www.postman.com/).

## Tecnologie Utilizzate
### Backend
- **Python** con il framework [Flask](https://flask.palletsprojects.com/): per la gestione del server e delle API REST.
- **SQLite**: per il database, utilizzato per salvare e recuperare le prenotazioni.

### Frontend
- **HTML**, **CSS** e **JavaScript**: per l'interfaccia utente responsiva e intuitiva.

### Strumenti di Sviluppo
- [Git](https://git-scm.com/): per il versioning del codice.
- [GitHub](https://github.com/): per l'hosting e la condivisione del progetto.
- [Postman](https://www.postman.com/): per testare le API e garantire il corretto funzionamento.

## Struttura del Progetto
La struttura dei file e delle cartelle è la seguente:    
**wm_0312201117**  
├── app.py   
├── templates/   
│ ├── index.html   
│ └── area-riservata.html   
└── static/   
│ ├── styles.css   
│ └── app.js   
│ └── logo.png   
│ └── favicon.ico  
