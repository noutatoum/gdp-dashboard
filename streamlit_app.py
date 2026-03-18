import streamlit as st
import random

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="FRONTIER AI SCAN", page_icon="🛂", layout="centered")

# --- 2. DESIGN GRAPHIQUE PRO (CSS mis à jour) ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f5; }
    h1 { color: #1877f2; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; }
    
    /* Boutons de réponse */
    div.stButton > button {
        background-color: white; color: #1877f2; border: 2px solid #1877f2;
        border-radius: 15px; height: 3.5rem; font-weight: bold; font-size: 1.1rem;
        transition: 0.3s; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 10px;
    }
    div.stButton > button:hover { background-color: #1877f2; color: white; transform: translateY(-3px); }

    /* La Carte de Résultat Finale */
    .id-card {
        background: white; border-radius: 25px; padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-top: 12px solid #1877f2;
        margin-top: 20px; font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Badges de Statut Dynamiques */
    .status-ok { color: #42b72a; font-weight: bold; text-transform: uppercase; }
    .status-warn { color: #fabb3a; font-weight: bold; text-transform: uppercase; }
    .status-danger { color: #d93025; font-weight: bold; text-transform: uppercase; }
    
    .label { color: #606770; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; margin-bottom: 2px; }
    .value { color: #1c1e21; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. BASE DE DONNÉES DYNAMIQUE (Génération d'identité) ---
def generer_identite():
    prenoms = ["Nour", "Jean", "Sarah", "Alex", "Luna", "Liam", "Geoffrey"]
    noms = ["Al-Fayed", "Dupont", "Smith", "Wang", "Müller", "Gomez"]
    origines = ["Zone-A (Urbaine)", "Zone-B (Rurale)", "Zone-C (Haute Sécurité)", "Zone-D (Extérieure)"]
    
    return {
        "nom": f"{random.choice(prenoms)} {random.choice(noms)}",
        "origine": random.choice(origines),
        "id_scan": f"#SCAN-{random.randint(10000, 99999)}"
    }

# --- 4. BASE DE DONNÉES DES PROFILS (Logique de décision & Images) ---
# NOTE POUR TOI, NOUR : Pour mettre une vraie photo, remplace l'emoji par :
# "image": "https://url-de-ton-image.com/photo.jpg",
PROFILS = {
    "Touriste": {
        "decision": "AUTORISÉ", "risk": "BAS", "color": "status-ok",
        "image": "https://img.icons8.com/emoji/150/camera-with-flash-emoji.png",
        "note": "Aucun antécédent. Sujet en règle."
    },
    "Hacker": {
        "decision": "REFUSÉ / DÉTENU", "risk": "CRITIQUE", "color": "status-danger",
        "image": "https://img.icons8.com/emoji/150/technologist-emoji.png",
        "note": "Matériel cyber-offensif détecté. Tentative d'intrusion réseau."
    },
    "Trafiquant": {
        "decision": "REFUSÉ / INTERPELLÉ", "risk": "ÉLEVÉ", "color": "status-danger",
        "image": "https://img.icons8.com/emoji/150/package-emoji.png",
        "note": "Contrebande détectée via scanner THz."
    },
    "Exilé": {
        "decision": "EN ATTENTE D'ASILE", "risk": "MODÉRÉ", "color": "status-warn",
        "image": "https://img.icons8.com/emoji/150/shield-emoji.png",
        "note": "Vérification des documents de protection en cours."
    },
    "Ananas": {
        "decision": "SAISI / DÉTRUIT", "risk": "BIO-RISQUE", "color": "status-danger",
        "image": "https://img.icons8.com/emoji/150/pineapple-emoji.png",
        "note": "Matériel biologique non identifié. Protocole de quarantaine."
    },
    "Agent": {
        "decision": "AUTORISÉ (Transit)", "risk": "AUCUN", "color": "status-ok",
        "image": "https://img.icons8.com/emoji/150/police-officer.png",
        "note": "Agent en mission officielle. Code de transit validé."
    }
}

# --- 5. LOGIQUE & QUESTIONS ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.passager = generer_identite() # On génère l'identité au début
    st.session_state.scores = {k: 0 for k in PROFILS.keys()}

QUESTIONS = [
    ("Motif principal de votre passage ?", [("Aide Humanitaire", "Agent"), ("Vacances", "Touriste"), ("Affaires confidentielles", "Hacker"), ("Asile", "Exilé")]),
    ("Objectif après la frontière ?", [("Installation", "Exilé"), ("Transit rapide", "Agent"), ("Recherche / Exploration", "Hacker"), ("Inconnu", "Ananas")]),
    ("Ressources financières ?", [("Cryptomonnaies", "Hacker"), ("Standard / Cash", "Touriste"), ("Faibles", "Exilé"), ("Néant", "Ananas")]),
    ("Document présenté ?", [("Passeport Bio", "Touriste"), ("Diplomatique", "Agent"), ("Abîmé / Faux", "Exilé"), ("Aucun", "Ananas")]),
    ("Objets suspects ?", [("Laptop chiffré", "Hacker"), ("Contrebande", "Trafiquant"), ("Arme", "Ananas"), ("Aucun", "Agent")]),
    ("Réaction au scanner ?", [("Arrogance", "Hacker"), ("Nervosité", "Trafiquant"), ("Vigilance", "Agent"), ("Silence", "Ananas")])
]

st.markdown("<h1>🛂 FRONTIER AI SCAN v1.0</h1>", unsafe_allow_html=True)

if st.session_state.step < len(QUESTIONS):
    # QUESTIONNAIRE (Visuel actuel sur ton iPhone image_0.png)
    st.progress(st.session_state.step / len(QUESTIONS))
    
    q_text, options = QUESTIONS[st.session_state.step]
    st.markdown(f"### PROTOCOLE D'ANALYSE {st.session_state.step + 1}/{len(QUESTIONS)}")
    st.subheader(q_text)
    
    for text, category in options:
        if st.button(text):
            st.session_state.scores[category] += 1
            st.session_state.step += 1
            st.rerun()

else:
    # RÉSULTAT FINAL DYNAMIQUE (Basé sur image_2.png mais amélioré)
    gagnant = max(st.session_state.scores, key=st.session_state.scores.get)
    resultat = PROFILS[gagnant]
    passager = st.session_state.passager

    st.markdown(f"""
        <div class="id-card">
            <div style="display: flex; justify-content: space-between;">
                <span class="{resultat['color']}">● {resultat['decision']}</span>
                <span style="color:#606770;">ID {passager['id_scan']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 30px; margin-top: 30px;">
                <img src="{resultat['image']}" style="width: 120px; height: 120px; border-radius: 50%; border: 4px solid #1877f2; background:#f0f2f5; padding:5px;">
                <div>
                    <h2 style="margin:0; color:#1c1e21; font-family: Segoe UI;">{passager['nom']}</h2>
                    <p style="color:#606770; margin:0;">ORIGINE : {passager['origine']}</p>
                    <p style="color:#1877f2; font-weight: bold; font-size: 1.2rem; margin:5px 0 0 0;">PROFIL : {gagnant.upper()}</p>
                </div>
            </div>
            <hr style="border: 0.5px solid #eee; margin: 30px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <p class="label">Statut Décisionnel</p>
                    <p class="value {resultat['color']}">{resultat['decision']}</p>
                </div>
                <div>
                    <p class="label">Niveau de Risque</p>
                    <p class="value">{resultat['risk']}</p>
                </div>
            </div>
            <p class="label">Insights de l'IA de Sécurité</p>
            <p class="value" style="font-style: italic;">{resultat['note']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("NOUVEAU SCANNER"):
        st.session_state.step = 0
        st.session_state.passager = generer_identite() # On régénère une identité
        st.session_state.scores = {k: 0 for k in PROFILS.keys()}
        st.rerun()
