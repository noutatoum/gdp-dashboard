# **CODE FINAL COMPLET - PRÊT À COPIER/COLLER** 🚀

```python
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
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            display: flex;
            justify-content: center;
            padding: 20px;
            margin: 0;
            min-height: 100vh;
        }
        #app-container {
            width: 100%;
            max-width: 650px;
            text-align: center;
        }
        .header-title {
            color: #00d2ff;
            font-size: 2.8rem;
            font-weight: 800;
            margin-bottom: 25px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { text-shadow: 2px 2px 4px rgba(0,0,0,0.2), 0 0 10px #00d2ff; }
            to { text-shadow: 2px 2px 4px rgba(0,0,0,0.2), 0 0 20px #00d2ff; }
        }
        .progress-container {
            width: 100%;
            background-color: #e0e0e0;
            border-radius: 15px;
            margin-bottom: 30px;
            height: 14px;
            overflow: hidden;
            border: 2px solid #ddd;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #00d2ff, #0099cc);
            width: 0%;
            transition: 0.5s cubic-bezier(0.23, 1, 0.32, 1);
            box-shadow: 0 0 10px rgba(0,210,255,0.5);
        }
        .btn-option {
            width: 100%;
            padding: 18px;
            margin: 12px 0;
            background: white;
            color: #1c1e21;
            border: 2px solid #e4e6ea;
            border-radius: 15px;
            font-size: 1.15rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .btn-option:hover {
            background: linear-gradient(135deg, #f0f2f5, #e4e6ea);
            border-color: #00d2ff;
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,210,255,0.3);
        }
        .btn-option:active {
            transform: translateY(-1px);
        }
        #access-bar {
            display: none;
            width: 100%;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            font-weight: 800;
            text-align: left;
            font-size: 1.2rem;
            border-left: 6px solid;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        #result-card {
            display: none;
            background: linear-gradient(145deg, #1b2838, #0f1a26);
            border-radius: 25px;
            padding: 35px;
            border-bottom: 8px solid #42b72a;
            text-align: left;
            position: relative;
            animation: slideUp 0.8s cubic-bezier(0.23, 1, 0.32, 1);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        .id-number {
            position: absolute;
            top: 25px;
            right: 30px;
            color: #00d2ff;
            opacity: 0.8;
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            font-weight: bold;
        }
        .photo-frame {
            width: 200px;
            height: 200px;
            border-radius: 20px;
            border: 4px solid #42b72a;
            overflow: hidden;
            background: linear-gradient(145deg, #0e1621, #1a2332);
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(66,183,42,0.3);
        }
        .photo-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center top;
            display: block;
        }
        .fallback-text {
            display: none;
            color: #84a1c0;
            font-size: 1rem;
            text-align: center;
            padding: 15px;
            font-weight: 500;
        }
        .info-text h2 {
            color: #00d2ff;
            font-size: 2.1rem;
            margin: 0 0 10px 0;
            text-transform: uppercase;
            font-weight: 900;
            letter-spacing: 2px;
        }
        .profile-type {
            font-weight: 900;
            font-size: 1.5rem;
            margin: 12px 0;
        }
        .terminal-box {
            background: linear-gradient(145deg, #0e1621, #1a2332);
            padding: 22px;
            border-radius: 15px;
            border-left: 5px solid #42b72a;
            color: #42b72a;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }
        #restart-btn {
            display: none;
            width: 100%;
            padding: 18px;
            margin-top: 30px;
            background: linear-gradient(135deg, #00d2ff, #0099cc);
            color: white;
            border: none;
            border-radius: 15px;
            font-weight: 800;
            font-size: 1.2rem;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 8px 25px rgba(0,210,255,0.4);
        }
        #restart-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 35px rgba(0,210,255,0.6);
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(50px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div id="app-container">
        <div class="header-title">⚡ FRONTIER SCAN v1.2 ⚡</div>

        <div id="quiz-zone">
            <div class="progress-container"><div id="p-bar" class="progress-bar"></div></div>
            <h3 id="q-text" style="color: #1c1e21; font-size: 1.3rem; font-weight: 700;">Analyse en cours...</h3>
            <div id="options-zone"></div>
        </div>

        <div id="result-zone">
            <div id="access-bar"></div>

            <div id="result-card">
                <span class="id-number" id="res-id"></span>

                <div style="display:flex; gap:30px; align-items:center; margin-bottom:35px;">
                    <div class="photo-frame">
                        <img id="res-img" src="" alt="Sujet">
                        <div id="img-fallback" class="fallback-text">🔍 IMAGE EN COURS DE CHARGEMENT</div>
                    </div>
                    <div class="info-text">
                        <h2>SUJET IDENTIFIÉ</h2>
                        <p class="profile-type" id="res-type"></p>
                        <p id="res-risk" style="color:#84a1c0; font-size:1.1rem; font-weight:700; margin:5px 0;"></p>
                    </div>
                </div>

                <div class="terminal-box">> <span id="res-note"></span></div>
            </div>

            <button id="restart-btn" onclick="location.reload()">🔄 RESCANNER NOUVEAU SUJET</button>
        </div>
    </div>

    <script>
        // IMAGES SVG EN BASE64 - AUCUN LIEN EXTERNE REQUIS !
        const SVG_IMAGES = {
            "Touriste": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjNDJiNzJhIiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI4MCIgcj0iNDAiIGZpbGw9IiNmZmYiIHN0cm9rZT0iIzAwZDJmZiIgc3Ryb2tlLXdpZHRoPSI0Ii8+PHRleHQgeD0iMTAwIiB5PSIxNDAiIGZvbnQtc2l6ZT0iMTgiIGZpbGw9IiMwMGQyZmYiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5UT1VSSVNURTwvdGV4dD48L3N2Zz4=",
            "Hacker": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZDkzMDI1IiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI4MCIgcj0iMzUiIGZpbGw9IiNmZmYiIHN0cm9rZT0iIzAwZDJmZiIgc3Ryb2tlLXdpZHRoPSIzIi8+PHRleHQgeD0iMTAwIiB5PSIxNDAiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IndoaXRlIiBmb250LXdlaWdodD0iYm9sZCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+SENLRUVSPC90ZXh0Pjx0ZXh0IHg9IjUwIiB5PSIxNjAiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiNmZmYiIGZvbnQtZmFtaWx5PSdDb3VyaWVyJz4kPC90ZXh0Pjwvc3ZnPg==",
            "Trafiquant": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZDkzMDI1IiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI4MCIgcj0iNDAiIGZpbGw9IiNmZmYiIHN0cm9rZT0iI2Q5MzAyNSIgc3Ryb2tlLXdpZHRoPSI0Ii8+PHRleHQgeD0iMTAwIiB5PSIxNDAiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IndoaXRlIiBmb250LXdlaWdodD0iYm9sZCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+VFJBRklJQU5UPHRleHQ+PHJlY3QgeD0iNjAiIHk9IjE1MCIgd2lkdGg9IjgwIiBoZWlnaHQ9IjE1IiBmaWxsPSIjZGRkIiByeD0iOCIvPjwvc3ZnPg==",
            "Exile": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZmFiYjNhIiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI4MCIgcj0iMzgiIGZpbGw9IiNmZmYiIHN0cm9rZT0iIzAwZDJmZiIgc3Ryb2tlLXdpZHRoPSIzIi8+PHRleHQgeD0iMTAwIiB5PSIxNDAiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiMwMGQyZmYiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5FWElMRS90ZXh0Pjwvc3ZnPg==",
            "Ananas": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZDkzMDI1IiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI3MCIgcj0iNDUiIGZpbGw9IiNmZmY4MDAiIHN0cm9rZT0iI2ZmZDAwMCIgc3Ryb2tlLXdpZHRoPSI0Ii8+PHBhdGggZD0iTTkwLDEyMEw5NSwxMTVMMTAwLDExNUwxMDUsMTE1TDEwLDEyMCIgZmlsbD0iI2ZmYjAwMCIgc3Ryb2tlPSIjZmZkMDAwIiBzdHJva2Utd2lkdGg9IjIiLz48dGV4dCB4PSIxMDAiIHk9IjE2NSIgZm9udC1zaXplPSIxNCIgZmlsbD0id2hpdGUiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BTkFOQVM8L3RleHQ+PC9zdmc+",
            "Agent": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjNDJiNzJhIiByeD0iMjAiLz48Y2lyY2xlIGN4PSIxMDAiIGN5PSI4MCIgcj0iNDAiIGZpbGw9IiNmZmYiIHN0cm9rZT0iIzAwZDJmZiIgc3Ryb2tlLXdpZHRoPSI0Ii8+PHRleHQgeD0iMTAwIiB5PSIxNDAiIGZvbnQtc2l6ZT0iMTYiIGZpbGw9IiMwMGQyZmYiIGZvbnQtd2VpZ2h0PSJib2xkIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5BR0VOVDwvdGV4dD48L3N2Zz4=",
            "Artiste": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIx
