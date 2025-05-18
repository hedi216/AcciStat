from fastapi import FastAPI
from update import update_all
import uvicorn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de mise à jour des accidents 🚦"}

@app.get("/update")
def update_route():
    try:
        update_all()
        return {"status": "succès", "message": "Mise à jour effectuée avec succès ✅"}
    except Exception as e:
        return {"status": "échec", "message": str(e)}

# Pour exécution directe : uvicorn src.api:app --reload
if __name__ == "__main__":
    uvicorn.run("src.api:app", host="127.0.0.1", port=8000, reload=True)
