from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Ruta para servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta para servir el archivo HTML desde la carpeta estática
@app.get("/", response_class=FileResponse)
async def get_form():
    return FileResponse("static/index.html")  # Aquí especificamos la ubicación de tu HTML