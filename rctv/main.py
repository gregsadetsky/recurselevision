import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="rctv/templates")
all_apps = json.loads(Path("rctv/apps.json").read_text())


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/rctv/app/{app_index}")
async def rctv(request: Request, app_index: int):
    if app_index >= len(all_apps):
        return "App index not found"
    app = all_apps[app_index]
    next_app_index = (app_index + 1) % len(all_apps)
    return templates.TemplateResponse(
        "rctv.html", {"request": request, "app": app, "next_app_index": next_app_index}
    )


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
