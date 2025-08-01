import os
import vertexai
import config

from vertexai import rag
from cache import CacheManager

# --- Cache Cleaning ---
print("🧹 Clearing Caches...")
CacheManager().list_caches(cleanup=True)
print("✅ Caches cleared successfully.")

# --- RAG Corpora Cleaning ---
print("\n🧹 Clearing RAG Corpora...")
vertexai.init(project=config.PROJECT_ID, location=config.LOCATION_RAG)

corpora_found = False
for corpora in rag.list_corpora():
    if corpora.display_name == config.RAG_CORPUS_DISPLAY_NAME:
        corpora_found = True
        print(f"   - Deleting Corpus: {corpora.display_name} ({corpora.name})")
        try:
            rag.delete_corpus(corpora.name)
            print(f"   ✅ Corpus '{corpora.display_name}' deleted.")
        except Exception as e:
            print(f"   ❌ Error deleting corpus '{corpora.display_name}': {e}")

if not corpora_found:
    print("   ℹ️ No RAG Corpora to clean up.")

# --- Flag File Cleaning ---
print("\n🧹 Clearing Flag Files...")
files_to_remove = [config.CACHE_FILE, config.RAG_CORPUS_NAME_FILE]
files_removed = False

for f in files_to_remove:
    if os.path.exists(f):
        try:
            os.remove(f)
            print(f"   ✅ Removed: {f}")
            files_removed = True
        except OSError as e:
            print(f"   ❌ Error removing file {f}: {e}")
    else:
        print(f"   ℹ️ File not found, skipping: {f}")

if not files_removed:
    print("   ℹ️ No flag files to remove.")

print("\n✨ Cleanup complete! ✨")
