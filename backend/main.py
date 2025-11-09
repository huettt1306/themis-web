# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, submit, problems

app = FastAPI(title="Themis Proxy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production: hạn chế domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn router
app.include_router(login.router)
app.include_router(submit.router)
app.include_router(problems.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
