document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("simulationForm").addEventListener("submit", function (event) {
        event.preventDefault();

        // Récupérer les valeurs du formulaire
        let revenu = parseFloat(document.getElementById("revenu").value);
        let surface = parseFloat(document.getElementById("surface").value);
        let energie = document.getElementById("energie").value;

        // Calcul de la prime (exemple : ajustable selon les règles)
        let prime = 0;
        if (revenu < 30000) {
            prime = surface * 50; // Prime plus élevée pour petits revenus
        } else if (revenu < 50000) {
            prime = surface * 30;
        } else {
            prime = surface * 20;
        }

        // Bonus selon type d'énergie
        if (energie === "fioul") {
            prime += 500;
        }

        // Afficher le résultat
        document.getElementById("primeMontant").textContent = prime.toFixed(2);
        document.getElementById("resultat").style.display = "block";
    });
});
