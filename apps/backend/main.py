from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
from PIL import Image as PILImage, ImageDraw, ImageFont
import shutil, uuid

from .settings import settings
from .database import Base, engine, get_session
from .models import Image as ImageModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_PATH = Path(settings.UPLOAD_DIR)
UPLOADS_PATH.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_PATH)), name="uploads")

def public_url(filename: str) -> str:
    return f"http://localhost:8000/uploads/{filename}"

@app.get("/")
def index():
    return {"ok": True, "endpoints": ["/images", "/upload (POST)", "/reorder (POST)", "/annotate (POST)", "/uploads/*", "/docs"]}

@app.get("/images")
def list_images(db: Session = Depends(get_session)):
    rows = db.query(ImageModel).order_by(ImageModel.ord.asc(), ImageModel.id.asc()).all()
    return [{"id": r.id, "title": r.title, "url": public_url(r.filename)} for r in rows]

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...), db: Session = Depends(get_session)):
    out = []
    base_ord = db.query(ImageModel).count()
    for i, f in enumerate(files):
        ext = Path(f.filename).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        new_name = f"{uuid.uuid4().hex}{ext}"
        dest = UPLOADS_PATH / new_name
        with dest.open("wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
        row = ImageModel(filename=new_name, title=None, ord=base_ord + i)
        db.add(row); db.commit(); db.refresh(row)
        out.append({"id": row.id, "title": row.title, "url": public_url(row.filename)})
    return out

@app.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_session)):
    row = db.get(ImageModel, image_id)
    if not row:
        raise HTTPException(404, "Not found")
    (UPLOADS_PATH / row.filename).unlink(missing_ok=True)
    db.delete(row); db.commit()
    return {"ok": True}

@app.post("/reorder")
def reorder(ids: List[int], db: Session = Depends(get_session)):
    for idx, image_id in enumerate(ids):
        row = db.get(ImageModel, image_id)
        if row:
            row.ord = idx
            db.add(row)
    db.commit()
    return {"ok": True}

@app.post("/annotate")
def annotate(
    image_id: int = Form(...),
    text: str = Form(...),
    x: int = Form(20),
    y: int = Form(40),
    font_size: int = Form(42),
    color: str = Form("#ffffff"),
    db: Session = Depends(get_session)
):
    row = db.get(ImageModel, image_id)
    if not row:
        raise HTTPException(404, "Not found")
    src = UPLOADS_PATH / row.filename
    img = PILImage.open(src).convert("RGBA")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()
    draw.text((x+2, y+2), text, fill="#000000", font=font)
    draw.text((x, y), text, fill=color, font=font)
    if src.suffix.lower() in (".jpg", ".jpeg"):
        img = img.convert("RGB")
    img.save(src)
    if not row.title:
        row.title = text
        db.add(row); db.commit(); db.refresh(row)
    return {"id": row.id, "url": public_url(row.filename), "title": row.title}
