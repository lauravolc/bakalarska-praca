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
            resultBox.textContent = data.result;
            // Pridanie triedy pre animáciu zvýraznenia výsledku
            resultBox.classList.add('result-generated');
            // Po uplynutí 1 sekundy sa trieda odstráni
            setTimeout(() => {
                resultBox.classList.remove('result-generated');
            }, 1000);
        }
    })
    .catch(error => {
        alert('Chyba: ' + error);
    });
}
