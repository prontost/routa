"""Routa PWA — the product. Hard input forms, deterministic outputs.

Auth: Avalone SSO via shared `avalone_session` cookie only.
No AI/LLM layer: all analytics and tips are rule-based.
"""

import hashlib
import logging
import logging.handlers
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer

from avalone_core import glossary
from avalone_core.registry import AvaloneRegistry
from avalone_core.ui import Shell, build_id as ui_build_id
import avalone_core.ui
from routa.core import config, constants, db, external_auth, rides, tenant
from routa.core.config import settings
from routa.web.api import router as api_router


def _setup_logging() -> None:
    """Пишем логи приложения в файл с ротацией; stderr оставляем для launchd."""
    log_dir = db.DB_PATH.parent if db.DB_PATH else Path.home() / ".routa"
    log_dir.mkdir(parents=True, exist_ok=True)
    handler = logging.handlers.RotatingFileHandler(
        log_dir / "routa.log",
        maxBytes=constants.get("log_max_bytes"),
        backupCount=constants.get("log_backup_count"),
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    if not any(isinstance(h, logging.handlers.RotatingFileHandler) for h in root.handlers):
        root.addHandler(handler)


_setup_logging()

app = FastAPI(title="Routa")
BASE = Path(__file__).parent
_templates_dir = BASE / "templates"
_static_dir = BASE / "static"
_ui_dir = Path(avalone_core.ui.__file__).parent
_ui_templates_dir = _ui_dir / "templates"
_ui_static_dir = _ui_dir / "static"
templates = Jinja2Templates(directory=[str(_templates_dir), str(_ui_templates_dir)])
templates.env.globals["glossary"] = glossary.GLOSSARY
templates.env.globals["t"] = glossary.t
templates.env.globals["i18n_js"] = glossary.i18n_js
templates.env.globals["registry"] = AvaloneRegistry
app.mount("/static/ui", StaticFiles(directory=str(_ui_static_dir)), name="ui_static")
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")
_sso_signer = URLSafeSerializer(
    settings().avalone_fernet_key or settings().fernet_key,
    salt="avalone-session",
)


def _build_id() -> str:
    """Хеш UI-изменений: при любом изменении шаблонов/статики/веб-API клиенты
    получают новый build и принудительно перезагружаются."""
    h = hashlib.md5(usedforsecurity=False)
    root = BASE.parent  # src/routa
    for sub in ["web", "templates", "static"]:
        p = root / sub
        if not p.exists():
            continue
        for f in sorted(p.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                try:
                    h.update(f"{f.relative_to(root)}:".encode())
                    h.update(f.read_bytes())
                except Exception:
                    pass
    # shared UI
    for sub in ("templates", "static"):
        p = _ui_dir / sub
        for f in sorted(p.rglob("*")):
            if f.is_file() and not f.name.startswith("."):
                try:
                    h.update(f"ui/{sub}/{f.name}:".encode())
                    h.update(f.read_bytes())
                except Exception:
                    pass
    return h.hexdigest()[:constants.get("build_id_hash_length")]


BUILD_ID = _build_id()


def _avalone_login_url(request: Request) -> str:
    next_url = str(request.url)
    return f"{settings().avalone_base_url}/login?next={next_url}"


@app.middleware("http")
async def auth_gate(request: Request, call_next):
    open_paths = {
        "/manifest.json", "/sw.js", "/healthz",
        "/icon.svg", "/icon-192.png", "/icon-512.png",
        "/api/version", "/api/apps", "/qr",
    }
    path = request.url.path
    tid = external_auth.user_id_of(request)
    # КАЖДЫЙ запрос ставит текущего тенанта в contextvar — все запросы к БД
    # фильтруются по нему (изоляция данных между пользователям).
    tenant.set_current(tid)
    if path not in open_paths and not path.startswith("/static/") and not tid:
        if path.startswith("/api"):
            return JSONResponse({"error": "unauthorized"}, status_code=401)
        return RedirectResponse(_avalone_login_url(request), status_code=303)
    return await call_next(request)


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    tid = tenant.current()
    if not tid or not tenant.is_admin(tid):
        return RedirectResponse(_avalone_login_url(request), status_code=303)
    return _no_cache(templates.TemplateResponse(request, "admin_dashboard.html", {
        "build_id": BUILD_ID,
        "user": tenant.get_user(tid),
    }))


def _no_cache(resp):
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


def _work_app_nav(active_id: str = "trips"):
    entries = [
        {"id": "trips", "label": "Поездки", "icon": "🚐", "url": "/#trips"},
        {"id": "stats", "label": "Статистика", "icon": "📊", "url": "/#stats"},
        {"id": "notifications", "label": "Уведомления", "icon": "🔔", "url": "/#notifications"},
        {"id": "settings", "label": "Настройки", "icon": "⚙️", "url": "/#settings"},
    ]
    for e in entries:
        e["active"] = e["id"] == active_id
    return [{"label": "Работа", "entries": entries}]


def _shell_context_for(request: Request, user, current_app: str = "work", active_id: str = "trips"):
    branches = AvaloneRegistry.for_shell("ru")
    shell = Shell(
        current_app=current_app,
        user=user,
        branches=branches,
        app_nav=_work_app_nav(active_id),
    )
    return {
        "build_id": BUILD_ID,
        "user": user,
        "shell_html": shell.render(templates.env, request),
    }


@app.get("/", response_class=HTMLResponse)
async def app_page(request: Request):
    user = tenant.get_user(tenant.require_current()) if tenant.current() else None
    ctx = _shell_context_for(request, user, current_app="work", active_id="trips")
    return _no_cache(templates.TemplateResponse(request, "work.html", ctx))


@app.get("/join/{invite_code}")
async def join_by_invite(request: Request, invite_code: str):
    try:
        trip = rides.get_trip_by_code(invite_code)
        if not trip:
            return JSONResponse({"error": "invalid invite code"}, status_code=404)
        rides.join_trip_by_code(invite_code)
    except ValueError as e:
        return JSONResponse({"error": str(e)}, status_code=404)
    return RedirectResponse(f"/#trip-{trip['id']}", status_code=303)


@app.get("/manifest.json")
async def manifest():
    return _no_cache(JSONResponse({
        "name": "Работа — Avalone", "short_name": "Работа",
        "start_url": "/", "display": "standalone",
        "background_color": "#0a0c10", "theme_color": "#0a0c10",
        "icons": [
            {"src": f"/icon-192.png?v={BUILD_ID}", "sizes": "192x192", "type": "image/png", "purpose": "any maskable"},
            {"src": f"/icon-512.png?v={BUILD_ID}", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
            {"src": f"/icon.svg?v={BUILD_ID}", "sizes": "any", "type": "image/svg+xml"},
        ],
    }))


@app.get("/icon.svg")
async def icon():
    return _no_cache(FileResponse(BASE / "static" / "icon.svg", media_type="image/svg+xml"))


@app.get("/icon-192.png")
async def icon_192():
    return _no_cache(FileResponse(BASE / "static" / "icon-192.png", media_type="image/png"))


@app.get("/icon-512.png")
async def icon_512():
    return _no_cache(FileResponse(BASE / "static" / "icon-512.png", media_type="image/png"))


@app.get("/qr")
async def qr(url: str = "", size: int = constants.get("qr_default_size")):
    """SVG QR-код для быстрого входа/регистрации."""
    if not url:
        url = config.web_base_url() or "/"
    try:
        import qrcode
        import qrcode.image.svg
        factory = qrcode.image.svg.SvgFragmentImage
        qr = qrcode.QRCode(image_factory=factory, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = BytesIO()
        img.save(buf)
        svg = buf.getvalue()
        return Response(content=svg, media_type="image/svg+xml")
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.get("/sw.js")
async def sw():
    return _no_cache(FileResponse(BASE / "static" / "sw.js", media_type="application/javascript"))


@app.get("/logout")
async def logout():
    return RedirectResponse(f"{settings().avalone_base_url}/login", status_code=303)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.get("/api/version")
async def version():
    return {"build": BUILD_ID}


app.include_router(api_router)


@app.on_event("startup")
async def _ensure_catalog():
    """Идемпотентно гарантируем базовый набор категорий с переводами ru/en/ko —
    чтобы новый пользователь не смотрел в пустой дроплист (см. catalog.DEFAULT_KEYS).
    Сид выполняется для всех существующих тенантов (никакого служебного owner)."""
    _setup_logging()  # uvicorn перезаписывает root-логгер, поэтому ставим handler ещё раз
    import logging
    from routa.core import catalog, money
    for tid in tenant.all_ids():
        tenant.set_current(tid)
        try:
            n = await catalog.ensure_user_catalog()
            if n:
                logging.getLogger(__name__).info("ensure_user_catalog tenant=%s: создано %d категорий", tid, n)
        except Exception:
            logging.getLogger(__name__).exception("ensure_user_catalog tenant=%s", tid)
        try:
            m = await money.ensure_money_seed()
            if m:
                logging.getLogger(__name__).info("ensure_money_seed tenant=%s: засеяно %d денежных счетов", tid, m)
        except Exception:
            logging.getLogger(__name__).exception("ensure_money_seed tenant=%s", tid)
    # этапы B/A глоссария: доменные строки — в единый глоссарий
    # (уведомления, валюты, канонические категории/доходы под нейтральными ключами)
    try:
        from routa.core import currency
        currency.seed_glossary()
        catalog.seed_glossary()
    except Exception:
        logging.getLogger(__name__).exception("glossary domain seed")
    # Гарантируем наличие хотя бы одного администратора Work.
    try:
        tenant.ensure_admin_table()
        if not tenant.list_admins():
            admin_login = "lucifer"
            u = tenant.get_user_by_login(admin_login)
            if u:
                tenant.add_admin(u["id"])
                logging.getLogger(__name__).info(
                    "created default admin: %s (uid=%s)", admin_login, u["id"])
    except Exception:
        logging.getLogger(__name__).exception("ensure default admin")
