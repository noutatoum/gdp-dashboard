import streamlit as st
import streamlit.components.v1 as components

# 1. Configuration de l'onglet du navigateur
st.set_page_config(page_title="FRONTIER SCAN v1.0", layout="centered")

# 2. On définit le bloc HTML/JS complet
frontier_html = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f8f9fa; display: flex; justify-content: center; padding: 20px; margin: 0; }
        #app-container { width: 100%; max-width: 600px; text-align: center; }
        
        .header-title { color: #00d2ff; font-size: 2.5rem; font-weight: 800; margin-bottom: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
        
        /* Barre de progression */
        .progress-container { width: 100%; background-color: #ddd; border-radius: 10px; margin-bottom: 25px; height: 12px; overflow: hidden; border: 1px solid #ccc; }
        .progress-bar { height: 100%; background-color: #00d2ff; width: 0%; transition: 0.4s ease-out; }

        /* Style des boutons de choix */
        .btn-option { width: 100%; padding: 16px; margin: 10px 0; background: white; color: #1c1e21; border: 1px solid #ddd; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .btn-option:hover { background: #f0f2f5; border-color: #00d2ff; transform: translateY(-2px); }

        /* BANDEAU DE STATUT (EN HAUT DU RÉSULTAT) */
        #access-bar { display: none; width: 100%; padding: 15px; border-radius: 12px; margin-bottom: 15px; font-weight: bold; text-align: left; font-size: 1.1rem; border-left: 5px solid; }
        
        /* CARTE DE RÉSULTAT NOIRE */
        #result-card { display: none; background: #1b2838; border-radius: 20px; padding: 30px; border-bottom: 6px solid #42b72a; text-align: left; position: relative; animation: slideUp 0.6s cubic-bezier(0.23, 1, 0.32, 1); }
        
        .id-number { position: absolute; top: 20px; right: 25px; color: white; opacity: 0.6; font-family: monospace; font-size: 1.1rem; }
        .status-dot { font-weight: bold; margin-bottom: 20px; display: block; font-size: 1rem; }
        
        .profile-section { display: flex; gap: 25px; align-items: center; margin-bottom: 30px; }
        .photo-frame { width: 190px; height: 190px; border-radius: 18px; border: 3px solid #42b72a; overflow: hidden; background: #0e1621; flex-shrink: 0; }
        
        /* CADRAGE PHOTO PARFAIT */
        .photo-frame img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            object-position: center top; 
        }
        
        .info-text h2 { color: #00d2ff; font-size: 1.9rem; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
        .profile-type { font-weight: 800; font-size: 1.3rem; margin: 8px 0; letter-spacing: 1px; }
        .risk-level { color: #84a1c0; font-size: 0.95rem; font-weight: bold; }

        .terminal-box { background: #0e1621; padding: 18px; border-radius: 12px; border-left: 4px solid #42b72a; color: #42b72a; font-family: 'Courier New', monospace; font-size: 1.05rem; line-height: 1.4; }

        #restart-btn { display: none; width: 100%; padding: 15px; margin-top: 25px; background: #00d2ff; color: white; border: none; border-radius: 12px; font-weight: bold; font-size: 1.1rem; cursor: pointer; }

        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <div id="app-container">
        <div class="header-title">⚡ FRONTIER SCAN ⚡</div>

        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="color: #1c1e21; font-size: 1.4rem; margin-bottom: 25px;">Initialisation...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="access-bar"></div>
            
            <div id="result-card">
                <span class="id-number" id="res-id">ID-00000</span>
                <span class="status-dot" id="res-status-dot">● STATUS: ANALYSE</span>
                
                <div class="profile-section">
                    <div class="photo-frame">
                        <img id="res-img" src="" alt="Sujet">
                    </div>
                    <div class="info-text">
                        <h2>SUJET IDENTIFIÉ</h2>
                        <p class="profile-type" id="res-type">TYPE</p>
                        <p class="risk-level" id="res-risk">RISQUE : ---</p>
                    </div>
                </div>

                <p style="color: #84a1c0; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 10px; font-weight: bold;">Analyse IA Terminal</p>
                <div class="terminal-box">
                    > <span id="res-note">Traitement des données biométriques...</span>
                </div>
            </div>
            
            <button id="restart-btn" onclick="location.reload()">RESCANNER UN NOUVEAU SUJET</button>
        </div>
    </div>

    <script>
        // LIEN GITHUB VERS TES IMAGES PNG
        const PATH = "https://raw.githubusercontent.com/noutatoum/gdp-dashboard/main/MonScanner/";

        const PROFILS = {
            "Touriste": { s: "AUTORISÉ", c: "#42b72a", img: "touriste.png", n: "Voyageur standard identifié. Visa et documents en règle.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Hacker": { s: "DÉTENU", c: "#d93025", img: "hacker.png", n: "Matériel cyber-offensif détecté. Tentative d'intrusion réseau.", r: "CRITIQUE", msg: "🚨 ALERTE SÉCURITÉ", bc: "#ffebee" },
            "Trafiquant": { s: "INTERPELLÉ", c: "#d93025", img: "trafiquant.png", n: "Contrebande suspectée. Unité de fouille prévenue.", r: "ÉLEVÉ", msg: "🚨 INTERCEPTION DOUANE", bc: "#ffebee" },
            "Exile": { s: "EN ATTENTE", c: "#fabb3a", img: "exile.png", n: "Dossier humanitaire en cours. Sujet placé en zone de transit.", r: "MODÉRÉ", msg: "⚠️ EXAMEN REQUIS", bc: "#fff3e0" },
            "Ananas": { s: "SAISI", c: "#d93025", img: "ananas.png", n: "Bio-organisme non identifié. Risque de contamination.", r: "BIO-RISQUE", msg: "🚫 BIO-DANGER DÉTECTÉ", bc: "#ffebee" },
            "Agent": { s: "VALIDE", c: "#42b72a", img: "agent.png", n: "Mission officielle validée par l'État. Priorité diplomatique.", r: "AUCUN", msg: "🔓 PRIORITÉ DIPLOMATIQUE", bc: "#e8f5e9" },
            "Evasion": { s: "SIGNALÉ", c: "#fabb3a", img: "evasion.png", n: "Capitaux suspects. Signalement transmis aux autorités fiscales.", r: "FINANCIER", msg: "⚠️ SIGNALEMENT FISCAL", bc: "#fff3e0" },
            "Artiste": { s: "AUTORISÉ", c: "#42b72a", img: "artiste.png", n: "Sujet créatif identifié. Aucune menace pour la sécurité.", r: "BAS", msg: "🔓 ACCÈS ACCORDÉ", bc: "#e8f5e9" },
            "Chercheur": { s: "CONTRÔLÉ", c: "#1877f2", img: "chercheur.png", n: "Matériel scientifique certifié. Transport sous protocole.", r: "MODÉRÉ", msg: "🔍 CONTRÔLE SCIENTIFIQUE", bc: "#e3f2fd" }
        };

        const QS = [
            { q: "Motif principal de passage ?", opt: [["Vacances / Tourisme", "Touriste"], ["Mission Étatique", "Agent"], ["Optimisation financière", "Evasion"], ["Asile politique", "Exile"]] },
            { q: "Contenu des bagages ?", opt: [["Effets personnels", "Touriste"], ["Unités centrales chiffrées", "Hacker"], ["Spécimen végétal inconnu", "Ananas"], ["Toiles et pinceaux", "Artiste"]] },
            { q: "Profession déclarée ?", opt: [["Étudiant / Salarié", "Touriste"], ["Monsieur d'affaires / Trader", "Evasion"], ["Artiste indépendant", "Artiste"], ["Scientifique / Biologiste", "Chercheur"]] },
            { q: "Réaction face au scanner ?", opt: [["Calme absolu", "Agent"], ["Signes de stress intense", "Trafiquant"], ["Arrogance / Dédain", "Evasion"], ["Confusion totale", "Ananas"]] },
            { q: "Type de document présenté ?", opt: [["Passeport Biométrique", "Touriste"], ["Passeport Diplomatique", "Agent"], ["Document déchiré / Absent", "Exile"], ["Faux document détecté", "Trafiquant"]] },
            { q: "Équipements électroniques ?", opt: [["Smartphone standard", "Touriste"], ["Équipement médical pro", "Chercheur"], ["Matériel d'espionnage", "Hacker"], ["Appareil photo pro", "Artiste"]] },
            { q: "Ressources financières ?", opt: [["Salaire mensuel fixe", "Touriste"], ["Comptes Offshore / Crypto", "Evasion"], ["Actifs anonymes (Monero)", "Hacker"], ["Néant / Sans ressources", "Exile"]] },
            { q: "Destination du séjour ?", opt: [["Hôtel / Location", "Touriste"], ["Ambassade / Consulat", "Agent"], ["Banque privée", "Evasion"], ["Centre de recherche", "Chercheur"]] },
            { q: "Durée prévue du séjour ?", opt: [["1 à 2 semaines", "Touriste"], ["Durée indéfinie", "Exile"], ["Transit 48 heures", "Agent"], ["Escale technique 24h", "Ananas"]] },
            { q: "Provenance géographique ?", opt: [["Zone sécurisée (Schengen)", "Touriste"], ["Zone de conflit armé", "Exile"], ["Pays sous embargo", "Hacker"], ["Provenance non répertoriée", "Ananas"]] }
        ];

        let step = 0;
        let sc = { "Touriste":0, "Hacker":0, "Trafiquant":0, "Exile":0, "Ananas":0, "Agent":0, "Evasion":0, "Artiste":0, "Chercheur":0 };

        function loadQ() {
            if (step < QS.length) {
                const curr = QS[step];
                document.getElementById("p-bar").style.width = ((step / QS.length) * 100) + "%";
                document.getElementById("q-text").innerText = `ÉTAPE ${step + 1} / 10 : ${curr.q}`;
                const zone = document.getElementById("options-zone");
                zone.innerHTML = "";
                curr.opt.forEach(o => {
                    const b = document.createElement("button");
                    b.className = "btn-option"; b.innerText = o[0];
                    b.onclick = () => { sc[o[1]] += 15; step++; loadQ(); };
                    zone.appendChild(b);
                });
            } else { finish(); }
        }

        function finish() {
            document.getElementById("quiz-zone").style.display = "none";
            document.getElementById("result-card").style.display = "block";
            document.getElementById("restart-btn").style.display = "block";

            let win = Object.keys(sc).reduce((a, b) => sc[a] > sc[b] ? a : b);
            const r = PROFILS[win];

            const bar = document.getElementById("access-bar");
            bar.style.display = "block"; 
            bar.style.background = r.bc; 
            bar.style.color = r.c; 
            bar.style.borderColor = r.c;
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
                confetti({ particleCount: 200, spread: 80, origin: { y: 0.6 } });
            }
        }
        loadQ();
    </script>
</body>
</html>
"""

# 3. Injection du code final dans l'interface Streamlit
components.html(frontier_html, height=900, scrolling=False)
