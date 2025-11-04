# python-editor

## Popis
Jednoduchý projekt: FastAPI backend + statický frontend (HTML/JS). Backend používa PostgreSQL a Judge0 (cez RapidAPI) na bezpečné spúšťanie Python kódu.

## Štruktúra
```
python-editor/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── start.sh
│   └── render.yaml
└── frontend/
    └── index.html
```

## Rýchle kroky (nasadenie na Render)
1. Nahraj tento projekt do GitHub repozitára.
2. V Render -> New -> Web Service -> vyber repozitár a priečinok `backend/`.
   - Render načíta `render.yaml` a vytvorí službu + PostgreSQL databázu.
3. V Settings -> Environment add:
   - `JUDGE0_API_KEY` = tvoj RapidAPI kľúč (viď nižšie).
   - (voliteľné) `FRONTEND_URL` = URL kde bude hostovaný frontend (napr. https://moja-frontenda.onrender.com) — použije sa pre CORS.
4. Po nasadení skopíruj URL služby (napr. `https://python-editor-backend.onrender.com`).

## RapidAPI (Judge0) — ako získať kľúč
1. Choď na https://rapidapi.com/judge0-official/api/judge0-ce/
2. Prihlás sa / zaregistruj.
3. Klikni na **Subscribe** pre bezplatný plán.
4. V pravom paneli nájdeš `x-rapidapi-key` — túto hodnotu vlož do `JUDGE0_API_KEY` v Render Environment.

## Frontend
- `frontend/index.html` je samostatná statická stránka. Pred nasadením uprav `API_URL` v JS na URL backendu (napr. https://python-editor-backend.onrender.com).
- Frontend môžeš hostovať ako Static Site na Render, alebo na Netlify/Vercel.

## Lokálne testovanie (bez Render)
1. Vytvor a aktivuj virtuálne prostredie:
   ```
   python -m venv venv
   source venv/bin/activate  # alebo venv\Scripts\activate na Windows
   pip install -r backend/requirements.txt
   ```
2. Spusti backend:
   ```
   cd backend
   export JUDGE0_API_KEY=...   # alebo nastav v .env
   uvicorn main:app --reload
   ```
3. Otvor `frontend/index.html` lokálne (alebo použij jednoduchý static server).

## Poznámky o bezpečnosti
- Kód sa vykonáva výhradne cez Judge0 sandbox (nikdy nie lokálne na serveri).
- Nastav `FRONTEND_URL` na presnú URL frontendu namiesto wildcardu `*`.
- Sleduj používanie API a pridaj rate-limiting podľa potreby.
