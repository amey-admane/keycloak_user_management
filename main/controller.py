import requests

API_BASE_URL = "http://localhost:8080/"  

TOKEN_URL = "http://localhost:8080/realms/myrealm/protocol/openid-connect/token"

GRANT_TYPE = [
    "authorization_code",
    "implicit",
    "refresh_token",
    "password",
    "client_credentials"
]
CLIENT_ID = "myclient" 
CLIENT_SECRET = "4zB2VNABdRA8p9eCtavrAWVcpDzOB9SX"  


def get_token(grant_type: str, extra_params: dict = None) -> str:
    """
    Retrieve an API token based on the grant type and parameters.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {
        "grant_type": grant_type,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    
    if extra_params:
        payload.update(extra_params)

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve token: {response.text}")

    token_data = response.json()
    return token_data.get("access_token")


def create_user(user_data: dict, token: str) -> dict:
    """
    Call the external API to create a user.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_BASE_URL}/admin/realms/myrealm/users", json=user_data, headers=headers)
    if response.status_code == 201: 
        
        if response.content.strip():  
            return response.json()
        else:
            
            return {"message": "User created successfully, but no content returned."}

    if response.status_code != 201:
        raise Exception(f"Failed to create user: {response.text}")

    return response.json()


def create_client(client_data: dict, token: str) -> dict:
    """
    Call the external API to create a client.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_BASE_URL}/admin/realms/myrealm/clients", json=client_data, headers=headers)
    if response.status_code == 201:  
        
        if response.content.strip():  
            return response.json()
        else:
           
            return {"message": "Client created successfully, but no content returned."}

    if response.status_code != 201:
        raise Exception(f"Failed to create client: {response.text}")

    return response.json()


def view_users(token: str) -> list:
    """
    Call the external API to fetch users.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{API_BASE_URL}/admin/realms/myrealm/users", headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch users: {response.text}")

    return response.json()


def view_clients(token: str) -> list:
    """
    Call the external API to fetch clients.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{API_BASE_URL}/admin/realms/myrealm/clients", headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch clients: {response.text}")

    return response.json()



def view_groups(token: str) -> list:
    """
    Call the external API to fetch clients.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{API_BASE_URL}/admin/realms/myrealm/groups", headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch groups: {response.text}")

    return response.json()


def create_groups(group_data: dict, token: str) -> dict:
    """
    Call the external API to create a client.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{API_BASE_URL}/admin/realms/myrealm/groups", json=group_data, headers=headers)
    if response.status_code == 201:  
        
        if response.content.strip():  
            return response.json()
        else:
           
            return {"message": "Group created successfully, but no content returned."}

    if response.status_code != 201:
        raise Exception(f"Failed to create group: {response.text}")

    return response.json()

