import os
import stripe
import jwt
from datetime import datetime, timedelta
from jose import JWTError, jwt


from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from backend.database import SessionLocal, User, add_user, check_user_existence, get_db
from backend.utils import hash_password, verify_password, generate_reset_token, send_reset_email
from backend.auth import SECRET_KEY, ALGORITHM, create_access_token
from backend.smtp import *
from backend.CAE import *

# Initialisation de l'application FastAPI

TEMPLATES_DIR = "templates"
templates = Jinja2Templates(directory=TEMPLATES_DIR)



from pydantic import BaseModel
import os
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError


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

@app.get("/")
async def login(request: Request):
    access_token = request.cookies.get("access_token")
    print("Access Token:", access_token)  # ✅ Debugging

    # If no token, show login page
    if not access_token:
        return templates.TemplateResponse("index.html", {"request": request})
        #return HTMLResponse(content=html_content, status_code=200)

    # Remove "Bearer " prefix before decoding
    access_token = access_token.replace("Bearer ", "")

    try:
        # Decode the token
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except :
        return templates.TemplateResponse("index.html", {"request": request})
    try :
        user_email = payload.get("sub")
        
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid token")

        # ✅ If token is valid, redirect to /simulation
        return RedirectResponse(url="/simulation")
        #return HTMLResponse(content=html_content, status_code=200)

    except JWTError:
        # If token is invalid, show login page
        return templates.TemplateResponse("index.html", {"request": request})
        #return HTMLResponse(content=html_content, status_code=200)

@app.get("/signup")
def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
@app.get("/reset")
def login(request: Request):
    return templates.TemplateResponse("oublie.html", {"request": request})

#@app.get("/subscribe")
#async def subscribe(request: Request, db: Session = Depends(get_db)):
#    """
#    ✅ Show subscription page if trial has ended and user is not subscribed
#    """
#    session_id = request.cookies.get("session_id")
#    if not session_id:
#        return RedirectResponse(url="/")
#
#    try:
#        payload = jwt.decode(session_id, SECRET_KEY, algorithms=["HS256"])
#        email = payload.get("email")
#        user = db.query(User).filter(User.email == email).first()
#
#        if not user:
#            raise HTTPException(status_code=404, detail="User not found")
#
#        # ✅ Pass `user` to template
#        return templates.TemplateResponse("subscribe.html", {"request": request, "user": user})
#
#    except JWTError:
#        return RedirectResponse(url="/")


@app.get("/subscribe")
async def subscribe(request: Request, db: Session = Depends(get_db)):
    """
    ✅ Show subscription page if trial has ended and user is not subscribed
    """

    session_id = request.cookies.get("access_token") 
    
    if not session_id:
        return RedirectResponse(url="/")  # Redirect if not logged in
    if session_id.startswith("Bearer "):
        session_id = session_id.replace("Bearer ", "")
    try :    
        payload = jwt.decode(session_id, SECRET_KEY, algorithms=["HS256"])
        user_email = payload.get("sub")  
        user_licence = payload.get("licence")  
        renewal_date = payload.get("renewal_date")  

        user = db.query(User).filter(User.email == user_email).first()

        if not user:
            return RedirectResponse(url="/")

        # Check if the free trial is over
        #if datetime.now() > user.trial_end_date:
        #    return RedirectResponse(url="/subscribe")  # Redirect to subscription page
        

        return templates.TemplateResponse("subscribe.html", {
                "request": request,
                "user_name": user_email,
                "user_licence": user_licence,
                "renewal_date": renewal_date,
                "user":user
            })
    except JWTError:
        return templates.TemplateResponse("index.html", {"request": request})

  








oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    print("Received Token:", token)  # Debugging
    credentials_exception = HTTPException(status_code=401, detail="Token invalide")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        return user_email
    except JWTError:
        raise credentials_exception





@app.post("/signup")
def signup(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"error": "Email déjà utilisé"}
    print(email,",,______________________,",password)
    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "Compte créé avec succès"}






