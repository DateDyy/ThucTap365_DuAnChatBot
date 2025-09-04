from fastapi import FastAPI
from api.app.routes import query, chat, update

app = FastAPI()

app.include_router(query.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(update.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))  # Railway sẽ tự set PORT
    uvicorn.run("api.app.main:app", host="0.0.0.0", port=port)
