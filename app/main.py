from fastapi import FastAPI
from .routes import auth, user, invoice
from .database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.routers)
app.include_router(invoice.router)


@app.get("/")
async def root():
    return {"message": "welcome to my invoicing app"}