class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login")
def login(request: Request,data: LoginRequest, db: Session = Depends(get_db)):
    #print('ssssssssssssssssssssss')
    print(data)
    user = db.query(User).filter(User.email == data.email).first()
    #print(user.email)
    #print(user.is_subscribed)
    #print(user.name)
    is_subscribed=user.is_subscribed
    print(user.password)
    print(data.password)
    trial_end_date=user.trial_end_date
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")


    # Generate JWT Token
    access_token = create_access_token(data={"sub": user.email,"licence": is_subscribed,"renewal_date": trial_end_date.isoformat()})
    print(access_token)

    # Create Response and Set Cookie
    response = JSONResponse({"message": "Connexion réussie!", "access_token": access_token})
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}",  
        httponly=True,  
        samesite="Strict",
        max_age=86400  
    )

    return response


#@app.get("/simulation")
#async def simulation(request: Request):
#    access_token = request.cookies.get("access_token")  # ✅ Retrieve access_token from cookies
#    print("Access Token:", access_token)  # Debugging step
#
#    if not access_token:
#        login_dir = os.path.join(templates, "index.html")
#        with open(login_dir, encoding="utf-8") as f:
#            html_content = f.read()
#
#        return HTMLResponse(content=html_content, status_code=200)
#
#
#    # Remove "Bearer " prefix if present
#    if access_token.startswith("Bearer "):
#        access_token = access_token.replace("Bearer ", "")
#
#    try:
#        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
#        user_email = payload.get("sub")
#        print(payload)
#        
#        if not user_email:
#            raise HTTPException(status_code=401, detail="Invalid token")
#
#        # ✅ Use correct path for simulation.html
#        simulation_path = os.path.join(templates, "simulation.html")
#
#        with open(simulation_path, encoding="utf-8") as f:
#            html_content = f.read()
#
#        return HTMLResponse(content=html_content, status_code=200)
#
#    except JWTError:
#        return templates.TemplateResponse("index.html", {"request": request})



#@app.get("/simulation")
#async def simulation(request: Request):
#    access_token = request.cookies.get("access_token")  # ✅ Récupérer le token depuis les cookies
#    print("Access Token:", access_token)  # Debugging
#
#    if not access_token:
#        return templates.TemplateResponse("index.html", {"request": request})
#
#    # ✅ Supprimer "Bearer " si présent
#    if access_token.startswith("Bearer "):
#        access_token = access_token.replace("Bearer ", "")
#
#    try:
#        # ✅ Décoder le JWT
#        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
#        user_email = payload.get("sub")  
#        user_licence = payload.get("licence")  
#        renewal_date = payload.get("renewal_date")  
#        
#
#        if not user_email:
#            raise HTTPException(status_code=401, detail="Invalid token")
#
#        # ✅ Renvoyer les infos à `simulation.html`
#        return templates.TemplateResponse("simulation.html", {
#            "request": request,
#            "user_name": user_email,
#            "user_licence": user_licence,
#            "renewal_date": renewal_date
#        })
#
#    except JWTError:
#        return templates.TemplateResponse("index.html", {"request": request})
@app.get("/simulation")
async def simulation(request: Request, db: Session = Depends(get_db)):
     return templates.TemplateResponse("simulation.html", {
                "request": request,
                "user_name": "haitham.abdedaim@gmail.com",
                "user_licence": 'Admin',
                "renewal_date": '2029'
            })
    #session_id = request.cookies.get("access_token") 
    
    #if not session_id:
    #    return RedirectResponse(url="/")  # Redirect if not logged in
    #if session_id.startswith("Bearer "):
    #    session_id = session_id.replace("Bearer ", "")
    #try :    
    #    payload = jwt.decode(session_id, SECRET_KEY, algorithms=["HS256"])
    #    user_email = payload.get("sub")  
    #    user_licence = payload.get("licence")  
    #    renewal_date = payload.get("renewal_date")  
#
    #    user = db.query(User).filter(User.email == user_email).first()
#
    #    if not user:
    #        return RedirectResponse(url="/")
