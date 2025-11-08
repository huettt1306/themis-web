# backend/main.py
import os
import shutil
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# cấu hình: chỉnh theo hệ thống của bạn
OSD_PATH = r"..\OSD"  # hoặc "/opt/themis/osd"
LOGS_SUBDIR = r"..\OSD\Logs"

app = FastAPI(title="Themis Proxy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production: hạn chế domain
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_filename(base_name: str) -> str:
    # đơn giản: loại bỏ ký tự đường dẫn
    return "".join(c for c in base_name if c.isalnum() or c in "._-[]").strip()

@app.post("/submit")
async def submit(student: str = Form(...), problem: str = Form(...), file: UploadFile = None):
    if file is None:
        raise HTTPException(400, "No file uploaded")
    ext = os.path.splitext(file.filename)[1] or ""
    # tạo tên file theo quy ước *[Mã][Bài].ext
    # ở đây dùng timestamp làm phần * để tránh trùng
    import time
    prefix = str(int(time.time() * 1000))
    raw_name = f"{prefix}[{safe_filename(student)}][{safe_filename(problem)}]{ext}"
    tmp_path = os.path.join(os.getcwd(), "tmp_upload")
    os.makedirs(tmp_path, exist_ok=True)
    tmp_file = os.path.join(tmp_path, raw_name)
    # ghi tạm
    with open(tmp_file, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # đảm bảo OSD tồn tại
    if not os.path.isdir(OSD_PATH):
        raise HTTPException(500, f"OSD path not found: {OSD_PATH}")
    dest_path = os.path.join(OSD_PATH, raw_name)
    # atomic move
    os.replace(tmp_file, dest_path)
    return JSONResponse({"status": "ok", "filename": raw_name})

@app.get("/result/{filename}")
def result(filename: str):
    # đọc file log
    safe = safe_filename(filename)
    log_path = os.path.join(OSD_PATH, LOGS_SUBDIR, safe + ".log")
    if os.path.exists(log_path):
        with open(log_path, encoding="utf8", errors="replace") as f:
            return {"ready": True, "content": f.read()}
    return {"ready": False}
