# main.py
import asyncio
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Try to import your real AI pipeline functions. If not available, use stubs so server still runs.
try:
    # Expecting a function that returns a dict of stats when called once.
    # If your pipeline is designed to run continuously, you can expose a "process_stream_once"
    # or wrap the continuous function to return the latest snapshot.
    from backend.ai_pipeline import process_stream_once as process_stream_once  # type: ignore
except Exception:
    async def process_stream_once() -> Dict[str, Any]:
        """Fallback stub that simulates analysis output — replace with real function."""
        await asyncio.sleep(0.1)
        return {
            "rally_count": 0,
            "heatmaps": {},
            "player_stats": {},
            "last_updated": None,
        }


try:
    from backend.insights import generate_insights  # type: ignore
except Exception:
    def generate_insights(stats: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback insights generator."""
        return {"tips": ["AI pipeline not loaded — no tips available yet."]}


app = FastAPI(title="Smart Padel Court - API")
# serve static (css/js/images) from frontend/static
frontend_static = Path("frontend/static")
if frontend_static.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")


# Globals to hold latest computed stats
LATEST_STATS: Dict[str, Any] = {"status": "starting", "stats": {}, "tips": {}}
PROCESSING_INTERVAL_SECONDS = 1.0  # how often to poll process_stream_once for new stats


@app.on_event("startup")
async def startup_event():
    """Start background task to continuously update stats."""
    asyncio.create_task(_processing_loop())


async def _processing_loop():
    """Continuously call the processing function and update LATEST_STATS.

    This uses asyncio.to_thread to safely run sync functions without blocking the event loop.
    """
    global LATEST_STATS
    while True:
        try:
            # Support both async and sync process_stream_once implementations:
            if asyncio.iscoroutinefunction(process_stream_once):
                stats = await process_stream_once()
            else:
                stats = await asyncio.to_thread(process_stream_once)

            # Generate human-friendly tips/insights
            try:
                tips = generate_insights(stats)
            except Exception:
                tips = {"error": "insights generation failed"}

            LATEST_STATS = {
                "status": "ok",
                "stats": stats,
                "tips": tips,
            }
        except Exception as e:
            # Keep server alive; store last error for debugging
            LATEST_STATS = {
                "status": "error",
                "error": repr(e),
                "stats": LATEST_STATS.get("stats", {}),
                "tips": LATEST_STATS.get("tips", {}),
            }

        # Wait before next polling cycle
        await asyncio.sleep(PROCESSING_INTERVAL_SECONDS)


def _read_frontend_html(name: str) -> str:
    """Read an HTML file from frontend/ and return content or raise HTTPException."""
    html_path = Path("frontend") / name
    if not html_path.exists():
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return html_path.read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def home():
    """Return main analysis page (analysis.html)"""
    return _read_frontend_html("analysis.html")


@app.get("/analysis.html", response_class=HTMLResponse)
async def analysis_page():
    return _read_frontend_html("analysis.html")


@app.get("/technique.html", response_class=HTMLResponse)
async def technique_page():
    return _read_frontend_html("technique.html")


@app.get("/tactical.html", response_class=HTMLResponse)
async def tactical_page():
    return _read_frontend_html("tactical.html")


@app.get("/highlights.html", response_class=HTMLResponse)
async def highlights_page():
    return _read_frontend_html("highlights.html")


@app.get("/api/stats", response_class=JSONResponse)
async def api_stats():
    """Return latest computed stats and tips."""
    if LATEST_STATS is None:
        raise HTTPException(status_code=503, detail="Stats not available yet")
    return LATEST_STATS


if __name__ == "__main__":
    # For local dev / Replit: run uvicorn programmatically
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
