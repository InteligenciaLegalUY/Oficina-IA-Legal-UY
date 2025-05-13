# main.py
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from conexion import get_openai_client, get_google_services
from dotenv import load_dotenv

load_dotenv()  # carga variables de .env

ACCESS_KEY = os.getenv("ACCESS_KEY", "272903MVD$")
app = FastAPI()

# 1) Montar la carpeta static para servir tu front-end
app.mount("/", StaticFiles(directory="static", html=True), name="static")

def is_authenticated(request: Request):
    return request.cookies.get("auth_token") == ACCESS_KEY

@app.post("/login")
async def login(request: Request, key: str = Form(...)):
    if key == ACCESS_KEY:
        resp = RedirectResponse("/", status_code=302)
        resp.set_cookie("auth_token", key, httponly=True, secure=True)
        return resp
    return HTMLResponse("<h3>Clave incorrecta. <a href='/'>Reintentar</a></h3>", status_code=401)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    # Permitir archivos estáticos y ruta /login sin autenticar
    if request.url.path.startswith("/assets") or request.url.path == "/login":
        return await call_next(request)
    if not is_authenticated(request):
        # Si no está autenticado, muestra el formulario de login
        return HTMLResponse("""
        <html><body style="font-family:sans-serif;max-width:400px;margin:50px auto;">
          <h2>Ingrese clave de acceso</h2>
          <form method="post" action="/login">
            <input type="password" name="key" placeholder="Clave" required
                   style="width:100%;padding:8px;margin-bottom:10px;"/>
            <button type="submit" style="padding:8px 16px;">Entrar</button>
          </form>
        </body></html>
        """, status_code=200)
    return await call_next(request)
