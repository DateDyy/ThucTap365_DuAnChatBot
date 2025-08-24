from fastapi import FastAPI
from app.routes import query, chat, update

app = FastAPI()

app.include_router(query.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(update.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)