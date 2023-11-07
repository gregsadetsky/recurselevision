import json
import os
import secrets
from pathlib import Path
from typing import Annotated
from datetime import datetime, timedelta

import recurring_ical_events

from dotenv import load_dotenv
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Request,
    Response,
    status,
    BackgroundTasks,
)
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_400_BAD_REQUEST

from .calendar_api import get_events
from .recurse_api import get_hub_visits_for_today, get_profile

load_dotenv()

META_REFRESH_SECONDS = 60
TIME_FMT = "%Y%m%d"
YEAR = 365
RC_ACCESS_TOKEN = os.environ["RC_ACCESS_TOKEN"]
RC_CALENDAR_URL = os.environ["RC_CALENDAR_URL"]
BASIC_HTTP_AUTH_USER, BASIC_HTTP_AUTH_PASSWORD = os.environ["BASIC_HTTP_AUTH"].split(
    ":"
)
assert len(BASIC_HTTP_AUTH_USER) and len(BASIC_HTTP_AUTH_PASSWORD)
DEBUG = os.environ.get("DEBUG") == "True"

if not DEBUG:
    # do a test access using the rc api token, and fail immediately if it doesn't work
    assert get_profile(RC_ACCESS_TOKEN)["id"]
    # test the calendar URL directly and cache the result
    assert get_events(RC_CALENDAR_URL)

app = FastAPI()
templates = Jinja2Templates(directory="rctv/templates")
all_apps = json.loads(Path("rctv/apps.json").read_text())
security = HTTPBasic()

# This is 'bad' only doing this so we can load app-sdk.js from localhost
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Server static files
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/api/events")
async def cal(
    _request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    start: str | None = None,
    end: str | None = None,
):
    """
    Takes an optional query paramters ?start=YYYY-MM-DD and &end=YYYY-MM-DD
    Returns calendar events as JSON between [start, end] date ranges
    """

    # This either returns the cached calendar or makes an API call
    # This isn't ideal because if some RCTV is not regularly hitting this API we
    # are going to get cache-misses and do the full API request which comes out
    # to be 1.2 MB
    #
    # An alternative approach is to use something like fastapi_utils.repeat_every
    # to run this on a periodic basis instead:
    #
    # https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/
    cal = get_events(RC_CALENDAR_URL)

    try:
        start_datetime = (
            datetime.strptime(start, TIME_FMT) if start is not None else datetime.now()
        )
        end_datetime = (
            datetime.strptime(end, TIME_FMT)
            if end is not None
            else start_datetime + timedelta(days=(2 * YEAR))
        )
    except ValueError:
        response.status_code = HTTP_400_BAD_REQUEST
        return {
            "message": "'start' and 'end' params must be formatted in %Y%m%d. Example: 20250101"
        }

    events = recurring_ical_events.of(cal)
    events = events.between(
        start_datetime.strftime(TIME_FMT), end_datetime.strftime(TIME_FMT)
    )
    j = []
    for event in events:
        if "SUMMARY" in event:
            if "STATUS" in event and event["STATUS"] == "CANCELLED":
                continue
            e = {}
            e["summary"] = event["SUMMARY"]
            e["start"] = event["DTSTART"].dt
            e["end"] = event["DTEND"].dt
            duration = event["DTEND"].dt - event["DTSTART"].dt
            e["duration_seconds"] = duration
            e["duration_string"] = str(duration)
            e["description"] = event["DESCRIPTION"]
            e["location"] = event["LOCATION"]
            j.append(e)

    return j
