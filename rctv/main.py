import json
import os
import secrets
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates

from .recurse_api import get_hub_visits_for_today, get_profile

load_dotenv()

META_REFRESH_SECONDS = 60
RC_ACCESS_TOKEN = os.environ["RC_ACCESS_TOKEN"]
BASIC_HTTP_AUTH_USER, BASIC_HTTP_AUTH_PASSWORD = os.environ["BASIC_HTTP_AUTH"].split(
    ":"
)
assert len(BASIC_HTTP_AUTH_USER) and len(BASIC_HTTP_AUTH_PASSWORD)
DEBUG = os.environ.get("DEBUG") == "True"

if not DEBUG:
    # do a test access using the rc api token, and fail immediately if it doesn't work
    assert get_profile(RC_ACCESS_TOKEN)["id"]

app = FastAPI()
templates = Jinja2Templates(directory="rctv/templates")
all_apps = json.loads(Path("rctv/apps.json").read_text())
security = HTTPBasic()


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/app/{app_index}")
async def rctv(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    request: Request,
    app_index: int,
):
    # basic auth
    # https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), BASIC_HTTP_AUTH_USER.encode("utf8")
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), BASIC_HTTP_AUTH_PASSWORD.encode("utf8")
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    if app_index >= len(all_apps):
        return "App index not found"

    app = all_apps[app_index]
    next_app_index = (app_index + 1) % len(all_apps)

    rc_payload = {"hub_visits": get_hub_visits_for_today(RC_ACCESS_TOKEN)}

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "app": app,
            "next_app_index": next_app_index,
            "meta_refresh_seconds": META_REFRESH_SECONDS,
            "rc_payload": rc_payload,
        },
    )
