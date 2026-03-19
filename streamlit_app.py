
import streamlit as st
import streamlit.components.v1 as components

# Config Streamlit
st.set_page_config(page_title="FRONTIER SCAN", layout="centered")

# On intègre tout le design et la logique dans ce bloc HTML/JS
frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; display: flex; justify-content: center; padding: 20px; }
        #app-container { width: 100%; max-width: 600px; text-align: center; }
        
        .header-title { color: #00d2ff; font-size: 2.5rem; font-weight: 800; margin-bottom: 20px; display: flex; justify-content: center; align-items: center; gap: 15px; }
        
        /* Style des boutons de choix */
        .btn-option { width: 100%; padding: 15px; margin: 10px 0; background: white; color: #1c1e21; border: 1px solid #ddd; border-radius: 10px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-option:hover { background: #f0f2f5; border-color: #00d2ff; }

        /* BANDEAU ACCÈS */
        #access-bar { display: none; width: 100%; padding: 15px; border-radius: 10px; margin-bottom: 15px; font-weight: bold; text-align: left; }
        
        /* CARTE NOIRE (Ton design) */
        #result-card { display: none; background: #1b2838; border-radius: 20px; padding: 30px; border-bottom: 5px solid #42b72a; text-align: left; position: relative; animation: slideUp 0.5s ease; }
        
        .id-number { position: absolute; top: 20px; right: 25px; color: white; opacity: 0.8; font-weight: bold; }
        .status-dot { color: #42b72a; font-weight: bold; margin-bottom: 20px; display: block; }
        
        .profile-section { display: flex; gap: 20px; align-items: center; margin-bottom: 30px; }
        .photo-frame { width: 180px; height: 180px; border-radius: 20px; border: 2px solid #42b72a; overflow: hidden; background: #0e1621; }
        .photo-frame img { width: 100%; height: 100%; object-fit: cover; }
        
        .info-text h2 { color: #00d2ff; font-size: 2rem; margin: 0; text-transform: uppercase; }
        .profile-type { color: #42b72a; font-weight: 800; font-size: 1.2rem; margin: 5px 0; }
        .risk-level { color: #84a1c0; font-size: 0.9rem; }

        .terminal-box { background: #0e1621; padding: 20px; border-radius: 10px; border-left: 4px solid #42b72a; color: #42b72a; font-family: 'Courier New', monospace; font-size: 1rem; }

        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <div id="app-container">
        <div class="header-title">⚡ FRONTIER SCAN ⚡</div>

        <div id="quiz-zone">
            <h3 id="q-text" style="color: #1c1e21;">Initialisation...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="access-bar"></div>
            
            <div id="result-card">
                <span class="id-number" id="res-id">ID-61776</span>
                <span class="status-dot" id="res-status-dot">● STATUS: AUTORISÉ</span>
                
                <div class="profile-section">
                    <div class="photo-frame">
                        <img id="res-img" src="">
                    </div>
                    <div class="info-text">
                        <h2>SUJET IDENTIFIÉ</h2>
                        <p class="profile-type" id="res-type">TOURISTE</p>
                        <p class="risk-level" id="res-risk">RISQUE : BAS</p>
                    </div>
                </div>

                <p style="color: #84a1c0; font-size: 0.7rem; text-transform: uppercase; margin-bottom: 10px;">Analyse IA Terminal</p>
                <div class="terminal-box">
                    > <span id="res-note">Voyageur standard. Visa valide.</span>
                </div>
            </div>
            
            <button class="btn-option" style="margin-top:20px; background: white;" onclick="location.reload()">NOUVELLE ANALYSE</button>
        </div>
    </div>

    <script>
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/";

        const PROFILS = {
            "Touriste": { s: "AUTORISÉ", c: "#42b72a", img: "touriste.png", n: "Voyageur standard. Visa valide.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Hacker": { s: "DÉTENU", c: "#d93025", img: "hacker.png", n: "Matériel cyber-offensif détecté.", r: "CRITIQUE", msg: "🚨 ALERTE SÉCURITÉ", bc: "#ffebee" },
            "Trafiquant": { s: "INTERPELLÉ", c: "#d93025", img: "trafiquant.png", n: "Contrebande suspectée.", r: "ÉLEVÉ", msg: "🚨 INTERCEPTION", bc: "#ffebee" },
            "Exile": { s: "EN ATTENTE", c: "#fabb3a", img: "exile.png", n: "Dossier en cours d'examen.", r: "MODÉRÉ", msg: "⚠️ EXAMEN REQUIS", bc: "#fff3e0" },
            "Ananas": { s: "SAISI", c: "#d93025", img: "ananas.png", n: "Bio-organisme non identifié.", r: "BIO-RISQUE", msg: "🚫 BIO-DANGER", bc: "#ffebee" },
            "Agent": { s: "VALIDE", c: "#42b72a", img: "agent.png", n: "Mission officielle validée.", r: "AUCUN", msg: "🔓 PRIORITÉ DIPLOMATIQUE", bc: "#e8f5e9" },
            "Evasion": { s: "SIGNALÉ", c: "#fabb3a", img: "evasion.png", n: "Capitaux suspects détectés.", r: "FINANCIER", msg: "⚠️ SIGNALEMENT FISCAL", bc: "#fff3e0" },
            "Artiste": { s: "AUTORISÉ", c: "#42b72a", img: "artiste.png", n: "Profil créatif. Aucune menace.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Chercheur": { s: "CONTRÔLÉ", c: "#1877f2", img: "chercheur.png", n: "Matériel scientifique approuvé.", r: "MODÉRÉ", msg: "🔍 CONTRÔLE SCIENTIFIQUE", bc: "#e3f2fd" }
        };

        const QS = [
            { q: "Motif de passage ?", opt: [["Vacances", "Touriste"], ["Diplomatie", "Agent"], ["Optimisation", "Evasion"], ["Asile", "Exile"]] },
            { q: "Contenu des bagages ?", opt: [["Vêtements", "Touriste"], ["Serveurs", "Hacker"], ["Inconnu", "Ananas"], ["Rien", "Exile"]] },
            { q: "Profession ?", opt: [["Étudiant", "Touriste"], ["Expert Cyber", "Hacker"], ["Peintre", "Artiste"], ["Biologiste", "Chercheur"]] },
            { q: "Réaction au scanner ?", opt: [["Calme", "Agent"], ["Sueur", "Trafiquant"], ["Mépris", "Evasion"], ["Silence", "Ananas"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Evasion":0, "Artiste":0, "Chercheur":0 };

        function loadQ() {
            if (step < QS.length) {
                const curr = QS[step];
                document.getElementById("q-text").innerText = `ÉTAPE ${step + 1} : ${curr.q}`;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                curr.opt.forEach(o => {
                    const b = document.createElement("button");
                    b.className = "btn-option"; b.innerText = o[0];
                    b.onclick = () => { sc[o[1]]++; step++; loadQ(); };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-card").style.display = "block";
            const win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            const r = PROFILS[win];

            const bar = document.getElementById("access-bar");
            bar.style.display = "block";
            bar.style.background = r.bc;
            bar.style.color = r.c;
            bar.innerText = r.msg;

            document.getElementById("res-status-dot").innerText = `● STATUS: ${r.s}`;
            document.getElementById("res-status-dot").style.color = r.c;
            document.getElementById("result-card").style.borderColor = r.c;
            
            document.getElementById("res-img").src = PATH + r.img;
            document.getElementById("res-type").innerText = win.toUpperCase();
            document.getElementById("res-type").style.color = r.c;
            document.getElementById("res-risk").innerText = `RISQUE : ${r.r}`;
            document.getElementById("res-note").innerText = r.n;
            document.getElementById("res-id").innerText = "ID-" + Math.floor(10000 + Math.random() * 90000);

            if (r.s === "AUTORISÉ" || r.s === "VALIDE") {
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            } else {
                // Effet Alarme simple (vibration)
                navigator.vibrate(500);
            }
        }
        loadQ();
    </script>
</body>
</html>
"""

components.html(frontier_html, height=800, scrolling=False)
