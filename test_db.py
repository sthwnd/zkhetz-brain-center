from supabase import create_client

SUPABASE_URL = "https://knodraujylbsglscdrgh.supabase.co"
SUPABASE_KEY = "sb_publishable_NMHD3aib86R8k-fw7mTC9Q_k2QtoFNc"

# Connect
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Test: Insert a row
result = supabase.table("pipeline_runs").insert({
    "date": "2024-12-31",
    "status": "test",
    "items_collected": 0,
    "items_processed": 0
}).execute()

print("Insert result:", result)

# Test: Read it back
result = supabase.table("pipeline_runs").select("*").execute()
print("All rows:", result.data)

# Clean up: Delete test row
supabase.table("pipeline_runs").delete().eq("status", "test").execute()
print("Test row deleted")

print("\n✅ Database connection works!")