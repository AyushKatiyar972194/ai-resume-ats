import logging
import os
import sqlite3
import httpx
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict

logger = logging.getLogger('ats_resume_scorer')

from backend.core.config import SUPABASE_URL, SUPABASE_KEY

DB_PATH = os.path.join(os.path.dirname(__file__), 'ats_history.db')

def _init_sqlite():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    filename TEXT,
                    ats_score REAL,
                    keyword_match REAL,
                    missing_keywords TEXT,
                    analysis_result TEXT,
                    created_at TEXT
                )
            """)
    except Exception as exc:
        logger.error(f"Failed to init sqlite db: {exc}")

_init_sqlite()

def _save_sqlite(user_id: str, filename: str, ats_score: float, keyword_match: float, missing_keywords: list, analysis_result: dict, created_at: str) -> Optional[str]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO analyses (user_id, filename, ats_score, keyword_match, missing_keywords, analysis_result, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    filename,
                    ats_score,
                    keyword_match,
                    json.dumps(missing_keywords),
                    json.dumps(analysis_result),
                    created_at,
                )
            )
            conn.commit()
            return str(cursor.lastrowid)
    except Exception as exc:
        logger.error(f"SQLite save failed: {exc}")
        return None

def _get_sqlite_history(user_id: str) -> List[Dict]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,)
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                try:
                    res_json = json.loads(row['analysis_result']) if row['analysis_result'] else {}
                except Exception:
                    res_json = {}
                try:
                    missing_kw = json.loads(row['missing_keywords']) if row['missing_keywords'] else []
                except Exception:
                    missing_kw = []

                results.append({
                    "id": str(row['id']),
                    "filename": row['filename'] or "resume",
                    "resume_name": row['filename'] or "resume",
                    "job_title": "Software Engineer",
                    "ats_score": row['ats_score'] or 0,
                    "keyword_match": row['keyword_match'] or 0,
                    "missing_keywords": missing_kw,
                    "date": row['created_at'] or "",
                    "created_at": row['created_at'] or "",
                    "analysis_result": res_json,
                })
            return results
    except Exception as exc:
        logger.error(f"SQLite fetch failed: {exc}")
        return []

def _delete_sqlite(analysis_id: str, user_id: str) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analyses WHERE id = ? AND user_id = ?", (analysis_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as exc:
        logger.error(f"SQLite delete failed: {exc}")
        return False

def _get_headers():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

async def save_analysis(user_id: str, filename: str, analysis_result: Dict) -> Optional[str]:
    def _json_default(o):
        if hasattr(o, 'model_dump'):
            return o.model_dump()
        return str(o)
    serializable_result = json.loads(json.dumps(analysis_result, default=_json_default))

    ats_score = serializable_result.get("ats_score", 0) or serializable_result.get("ATS_score", 0)
    keyword_match = serializable_result.get("keyword_match", 0)
    missing_keywords = serializable_result.get("missing_keywords", [])
    now_iso = datetime.now(timezone.utc).isoformat()

    # 1. Always save to local SQLite so history is guaranteed to persist immediately
    local_id = _save_sqlite(
        user_id=user_id,
        filename=filename,
        ats_score=ats_score,
        keyword_match=keyword_match,
        missing_keywords=missing_keywords,
        analysis_result=serializable_result,
        created_at=now_iso,
    )

    # 2. Also try to persist to Supabase if configured
    headers = _get_headers()
    if headers and SUPABASE_URL:
        doc = {
            "user_id": user_id,
            "filename": filename,
            "ats_score": ats_score,
            "keyword_match": keyword_match,
            "missing_keywords": missing_keywords,
            "created_at": now_iso,
            "analysis_result": serializable_result,
        }
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, headers=headers, json=doc)
                if response.status_code in (200, 201):
                    data = response.json()
                    if data and len(data) > 0:
                        supabase_id = str(data[0].get("id"))
                        logger.info(f"Saved analysis to Supabase: {supabase_id}")
                        return supabase_id
                else:
                    logger.warning(f"Supabase returned status {response.status_code} when saving analysis: {response.text}")
        except Exception as exc:
            logger.warning(f"Failed to save analysis to Supabase ({exc}), local record saved as fallback.")

    return local_id

async def get_user_history(user_id: str) -> List[Dict]:
    # 1. Try Supabase first
    headers = _get_headers()
    if headers and SUPABASE_URL:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    url, 
                    headers=headers, 
                    params={
                        "user_id": f"eq.{user_id}",
                        "order": "created_at.desc"
                    }
                )
                if response.status_code == 200:
                    docs = response.json()
                    if docs:
                        results = []
                        for doc in docs:
                            results.append({
                                "id": str(doc.get("id")),
                                "filename": doc.get("filename", "resume"),
                                "resume_name": doc.get("filename", "resume"),
                                "job_title": "Software Engineer",
                                "ats_score": doc.get("ats_score", 0),
                                "keyword_match": doc.get("keyword_match", 0),
                                "missing_keywords": doc.get("missing_keywords", []),
                                "date": doc.get("created_at", ""),
                                "created_at": doc.get("created_at", ""),
                                "analysis_result": doc.get("analysis_result", {}),
                            })
                        return results
        except Exception as exc:
            logger.warning(f"Failed to fetch history from Supabase: {exc}")

    # 2. Fall back to local SQLite storage
    return _get_sqlite_history(user_id)

async def delete_analysis(analysis_id: str, user_id: str) -> bool:
    # 1. Delete from local SQLite
    deleted_local = _delete_sqlite(analysis_id, user_id)

    # 2. Also try Supabase
    headers = _get_headers()
    if headers and SUPABASE_URL:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/analyses"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(
                    url, 
                    headers=headers, 
                    params={
                        "id": f"eq.{analysis_id}",
                        "user_id": f"eq.{user_id}"
                    }
                )
                if response.status_code in (200, 204):
                    return True
        except Exception as exc:
            logger.warning(f"Failed to delete analysis from Supabase: {exc}")

    return deleted_local
