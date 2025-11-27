import os
from datetime import datetime, timedelta

from typing import Any, Dict, List, Union
from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer


from backend.CAE import *

# Initialisation de l'application FastAPI

TEMPLATES_DIR = "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)



import os
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse


# Get the BASE directory dynamically
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get backend folder path
#TEMPLATES_DIR = os.path.join(BASE_DIR, "../templates")  # Go up one level to templates
app = FastAPI()

# Get the parent directory (root of the project)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get backend folder path

# Mount "static" folder correctly
app.mount("/static", StaticFiles(directory="static"), name="templates")

# Load templates from "templates"

from fastapi.responses import RedirectResponse, HTMLResponse


@app.get("/signup")
def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
@app.get("/reset")
def login(request: Request):
    return templates.TemplateResponse("oublie.html", {"request": request})







@app.get("/simulation")
async def simulation(request: Request):
     return templates.TemplateResponse("simulation.html", {
                "request": request,
                "user_name": "haitham.abdedaim@gmail.com",
                "user_licence": 'Admin',
                "renewal_date": '2029'
            })
   
    #
    
    
@app.post("/validate-location")
async def validate_location(request: Request):
    data = await request.json()
    province_google = data.get("province")  # Province venant du frontend (Google Maps)
    
    # Mapper vers la province backend
    print(data)
    province=data.get("province")
    altitude=data.get("altitude")
    zone=get_zone(province, altitude)
    G=obtenir_coefficient_G(province, zone)
    cumac=calculer_ae_total(data,G, 0.97)

    return {"zone": zone,"Ceoficient":G,"cumac":cumac}



@app.post("/to_pay")
async def projets(request: Dict[Any, Any]):
    try :
        print(request)
        id_=request['event']['pulseId']
        id_insta=request['event']['boardId']

        #url_=create_payment(entreprise,nom,prenom,id_,id_insta,Email,Adresse)
        
        return request
    except :
        print("newwww_connexion")
        return request
