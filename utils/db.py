from supabase import create_client
from datetime import datetime, timedelta
import os

# Config - use env vars with fallback defaults
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://knodraujylbsglscdrgh.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_publishable_NMHD3aib86R8k-fw7mTC9Q_k2QtoFNc")

# Global client (lazy initialized)
_supabase_client = None


def get_supabase():
    """Get Supabase client, creating new one if needed."""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def reconnect():
    """Force reconnection to Supabase."""
    global _supabase_client
    _supabase_client = None
    return get_supabase()


def save_raw_items(items, retry=True):
    """Save raw items to database."""
    if not items:
        return 0
    
    supabase = get_supabase()
    
    try:
        for i in range(0, len(items), 100):
            batch = items[i:i+100]
            supabase.table("raw_items").insert(batch).execute()
        return len(items)
    except Exception as e:
        if retry:
            print(f"Connection error, retrying... ({e})")
            reconnect()
            return save_raw_items(items, retry=False)
        raise


def get_raw_items(limit=2500, retry=True):
    """Get all raw items from last 7 days."""
    cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat()
    supabase = get_supabase()
    
    try:
        all_items = []
        offset = 0
        batch_size = 1000
        
        while len(all_items) < limit:
            result = (
                supabase.table("raw_items")
                .select("*")
                .gte("collected_at", cutoff)
                .range(offset, offset + batch_size - 1)
                .execute()
            )
            all_items.extend(result.data)
            if len(result.data) < batch_size:
                break
            offset += batch_size
        
        return all_items[:limit]
    except Exception as e:
        if retry:
            print(f"Connection error, retrying... ({e})")
            reconnect()
            return get_raw_items(limit, retry=False)
        raise


def get_freshness_hours():
    today = datetime.now()
    if today.weekday() == 6:
        return 72
    return 24


def get_raw_items_with_freshness(limit=2500):
    items = get_raw_items(limit)
    fresh_hours = get_freshness_hours()
    fresh_cutoff = datetime.utcnow() - timedelta(hours=fresh_hours)
    
    for item in items:
        published = item.get("published_at")
        if published:
            try:
                if isinstance(published, str):
                    pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00").replace("+00:00", ""))
                else:
                    pub_dt = published
                item["is_fresh"] = pub_dt >= fresh_cutoff
            except:
                item["is_fresh"] = False
        else:
            created = item.get("created_at")
            if created:
                try:
                    if isinstance(created, str):
                        created_dt = datetime.fromisoformat(created.replace("Z", "+00:00").replace("+00:00", ""))
                    else:
                        created_dt = created
                    item["is_fresh"] = created_dt >= fresh_cutoff
                except:
                    item["is_fresh"] = False
            else:
                item["is_fresh"] = False
    
    return items


def clear_raw_items():
    supabase = get_supabase()
    supabase.table("raw_items").delete().neq("title", "").execute()


def clear_daily_items():
    supabase = get_supabase()
    supabase.table("daily_items").delete().neq("headline", "").execute()


def clear_old_raw_items(days=7):
    supabase = get_supabase()
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
    supabase.table("raw_items").delete().lt("collected_at", cutoff).execute()
    print(f"Cleared items older than {days} days")


supabase = get_supabase()
