# backend/routers/submit.py
import os, shutil, time
from fastapi import APIRouter, UploadFile, Form, HTTPException
from starlette.responses import JSONResponse

router = APIRouter(prefix="/submit", tags=["submit"])

# --- cấu hình ---
OSD_PATH = r"..\OSD"          # thư mục chính để lưu file nộp
LOGS_SUBDIR = "Logs"          # thư mục con chứa log trong OSD

# --- hàm tiện ích ---
def safe_filename(base_name: str) -> str:
    """Loại bỏ ký tự nguy hiểm để tránh traversal"""
    return "".join(c for c in base_name if c.isalnum() or c in "._-[]").strip()

# --- API 1: nộp bài ---
@router.post("/")
async def submit(student: str = Form(...), problem: str = Form(...), file: UploadFile = None):
    if file is None:
        raise HTTPException(400, "No file uploaded")

    # tạo tên file duy nhất
    ext = os.path.splitext(file.filename)[1] or ""
    prefix = str(int(time.time() * 1000))
    raw_name = f"{prefix}[{safe_filename(student)}][{safe_filename(problem)}]{ext}"

    # ghi tạm
    tmp_path = os.path.join(os.getcwd(), "tmp_upload")
    os.makedirs(tmp_path, exist_ok=True)
    tmp_file = os.path.join(tmp_path, raw_name)
    with open(tmp_file, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # đảm bảo thư mục đích tồn tại
    if not os.path.isdir(OSD_PATH):
        raise HTTPException(500, f"OSD path not found: {OSD_PATH}")

    # di chuyển sang OSD (atomic)
    dest_path = os.path.join(OSD_PATH, raw_name)
    os.replace(tmp_file, dest_path)

    return JSONResponse({"status": "ok", "filename": raw_name})

# --- API 2: lấy kết quả ---
@router.get("/result/{filename}")
def result(filename: str):
    safe_name = safe_filename(filename)
    log_path = os.path.join(OSD_PATH, LOGS_SUBDIR, safe_name + ".log")

    if os.path.exists(log_path):
        with open(log_path, encoding="utf8", errors="replace") as f:
            return {"ready": True, "content": f.read()}

    return {"ready": False}
