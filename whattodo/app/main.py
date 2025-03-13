# app/main.py
import uvicorn  # if __name__ == "__main__" 内から移動
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router  # ルーターを含めるコメント後から移動
from app.core.config import settings
from app.db.base import Base  # 26行目から移動
from app.db.session import engine  # データベース依存関係のコメント後から移動

app = FastAPI(
    title="WhatToDo API", description="API for WhatToDo - Task Management and Social Sharing App", version="0.1.0"
)

# CORS設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to WhatToDo API"}


# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

# ルーターを含める
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
