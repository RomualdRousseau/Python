import jwt
import base64
import urllib
import secrets
import hashlib
import requests

from flask import request, redirect, session

TENANT_ID = "cc0a4ff6-9454-4e4b-881b-85f448dee2e3"
CLIENT_ID = "a9ed6536-274c-46b6-a272-9208bef9a266"
#CLIENT_SECRET = "" # no secret needed for SPA
REDIRECT_URL = "http://localhost:4200/"
SCOPE = "https://daasdataportaldev-serviergroup.msappproxy.net/Main openid profile offline_access"

def enable_oauth(func):
    def wrapper():
        access_token = session.get("access_token")
        if access_token is None:
            return do_auth()
        userinfo = jwt.decode(access_token, options={"verify_signature": False})
        return func(userinfo)
    return wrapper


def do_auth():
    code = request.args.get("code")
    if code is None:
        global STATE
        global CODE_VERIFIER
        STATE = secrets.token_hex(5)
        CODE_VERIFIER = secrets.token_hex(50)

        # Auto discovery of endpoints

        resp = requests.get(f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration")
        config = resp.json()

        # First step: authorize and redirect to login page

        code_challenge = base64.urlsafe_b64encode(hashlib.sha256(CODE_VERIFIER.encode('ascii')).digest()).rstrip(b'=')
        params = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URL, 
            "state": STATE, 
            "scope": SCOPE,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256"
        }
        auth_url = config["authorization_endpoint"] + "?" + urllib.parse.urlencode(params)
        return redirect(auth_url, code=302)

    else:
        # Sanity check of the state session

        state = request.args.get("state")
        if STATE != state:
            raise Exception("Invalid OAUTH state")

        # Auto discovery of endpoints

        resp = requests.get(f"https://login.microsoftonline.com/{TENANT_ID}/v2.0/.well-known/openid-configuration")
        config = resp.json()

        # Second step: get access_token

        params = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URL,
            "client_id": CLIENT_ID,
            #"client_secret": CLIENT_SECRET,
            "code_verifier": CODE_VERIFIER
        }
        cross_origin = {"Origin": REDIRECT_URL}
        resp = requests.post(config["token_endpoint"], data=params, headers=cross_origin)
        token = resp.json()
        session["access_token"] = token["access_token"] 
        return redirect(REDIRECT_URL, code=302)
