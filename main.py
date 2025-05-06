from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from uuid import uuid4
from typing import List
import uvicorn

app = FastAPI(title="CNAM Ticketing System")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Modèle de données
class Ticket(BaseModel):
    id: str
    service: str
    is_processed: bool = False

# Base de données en mémoire
tickets_db = []

# Endpoints API
@app.post("/api/tickets", response_model=Ticket)
async def create_ticket(service: str):
    try:
        ticket = Ticket(
            id=str(uuid4()),
            service=service,
            is_processed=False
        )
        tickets_db.append(ticket.dict())
        return ticket
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/tickets", response_model=List[Ticket])
async def get_tickets():
    return tickets_db

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)