function handleRequest() {
    const tajnyKluc = document.getElementById('tajnyKluc').value;
    const typSifry = document.getElementById('typSifry').value;
    const message = document.getElementById('message').value;
    const nastavenie = document.getElementById('nastavenie').value;
    const mode = document.getElementById('mode').value;

    // Určenie správnej routy podľa módu
    const route = mode === 'encrypt' ? '/encrypt' : '/decrypt';

    fetch(route, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            tajny_kluc: tajnyKluc,
            typ_sifry: typSifry,
            message: message,
            nastavenie: nastavenie
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultBox = document.getElementById('result-box');
        if (data.error) {
            alert('Chyba: ' + data.error);
        } else {
            const resultText = data.result;
            resultBox.textContent = ""; // Vyčistenie predchádzajúceho textu
            resultBox.classList.add('result-active'); // Pridanie aktívnej animácie

            // Postupné zobrazovanie písmen po jednom
            let i = 0;
            const interval = setInterval(() => {
                if (i < resultText.length) {
                    resultBox.textContent += resultText[i];
                    i++;
                } else {
                    clearInterval(interval);
                    setTimeout(() => {
                        resultBox.classList.remove('result-active'); // Odstránenie animácie po dokončení
                    }, 2000);
                }
            }, 100); // Rýchlosť zobrazovania písmen (100ms na písmeno)
        }
    })
    .catch(error => {
        alert('Chyba: ' + error);
    });
}
