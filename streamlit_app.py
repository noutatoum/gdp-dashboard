import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="FRONTIER SCAN v1.2", layout="centered")

frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; display: flex; justify-content: center; padding: 20px; margin: 0; }
        #app-container { width: 100%; max-width: 600px; text-align: center; }
        .header-title { color: #00d2ff; font-size: 2.2rem; font-weight: 800; margin-bottom: 20px; }
        
        .progress-container { width: 100%; background-color: #ddd; border-radius: 10px; margin-bottom: 25px; height: 12px; overflow: hidden; }
        .progress-bar { height: 100%; background-color: #00d2ff; width: 0%; transition: 0.4s ease-out; }

        .btn-option { width: 100%; padding: 16px; margin: 10px 0; background: white; color: #1c1e21; border: 1px solid #ddd; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .btn-option:hover { background: #f0f2f5; border-color: #00d2ff; transform: translateY(-2px); }

        #access-bar { display: none; width: 100%; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-weight: bold; text-align: left; font-size: 1.1rem; border-left: 5px solid; }
        
        #result-card { display: none; background: #1b2838; border-radius: 20px; padding: 30px; border-bottom: 6px solid #42b72a; text-align: left; position: relative; animation: slideUp 0.6s ease; }
        
        .id-number { position: absolute; top: 20px; right: 25px; color: white; opacity: 0.6; font-family: monospace; }
        
        /* CADRE POUR EMOJI */
        .emoji-frame { width: 120px; height: 120px; border-radius: 20px; border: 3px solid #42b72a; background: #0e1621; display: flex; align-items: center; justify-content: center; font-size: 4rem; flex-shrink: 0; }
        
        .info-text h2 { color: #00d2ff; font-size: 1.7rem; margin: 0; text-transform: uppercase; }
        .profile-type { font-weight: 800; font-size: 1.3rem; margin: 8px 0; }
        .risk-level { font-size: 0.95rem; font-weight: bold; text-transform: uppercase; }

        .terminal-box { background: #0e1621; padding: 18px; border-radius: 12px; border-left: 4px solid #42b72a; color: #42b72a; font-family: 'Courier New', monospace; font-size: 1rem; margin-top: 15px; }

        #restart-btn { display: none; width: 100%; padding: 15px; margin-top: 25px; background: #00d2ff; color: white; border: none; border-radius: 12px; font-weight: bold; cursor: pointer; }

        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">⚡ FRONTIER SCAN ⚡</div>
        
        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="color: #1c1e21;">Initialisation...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="access-bar"></div>
            <div id="result-card">
                <span class="id-number" id="res-id"></span>
                <div style="display:flex; gap:25px; align-items:center;">
                    <div id="res-emoji" class="emoji-frame"></div>
                    <div class="info-text">
                        <h2>SUJET IDENTIFIÉ</h2>
                        <p class="profile-type" id="res-type"></p>
                        <p class="risk-level" id="res-risk"></p>
                    </div>
                </div>
                <div class="terminal-box">> <span id="res-note"></span></div>
            </div>
            <button id="restart-btn" onclick="location.reload()">RESCANNER UN NOUVEAU SUJET</button>
        </div>
    </div>

    <script>
        const PROFILS = {
            "Touriste": { s: "AUTORISÉ", c: "#42b72a", emoji: "✈️", n: "Voyageur standard. Documents valides.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Hacker": { s: "REFUSÉ", c: "#d93025", emoji: "💻", n: "Outils d'intrusion détectés.", r: "ÉLEVÉ", msg: "🚨 ACCÈS REFUSÉ", bc: "#ffebee" },
            "Trafiquant": { s: "REFUSÉ", c: "#d93025", emoji: "📦", n: "Marchandises non déclarées.", r: "ÉLEVÉ", msg: "🚨 ACCÈS REFUSÉ", bc: "#ffebee" },
            "Exile": { s: "EN ATTENTE", c: "#fabb3a", emoji: "🛡️", n: "Demande de protection à examiner.", r: "MODÉRÉ", msg: "⚠️ EXAMEN REQUIS", bc: "#fff3e0" },
            "Ananas": { s: "SAISI", c: "#d93025", emoji: "🍍", n: "Bio-danger non identifié.", r: "CRITIQUE", msg: "🚫 BIO-ALERTE", bc: "#ffebee" },
            "Agent": { s: "VALIDE", c: "#42b72a", emoji: "🕶️", n: "Mission officielle confirmée.", r: "BAS", msg: "🔓 PRIORITÉ DIPLOMATIQUE", bc: "#e8f5e9" },
            "Artiste": { s: "AUTORISÉ", c: "#42b72a", emoji: "🎨", n: "Âme créative. Profil sans danger.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Chercheur": { s: "CONTRÔLÉ", c: "#1877f2", emoji: "🧪", n: "Matériel scientifique certifié.", r: "MODÉRÉ", msg: "🔍 CONTRÔLE SCIENTIFIQUE", bc: "#e3f2fd" },
            "Evasion": { s: "SIGNALÉ", c: "#fabb3a", emoji: "💰", n: "Flux de capitaux suspects.", r: "ÉLEVÉ", msg: "⚠️ SIGNALEMENT FISCAL", bc: "#fff3e0" }
        };

        const QS = [
            { q: "1. Motif déclaré du séjour ?", opt: [["Vacances", "Touriste"], ["Recherche", "Chercheur"], ["Mission diplomatique", "Agent"], ["Asile", "Exile"]] },
            { q: "2. Contenu principal des bagages ?", opt: [["Vêtements", "Touriste"], ["Matériel informatique", "Hacker"], ["Outils de dessin", "Artiste"], ["Produits non identifiés", "Ananas"]] },
            { q: "3. Quel est votre domaine d'expertise ?", opt: [["Art et Design", "Artiste"], ["Informatique", "Hacker"], ["Sciences", "Chercheur"], ["Commerce international", "Evasion"]] },
            { q: "4. Provenance de vos fonds ?", opt: [["Salaire", "Touriste"], ["Épargne personnelle", "Artiste"], ["Investissements", "Evasion"], ["Budget d'État", "Agent"]] },
            { q: "5. Votre réaction face au scan corporel ?", opt: [["Coopératif", "Agent"], ["Amusé", "Artiste"], ["Nerveux", "Trafiquant"], ["Indifférent", "Hacker"]] },
            { q: "6. Destination finale de votre voyage ?", opt: [["Hôtel", "Touriste"], ["Laboratoire", "Chercheur"], ["Zone de commerce", "Evasion"], ["Inconnue", "Ananas"]] },
            { q: "7. Que pensez-vous des lois frontalières ?", opt: [["Nécessaires", "Agent"], ["Obsolètes", "Hacker"], ["Poétiques", "Artiste"], ["Contraignantes", "Exile"]] },
            { q: "8. Quel est votre dernier diplôme ?", opt: [["Doctorat / Master", "Chercheur"], ["Licence", "Touriste"], ["École d'Art", "Artiste"], ["Aucun / Autodidacte", "Hacker"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Artiste":0, "Chercheur":0, "Evasion":0 };

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
                    b.onclick = () => { sc[o[1]] += 10; step++; loadQ(); };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-card").style.display = "block";
            document.getElementById("restart-btn").style.display = "block";

            const win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            const r = PROFILS[win];

            const bar = document.getElementById("access-bar");
            bar.style.display = "block"; bar.style.background = r.bc; bar.style.color = r.c; bar.innerText = r.msg;

            document.getElementById("res-emoji").innerText = r.emoji;
            document.getElementById("res-emoji").style.borderColor = r.c;
            document.getElementById("res-type").innerText = win === "Artiste" ? "ÂME CRÉATIVE" : win.toUpperCase();
            document.getElementById("res-type").style.color = r.c;
            document.getElementById("res-risk").innerText = `NIVEAU DE RISQUE : ${r.r}`;
            document.getElementById("res-risk").style.color = r.c;
            document.getElementById("res-note").innerText = r.n;
            document.getElementById("res-id").innerText = "ID-" + Math.floor(10000 + Math.random() * 90000);
            document.getElementById("result-card").style.borderColor = r.c;

            if (r.r === "BAS") {
                confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
            }
        }
        loadQ();
    </script>
</body>
</html>
"""

components.html(frontier_html, height=850, scrolling=False)
