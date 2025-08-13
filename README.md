# 📸 Hyperfotopixelicious  
A drag-and-drop AI-infused image gallery with WhatsApp import, text overlay, and automatic AI captions.  
Built as a **monorepo** with:  
- **Frontend** → Next.js + Tailwind CSS (`apps/frontend`)  
- **Backend** → FastAPI + Pillow + OpenAI API (`apps/backend`)  

---

## 🚀 Features  
- **Drag & Drop** image gallery  
- **Permanent storage** of uploaded images  
- **WhatsApp self-chat import** (manual file select for now)  
- **Text overlay** tool for each image  
- **AI captions & tags** via OpenAI’s vision models  
- **Monorepo** with pnpm workspaces for unified install/run  

---

## 📂 Structure
```
hyperfotopixelicious/
├── apps/
│   ├── backend/     # FastAPI backend
│   └── frontend/    # Next.js frontend
├── package.json     # root workspace config
├── pnpm-workspace.yaml
├── Makefile         # optional: run frontend+backend together
└── .gitignore
```

---

## 🛠 Prerequisites
- **Node.js** 20+ (installed via NodeSource or nvm)  
- **pnpm** 10.14+ (enable with `corepack enable`)  
- **Python** 3.10+ (for FastAPI backend)  
- OpenAI API key (for AI captioning)

---

## 📦 Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/yourusername/hyperfotopixelicious.git
cd hyperfotopixelicious
```

### 2️⃣ Install frontend dependencies
```bash
pnpm install
```

### 3️⃣ Setup backend Python env
```bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4️⃣ Create `.env` files
- **Backend** (`apps/backend/.env`)
  ```
  OPENAI_API_KEY=your_openai_key_here
  ```
- **Frontend** (`apps/frontend/.env.local`)  
  *(optional if you have frontend-specific vars)*

---

## ▶️ Running in Development

### Run backend
```bash
cd apps/backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000
```

### Run frontend (port 3001 to avoid conflicts)
```bash
pnpm -C apps/frontend dev --port 3001
```
Then open → [http://localhost:3001](http://localhost:3001)

---

## 🧠 AI Captioning
The backend exposes `/ai/caption/{image_id}` which:  
- Sends the image to OpenAI Vision  
- Returns a short caption + 5–8 tags  
- Updates the image metadata in the gallery

---

## 📜 License
MIT — use freely, but attribution appreciated.
