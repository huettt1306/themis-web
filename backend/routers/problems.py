# backend/routers/problems.py
import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/problems", tags=["problems"])

DOWNLOADS_PATH = r"..\downloads"

def safe_filename(base_name: str) -> str:
    """Loại bỏ ký tự nguy hiểm trong tên file"""
    return "".join(c for c in base_name if c.isalnum() or c in "._-[]").strip()

@router.get("/")
def list_problems():
    """Trả danh sách các file PDF trong thư mục downloads"""
    if not os.path.isdir(DOWNLOADS_PATH):
        raise HTTPException(500, f"Downloads path not found: {DOWNLOADS_PATH}")

    files = [f for f in os.listdir(DOWNLOADS_PATH) if f.lower().endswith(".pdf")]
    return {"files": files}

@router.get("/{filename}")
def download_problem(filename: str):
    """Tải file PDF — cho phép bỏ phần .pdf trong URL"""
    safe_name = safe_filename(filename)

    # Nếu người dùng không truyền đuôi .pdf → tự thêm vào
    if not safe_name.lower().endswith(".pdf"):
        safe_name += ".pdf"

    file_path = os.path.join(DOWNLOADS_PATH, safe_name)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type="application/pdf", filename=safe_name)
