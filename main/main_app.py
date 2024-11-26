


from fastapi import  FastAPI, Depends, HTTPException, Request, status
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient

from starlette.responses import RedirectResponse
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from httpx import Client
import logging
from fastapi import Security

# Load environment variables
config = Config(".env")
KEYCLOAK_URL = config("KEYCLOAK_URL")
KEYCLOAK_REALM = config("KEYCLOAK_REALM")
CLIENT_ID = config("KEYCLOAK_CLIENT_ID")
CLIENT_SECRET = config("CLIENT_SECRET")
REDIRECT_URI = config("REDIRECT_URI")
SESSION_SECRET_KEY = config("SESSION_SECRET_KEY", default="supersecretkey")

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)


authorize_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"
token_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token"
userinfo_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo"

REDIRECT_URI = "http://localhost:8000/callback"

authorize_url = f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth"



@app.get("/login")
def login():
    """Redirect to Keycloak login page."""
    auth_endpoint = (
        f"{authorize_url}?client_id={CLIENT_ID}"
        f"&response_type=code&scope=openid"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(auth_endpoint)


@app.get("/callback")
async def auth_callback(request: Request, code: str):
    print("In auth callback ")
    """Handle the Keycloak callback, get the token, and retrieve user info."""
    async with AsyncClient() as client:
        # Exchange the authorization code for tokens
        token_response = await client.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            }
        )
        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Token exchange failed")

        tokens = token_response.json()
        request.session['access_token'] = tokens.get("access_token")
        request.session['refresh_token'] = tokens.get("refresh_token")
        
        # Retrieve user information using the access token
        userinfo_response = await client.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {request.session['access_token']}"}
        )
        if userinfo_response.status_code != 200:
            raise HTTPException(status_code=400, detail="User info retrieval failed")

        user_info = userinfo_response.json()
        request.session['user_info'] = user_info
        return {"user_info": user_info, "access_token": request.session['access_token']}

def get_current_user(request: Request):
    """Retrieve the current user information from the session or redirect to login."""
    token = request.session.get('access_token')
    if not token:
        # No access token, construct login URL and redirect
        login_url = (
            f"{authorize_url}?client_id={CLIENT_ID}"
            f"&response_type=code&scope=openid"
            f"&redirect_uri={REDIRECT_URI}"
        )
        return RedirectResponse(login_url)

    user_info = request.session.get('user_info')
    if not user_info:
        # If user_info is missing, also redirect to login URL
        login_url = (
            f"{authorize_url}?client_id={CLIENT_ID}"
            f"&response_type=code&scope=openid"
            f"&redirect_uri={REDIRECT_URI}"
        )
        return RedirectResponse(login_url)

    # If authenticated, return user information
    return user_info


@app.get("/me")
def get_loggedin_user(request: Request):
    
    user = request.session.get("user")
    print(user)
    if user is not None:
        return user
    return None
    
    


@app.get("/protected")
def protected_route(request: Request,user_info =Depends(get_loggedin_user)):
    """A protected route that requires a valid Keycloak session."""
    # if isinstance(user_info, RedirectResponse):
    #     # If get_current_user returned a RedirectResponse, execute the redirect
    #     return user_info
    if user_info is None:
    # If user_info is valid, return the protected content
    
        return {"message": "You dont have an access to this protected route!"}
    else:
        return {"message": "You have access to this protected route!", "user_info": user_info}
