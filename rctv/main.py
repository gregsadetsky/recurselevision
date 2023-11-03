import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from .recurse_api import get_hub_visits_for_today, get_profile

load_dotenv()

META_REFRESH_SECONDS = 60
RC_ACCESS_TOKEN = os.environ["RC_ACCESS_TOKEN"]
DEBUG = os.environ.get("DEBUG") == "True"

if not DEBUG:
    # do a test access using the token, and fail immediately if it doesn't work
    assert get_profile(RC_ACCESS_TOKEN)["id"]

app = FastAPI()
templates = Jinja2Templates(directory="rctv/templates")
all_apps = json.loads(Path("rctv/apps.json").read_text())


@app.get("/app/{app_index}")
async def rctv(
    request: Request,
    app_index: int,
):
    # FIXME roll out basic auth
    return

    if app_index >= len(all_apps):
        return "App index not found"

    app = all_apps[app_index]
    next_app_index = (app_index + 1) % len(all_apps)
    is_single_app = len(all_apps) == 1

    rc_payload = {"hub_visits": get_hub_visits_for_today(RC_ACCESS_TOKEN)}

    return templates.TemplateResponse(
        "app.html",
        {
            "request": request,
            "app": app,
            "next_app_index": next_app_index,
            "meta_refresh_seconds": META_REFRESH_SECONDS,
            "is_single_app": is_single_app,
            "rc_payload": rc_payload,
        },
    )
