import sys
import os

# Adiciona o diretório raiz ao sys.path para importações absolutas funcionarem
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from backend.api.routes import router as api_router  # noqa: E402
from backend.core.config import settings  # noqa: E402
from backend.core.database import init_db  # noqa: E402

# Initialize database
init_db()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api")

# Mount static files directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    # Return the Chat UI
    return FileResponse(os.path.join(static_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
