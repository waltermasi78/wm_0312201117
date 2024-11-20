
const prenotazioneForm = document.getElementById("prenotazioneForm");
const prenotazioniList = document.getElementById("prenotazioni");
const feedbackMessage = document.getElementById("feedback-message");

// Funzione per caricare le prenotazioni dal server
async function caricaPrenotazioni() {
    try {
        const response = await fetch("/api/prenotazioni");
        if (response.ok) {
            const prenotazioni = await response.json();
            prenotazioniList.innerHTML = ""; // Pulisce la lista esistente
            prenotazioni.forEach(prenotazione => {
                aggiungiPrenotazioneAllaLista(prenotazione);
            });
        } else {
            console.error("Errore nel caricamento delle prenotazioni.");
        }
    } catch (error) {
        console.error("Errore:", error);
    }
}

// Funzione per aggiungere una prenotazione alla lista
function aggiungiPrenotazioneAllaLista(prenotazione) {
    const li = document.createElement("li");
    li.setAttribute("data-id", prenotazione.id);
    li.innerHTML = `
        <span>${prenotazione.nominativo} - ${prenotazione.numero_posti} posti - ${prenotazione.data} ${prenotazione.ora}</span>
        <button onclick="eliminaPrenotazione(${prenotazione.id})">Elimina</button>
    `;
    prenotazioniList.appendChild(li);
}

// Funzione per eliminare una prenotazione
async function eliminaPrenotazione(id) {
    if (!confirm("Sei sicuro di voler eliminare questa prenotazione?")) return;
    try {
        const response = await fetch(`/prenotazione/${id}`, { method: "DELETE" });
        if (response.ok) {
            mostraMessaggio("Prenotazione eliminata con successo!", "success");
            const elementoDaRimuovere = document.querySelector(`[data-id="${id}"]`);
            if (elementoDaRimuovere) {
                elementoDaRimuovere.remove();
            }
        } else {
            mostraMessaggio("Errore nell'eliminazione della prenotazione.", "error");
        }
    } catch (error) {
        console.error("Errore:", error);
    }
}

// Funzione per validare il form di prenotazione
function validaPrenotazione(formData) {
    if (!formData.nominativo || formData.nominativo.length < 3) {
        mostraMessaggio("Il nominativo deve contenere almeno 3 caratteri.", "error");
        return false;
    }
    if (!formData.numeroPosti || formData.numeroPosti <= 0) {
        mostraMessaggio("Il numero di posti deve essere maggiore di zero.", "error");
        return false;
    }
    if (!formData.data) {
        mostraMessaggio("Inserisci una data valida.", "error");
        return false;
    }
    if (!formData.ora) {
        mostraMessaggio("Inserisci un'ora valida.", "error");
        return false;
    }
    if (!formData.contatto) {
        mostraMessaggio("Inserisci un contatto (telefono o email).", "error");
        return false;
    }
    return true;
}

prenotazioneForm.onsubmit = async function (event) {
    event.preventDefault();  // Impedisce l'invio predefinito del form

    const formData = {
        nominativo: document.getElementById("nominativo").value,
        numeroPosti: document.getElementById("numeroPosti").value,
        data: document.getElementById("data").value,
        ora: document.getElementById("ora").value,
        contatto: document.getElementById("contatto").value
    };

    if (!validaPrenotazione(formData)) return;  // Interrompe l'invio se la validazione fallisce

    try {
        const response = await fetch("/prenotazione", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        const responseData = await response.json();

        if (response.ok) {
            // Mostra il messaggio di successo sulla stessa pagina
            mostraMessaggio("Prenotazione creata con successo!", "success");
            prenotazioneForm.reset();  // Resetta il form
        } else {
            // Mostra un messaggio di errore
            mostraMessaggio(responseData.message || "Errore nella creazione della prenotazione.", "error");
        }
    } catch (error) {
        console.error("Errore:", error);
        mostraMessaggio("Si è verificato un errore. Riprova.", "error");
    }
};



// Funzione per mostrare messaggi di feedback sulla stessa pagina
function mostraMessaggio(messaggio, tipo) {
    const feedbackMessage = document.getElementById("feedback-message");  // Div per messaggi di feedback

    feedbackMessage.textContent = messaggio;
    feedbackMessage.className = tipo === "success" ? "show success" : "show error";

    // Nasconde il messaggio dopo 3 secondi
    setTimeout(() => {
        feedbackMessage.classList.remove("show");
    }, 3000);
}

// Carica le prenotazioni all'inizializzazione della pagina
window.onload = function () {
    caricaPrenotazioni(); // Carica le prenotazioni all'avvio
};
