import csv, hashlib, os, traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/login", tags=["login"])

# --- cấu hình ---
CSV_PATH = r".\users.csv"  # đường dẫn tương đối từ backend/main.py

class LoginRequest(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    """Hash SHA-256 để so sánh"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/")
def login(req: LoginRequest):
    """Đăng nhập dựa trên file CSV"""

    print("=== [LOGIN API CALLED] ===")
    print(f"Username: {req.username}")
    print(f"CSV_PATH: {os.path.abspath(CSV_PATH)}")

    # --- Kiểm tra file tồn tại ---
    if not os.path.exists(CSV_PATH):
        msg = f"User file not found: {os.path.abspath(CSV_PATH)}"
        print("[ERROR]", msg)
        raise HTTPException(status_code=500, detail=msg)

    try:
        with open(CSV_PATH, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            print("[DEBUG] CSV headers:", reader.fieldnames)

            # --- Kiểm tra header hợp lệ ---
            if "username" not in reader.fieldnames or "password" not in reader.fieldnames:
                msg = f"Invalid CSV format. Expected columns: username,password. Found: {reader.fieldnames}"
                print("[ERROR]", msg)
                raise HTTPException(status_code=500, detail=msg)

            # --- Duyệt từng dòng để xác thực ---
            for row in reader:
                print("[DEBUG] Checking row:", row)
                if row["username"] == req.username and row["password"] == hash_password(req.password):
                    print(f"[SUCCESS] User '{req.username}' authenticated.")
                    return {"status": "ok", "user": req.username}

        print(f"[WARN] Invalid credentials for '{req.username}'")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    except UnicodeDecodeError:
        msg = f"File encoding error: ensure {CSV_PATH} is saved as UTF-8"
        print("[ERROR]", msg)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=msg)

    except Exception as e:
        print("[EXCEPTION] Unexpected error while processing login:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
