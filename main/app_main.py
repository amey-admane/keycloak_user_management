from fastapi import FastAPI, HTTPException
from .controller import get_token, create_user, create_client, view_users, view_clients,view_groups,create_groups
import json


app = FastAPI()


group_data = {
	"name": "testgroup1",
	"path": "/testgroup1",
	"subGroups": []
}
client_data =  {
    "clientId": "myclient1",
    "name": "Samuel1",
    "description": "Test client1",
    "rootUrl": "http://localhost:8000/",
    "adminUrl": "",
    "baseUrl": "",
    "surrogateAuthRequired": False,
    "enabled": True,
    "redirectUris": [],
    "webOrigins": [
      "/*"
    ],
    "notBefore": 0,
    "bearerOnly": False,
    "consentRequired": False,
    "standardFlowEnabled": True,
    "implicitFlowEnabled": False,
    "directAccessGrantsEnabled": True,
    "serviceAccountsEnabled": True,
    "authorizationServicesEnabled": True,
    "publicClient": False,
    "frontchannelLogout": True,
    "protocol": "openid-connect",
    "fullScopeAllowed": True,
    "nodeReRegistrationTimeout": -1,
    "defaultClientScopes": [
      "web-origins",
      "acr",
      "profile",
      "roles",
      "basic",
      "email"
    ],
    "optionalClientScopes": [
      "address",
      "phone",
      "offline_access",
      "microprofile-jwt"
    ]
   
  }
@app.get("/users")
# async def create_user_endpoint(user_data: dict):
async def create_user_endpoint():
    """Create a new user."""
    try:
        user_data = {
            "username": "test_user_3",
            "firstName": "test_user3",
            "lastName": "user_3",
            "email": "testuser_3@gmail.com",
            "emailVerified": True,
            "enabled": True,
            "groups": [],
            "requiredActions": []
        }
        token = get_token(grant_type="client_credentials")  
        return create_user(user_data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/clients")
# async def create_client_endpoint(client_data: dict):
async def create_client_endpoint():
    """Create a new client."""
    try:
        token = get_token(grant_type="client_credentials")  
        # token = get_token(grant_type="password", extra_params={"username": "user", "password": "pass"})  # Example
        return create_client(client_data, token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_users")
async def view_users_endpoint():
    """Retrieve a list of users."""
    try:
        token = get_token(grant_type="client_credentials")
        return view_users(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get_clients")
async def view_clients_endpoint():
    """Retrieve a list of clients."""
    try:
        token = get_token(grant_type="client_credentials")
        return view_clients(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.get("/get_groups")
async def view_groups_endpoint():
    """Retrieve a list of groups."""
    try:
        token = get_token(grant_type="client_credentials")
        return view_groups(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get("/groups")
async def create_groups_endpoint():
    """Create a new of group."""
    try:
        token = get_token(grant_type="client_credentials")
        return create_groups(group_data,token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
