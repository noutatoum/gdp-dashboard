import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FRONTIER SCAN v1.3", layout="centered")

frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0b0e14; color: #e0e0e0; display: flex; justify-content: center; padding: 20px; margin: 0; }
        #app-container { width: 100%; max-width: 600px; text-align: center; }
        .header-title { color: #00d2ff; font-size: 2rem; font-weight: 800; margin-bottom: 20px; text-shadow: 0 0 10px rgba(0,210,255,0.5); }
        
        /* Quiz Styles */
        #quiz-zone { background: #161b22; padding: 25px; border-radius: 15px; border: 1px solid #30363d; }
        .progress-container { width: 100%; background-color: #30363d; border-radius: 10px; margin-bottom: 20px; height: 8px; }
        .progress-bar { height: 100%; background: linear-gradient(90deg, #00d2ff, #3a7bd5); width: 0%; transition: 0.4s; }
        .btn-option { width: 100%; padding: 14px; margin: 8px 0; background: #21262d; color: white; border: 1px solid #30363d; border-radius: 10px; font-size: 1rem; cursor: pointer; transition: 0.2s; }
        .btn-option:hover { background: #30363d; border-color: #58a6ff; transform: scale(1.01); }

        /* Results Card */
        #result-zone { display: none; }
        .alert-banner { background: #f85149; color: white; padding: 12px; border-radius: 10px; margin-bottom: 15px; font-weight: bold; animation: blink 1s infinite; display: none; }
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }
        
        #result-card { background: #0d1117; border-radius: 20px; padding: 25px; border: 2px solid #30363d; text-align: left; }
        .photo-area { display: flex; gap: 20px; align-items: center; margin-bottom: 20px; }
        .photo-frame { width: 140px; height: 140px; border-radius: 12px; border: 3px solid #58a6ff; overflow: hidden; background: #000; flex-shrink: 0; }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; }
        
        /* Stats & Probabilities */
        .stat-bar-bg { background: #30363d; height: 10px; border-radius: 5px; margin: 4px 0 12px 0; width: 100%; overflow: hidden; }
        .stat-bar-fill { height: 100%; transition: 1.5s cubic-bezier(0.1, 0, 0, 1); width: 0%; }
        .profile-name { font-size: 0.8rem; font-weight: bold; text-transform: uppercase; color: #8b949e; }
        
        .restart-btn { width: 100%; padding: 15px; background: #238636; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">TERMINAL DE CONTRÔLE FRONTALIER</div>
        
        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="margin-bottom:20px;">Analyse du sujet...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="alert-banner" class="alert-banner">🚨 INCOHÉRENCE DÉTECTÉE : FAUSSE IDENTITÉ</div>
            <div id="result-card">
                <div class="photo-area">
                    <div class="photo-frame"><img id="res-img" src=""></div>
                    <div>
                        <h2 id="res-status" style="margin:0;">ANALYSE TERMINÉE</h2>
                        <p id="res-type" style="font-size:1.5rem; font-weight:800; margin:5px 0; color:#58a6ff;"></p>
                        <p id="res-risk" style="margin:0; font-family:monospace;"></p>
                    </div>
                </div>
                <div id="stats-panel"></div>
                <button class="restart-btn" onclick="location.reload()">NOUVELLE ANALYSE</button>
            </div>
        </div>
    </div>

    <script>
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/";
        
        const PROFILS = {
            "Touriste": { img: "touriste.png", r: "BAS", c: "#238636" },
            "Hacker": { img: "hacker.png", r: "CRITIQUE", c: "#f85149" },
            "Trafiquant": { img: "trafiquant.png", r: "ÉLEVÉ", c: "#da3633" },
            "Exile": { img: "exile.png", r: "MODÉRÉ", c: "#d29922" },
            "Ananas": { img: "ananas.png", r: "BIO-RISQUE", c: "#f0883e" },
            "Agent": { img: "agent.png", r: "SÉCURISÉ", c: "#58a6ff" },
            "Artiste": { img: "artiste.png", r: "BAS", c: "#238636" },
            "Chercheur": { img: "chercheur.png", r: "CONTRÔLÉ", c: "#1f6feb" },
            "Evasion": { img: "evasion.png", r: "FINANCIER", c: "#8957e5" }
        };

        const QS = [
            { q: "Identité déclarée ?", opt: [["Touriste", "Touriste"], ["Chercheur", "Chercheur"], ["Diplomate", "Agent"], ["Réfugié", "Exile"]] },
            { q: "Objet suspect détecté ?", opt: [["Appareil Photo", "Touriste"], ["Brouilleur Wifi", "Hacker"], ["Faux Passeport", "Trafiquant"], ["Échantillon Terre", "Ananas"]] },
            { q: "Provenance du vol ?", opt: [["Paris", "Touriste"], ["Zone de Conflit", "Exile"], ["Paradis Fiscal", "Evasion"], ["Inconnu", "Trafiquant"]] },
            { q: "Réponse au test de stress ?", opt: [["Calme", "Agent"], ["Transpiration", "Trafiquant"], ["Regard fuyant", "Hacker"], ["Arrogance", "Evasion"]] },
            { q: "PIÈGE : Quel est l'objet de votre recherche ?", opt: [["Vacances (Incohérent)", "Trafiquant"], ["Physique Quantique", "Chercheur"], ["C'est confidentiel", "Agent"], ["Je n'ai rien à dire", "Hacker"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Artiste":0, "Chercheur":0, "Evasion":0 };
        let lieDetected = false;

        function loadQ() {
            if (step < QS.length) {
                const curr = QS[step];
                document.getElementById("p-bar").style.width = ((step / QS.length) * 100) + "%";
                document.getElementById("q-text").innerText = curr.q;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                curr.opt.forEach(o => {
                    const b = document.createElement("button");
                    b.className = "btn-option"; b.innerText = o[0];
                    b.onclick = () => { 
                        // Logique de détection de mensonge : 
                        // Si le joueur a dit être Chercheur (Etape 1) mais répond Vacances (Etape 5)
                        if(step === 4 && o[0] === "Vacances (Incohérent)" && sc["Chercheur"] > 0) {
                            lieDetected = true;
                        }
                        sc[o[1]] += 20; 
                        step++; 
                        loadQ(); 
                    };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-zone").style.display = "block";

            // Calcul du profil dominant
            const win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            const data = PROFILS[win];

            // Gestion des alertes
            if (lieDetected || sc["Trafiquant"] > 0) {
                document.getElementById("alert-banner").style.display = "block";
                document.getElementById("result-card").style.borderColor = "#f85149";
                document.getElementById("res-status").innerText = "ACCÈS REFUSÉ";
                document.getElementById("res-status").style.color = "#f85149";
            } else if (data.r === "BAS" || data.r === "SÉCURISÉ") {
                document.getElementById("res-status").innerText = "ACCÈS ACCORDÉ";
                document.getElementById("res-status").style.color = "#3fb950";
                confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
            }

            // Image (Gestion Evasion / evasion)
            const imgEl = document.getElementById("res-img");
            const fileName = win === "Evasion" ? "evasion.png" : win.toLowerCase() + ".png";
            imgEl.src = PATH + fileName;
            imgEl.onerror = () => { imgEl.src = "https://via.placeholder.com/140?text=SCAN+ID"; };

            document.getElementById("res-type").innerText = win.toUpperCase();
            document.getElementById("res-risk").innerText = "NIVEAU DE RISQUE : " + data.r;

            // Affichage des probabilités
            const panel = document.getElementById("stats-panel");
            Object.keys(sc).forEach(p => {
                if(sc[p] > 0) {
                    const row = document.createElement("div");
                    row.innerHTML = `
                        <div style="display:flex; justify-content:space-between; margin-top:10px;">
                            <span class="profile-name">${p}</span>
                            <span style="font-size:0.8rem; color:#8b949e;">${sc[p]}%</span>
                        </div>
                        <div class="stat-bar-bg"><div class="stat-bar-fill" style="width:${sc[p]}%; background:${PROFILS[p].c}"></div></div>
                    `;
                    panel.appendChild(row);
                }
            });
        }
        loadQ();
    </script>
</body>
</html>
"""

components.html(frontier_html, height=900)