#
    #    # Check if the free trial is over
    #    if datetime.now() > user.trial_end_date:
    #        return RedirectResponse(url="/subscribe")  # Redirect to subscription page
    #    
#
    #    return templates.TemplateResponse("simulation.html", {
    #            "request": request,
    #            "user_name": user_email,
    #            "user_licence": user_licence,
    #            "renewal_date": renewal_date
    #        })
    #except JWTError:
    #    return templates.TemplateResponse("index.html", {"request": request})
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


@app.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "Déconnecté"})
    response.delete_cookie("access_token")  # Supprimer le cookie
    return response
from fastapi import FastAPI, HTTPException, Request, Response, Depends, Form


class UserRegistration(BaseModel):
    name: str
    email: str
    password: str

@app.post("/inscription")
async def register_user(request: Request, response: Response, user_data: UserRegistration):
    email = user_data.email.lower()
    name = user_data.name
    print(email,name,user_data.password)
    password_not_hashed=user_data.password
    password = hash_password(password_not_hashed)  # ✅ Hash password
    print(password)

    if not check_user_existence(email):
        trial_end_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        licence = "Période d'essai"

        payload = {
            "name": name,
            "email": email,
            "trial_end_date": trial_end_date,
            "licence": licence,
            "is_subscribed": False
        }

        try:
            add_user(name, email, password, trial_end_date, licence)  # ✅ Save user

            access_token = create_access_token(data={"sub": email,"licence": False,"renewal_date": trial_end_date})
            print(access_token)

            # Create Response and Set Cookie
            response = JSONResponse({"message": "Connexion réussie!", "access_token": access_token})
            response.set_cookie(
                key="access_token", 
                value=f"Bearer {access_token}",  
                httponly=True,  
                samesite="Strict",
                max_age=86400  
            )

            return response
        except Exception as e:
            print("Error:", e)
            raise HTTPException(status_code=500, detail="Erreur lors de l'inscription")

    else:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    

class PasswordRecoveryRequest(BaseModel):
    email: str

