from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pathlib import Path
import shutil

from models import Image
from database import init_db, get_session
from settings import settings, UPLOAD_PATH

app = FastAPI(title="Image Gallery API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static file serving for uploaded images
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_PATH)), name="uploads")

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/images", response_model=List[Image])
def list_images():
    with get_session() as s:
        return s.query(Image).order_by(Image.ord.asc(), Image.id.asc()).all()

@app.post("/upload", response_model=Image)
async def upload_image(file: UploadFile = File(...), title: str = Form("") ):
    # Save file to disk
    suffix = Path(file.filename).suffix
    if suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp", ".gif"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Give it a unique name (id will be assigned after DB insert; use temp path first)
    temp_path = UPLOAD_PATH / ("temp_" + file.filename)
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create DB row
    with get_session() as s:
        # Find next order
        max_ord = s.query(Image).order_by(Image.ord.desc()).first()
        next_ord = (max_ord.ord + 1) if max_ord else 0
        img = Image(filename=temp_path.name, title=title or Path(file.filename).stem, ord=next_ord)
        s.add(img)
        s.commit()
        s.refresh(img)

        # Finalize filename using DB id for stability
        final_name = f"{img.id}{suffix.lower()}"
        final_path = UPLOAD_PATH / final_name
        temp_path.rename(final_path)
        img.filename = final_name
        s.add(img)
        s.commit()
        s.refresh(img)
        return img

@app.put("/order", response_model=List[Image])
async def save_order(ids_in_order: List[int]):
    with get_session() as s:
        items = s.query(Image).filter(Image.id.in_(ids_in_order)).all()
        # Map for quick lookup
        order_map = {img_id: i for i, img_id in enumerate(ids_in_order)}
        for item in items:
            item.ord = order_map.get(item.id, item.ord)
            s.add(item)
        s.commit()
        return s.query(Image).order_by(Image.ord.asc(), Image.id.asc()).all()

@app.patch("/images/{image_id}", response_model=Image)
async def rename_image(image_id: int, title: str = Form(...)):
    with get_session() as s:
        item = s.get(Image, image_id)
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        item.title = title
        s.add(item)
        s.commit()
        s.refresh(item)
        return item

@app.delete("/images/{image_id}")
async def delete_image(image_id: int):
    with get_session() as s:
        item = s.get(Image, image_id)
        if not item:
            raise HTTPException(status_code=404, detail="Not found")
        # Remove file
        file_path = UPLOAD_PATH / item.filename
        if file_path.exists():
            file_path.unlink()
        s.delete(item)
        s.commit()
        return {"ok": True}