@app.post("/password-recovery")
async def password_recovery(url:Request,request: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    email = request.email.lower()
    
    # Check if user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email non trouvé.")
    
    # Generate reset token
    reset_token = generate_reset_token(email)
    name=user.name
    print(name)
    licence=User.licence
    print(url)
    # Send email with reset link
    reset_link = f"{str(url.base_url).rstrip('/')}/reset-password?token={reset_token}"
    #send_msg(name,email,"Devis",email,reset_link,licence)
    send_password_reset_email(name, email, reset_link)
    #send_reset_email(email, reset_link)
    print(reset_link)

    return {"message": "Un lien de réinitialisation a été envoyé à votre email."}



class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@app.post("/reset-password")
async def reset_password(request: Request, data: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(data.token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except jwt.ExpiredSignatureError:
        return {"error": "Le lien de réinitialisation a expiré."}
    except jwt.InvalidTokenError:
        return {"error": "Token invalide."}

    # Get user from DB
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"error": "Utilisateur non trouvé."}

    # Hash and update the password
    user.password = hash_password(data.new_password)
    db.commit()

    return {"message": "Mot de passe réinitialisé avec succès."}


@app.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    """ Serve the password reset page """
    reset_password_path = os.path.join(TEMPLATES_DIR, "password-recovery.html")
    
    with open(reset_password_path, encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)


#----------------------------------- stripe -------------------------------------------------------



stripe.api_key = "sk_test_51Qz9HnBebPTU6EeSFUtxCE2vAnVjVUCpLXP7rH8kT1M0H1QDXUOr64khmq6ag0IHl94O1ICOxuAV3NYhDuWnia5j00ajTBTsod"



STRIPE_PRICES = {
    "monthly": "price_1QznNyBebPTU6EeSH732tg6X",  # Replace with your Stripe price ID
}

@app.post("/create-checkout-session")
async def create_checkout_session(request: Request,email: str, db: Session = Depends(get_db)):
    """
    ✅ Handles Stripe Subscription Checkout:
    - If user has an active subscription, redirect to `/simulation`.
    - If user has a canceled/unpaid subscription, create a new one.
    - If user is new, create Stripe Customer and subscribe them.
    """
    try:
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")

        # 🟢 Find User in Database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 🟢 Check if user already has a Stripe customer ID
        if user.customer_stripe_id:
            print(f"✅ User {email} already has a Stripe Customer ID: {user.customer_stripe_id}")

            # Retrieve all subscriptions for the customer
            subscriptions = stripe.Subscription.list(customer=user.customer_stripe_id)

            if subscriptions.data:
                # Check the status of the latest subscription
                latest_subscription = subscriptions.data[0]  # Latest subscription (sorted by creation date)
                status = latest_subscription.status

                if status == "active":
                    print(f"✅ Active subscription found for {email}, redirecting to /simulation.")
                    return RedirectResponse(url="/simulation", status_code=303)  # ✅ Use 303 See Other

                elif status in ["canceled", "unpaid", "past_due", "incomplete", "incomplete_expired"]:
                    print(f"🟠 Subscription {status} for {email}, creating a new one...")
                    # If subscription is unpaid/canceled, create a new subscription

        # 🟢 If no active subscription, create a new one
        print(f"🟡 No active subscription found. Creating a new one for {email}...")

        # If customer doesn't exist in Stripe, create a new one
        if not user.customer_stripe_id:
            customer = stripe.Customer.create(email=email)
            user.customer_stripe_id = customer.id
            db.commit()
        else:
            customer = stripe.Customer.retrieve(user.customer_stripe_id)

        # ✅ Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer=customer.id,
            line_items=[{
                "price": STRIPE_PRICES["monthly"],  # Default Monthly Plan
                "quantity": 1,
            }],
            mode="subscription",
            success_url=f"{str(request.base_url).rstrip('/')}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{str(request.base_url).rstrip('/')}/cancel",
        )

        return {"url": session.url}

    except Exception as e:
        print(f"❌ Error creating checkout session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")




@app.get("/success")
async def stripe_success(request: Request, session_id: str, response: Response, db: Session = Depends(get_db)):
    """
    ✅ Called when user completes Stripe payment successfully.
    - Extracts Stripe Customer ID & Subscription details
    - Updates `user.is_subscribed = True`, `user.customer_stripe_id`, `user.trial_end_date`
    - ✅ Uses Stripe `current_period_end` for `trial_end_date`
    - ✅ Sets authentication cookie before redirecting to `/simulation`
    """
    try:
        # 🟢 Retrieve Stripe Session Details
        session = stripe.checkout.Session.retrieve(session_id)

        if not session or not session.customer:
            raise HTTPException(status_code=400, detail="Invalid Stripe session")

        customer_id = session.customer  # Stripe Customer ID
        email = session.customer_details.email  # Get Email from Stripe

        # 🟢 Find User in Database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 🟢 Retrieve Subscription Details from Stripe
        subscription = stripe.Subscription.retrieve(session.subscription)
        end_date_unix = subscription.current_period_end  # Unix timestamp
        end_date = datetime.utcfromtimestamp(end_date_unix)  # Convert to Datetime

        # 🟢 Update User Subscription in Database
        user.is_subscribed = True
        user.customer_stripe_id = customer_id  # Save Stripe Customer ID
        user.licence = "Abonnement Mensuel"  # Update License Type
        user.trial_end_date = end_date  # ✅ Use Stripe subscription end date

        db.commit()

        print(f"✅ Subscription Activated for: {user.email} (Renews on {end_date})")

        # 🟢 Generate Access Token with Correct Data
        access_token = create_access_token(data={
            "sub": user.email,
            "licence": user.is_subscribed,
            "renewal_date": end_date.isoformat()  # ✅ Use Stripe renewal date
        })

        # ✅ Set authentication cookie
        response = RedirectResponse(url="/simulation")
        response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)

        return response

    except Exception as e:
        print(f"❌ Error processing Stripe success: {e}")
        raise HTTPException(status_code=500, detail="Payment verification failed")
