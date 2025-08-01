import vertexai
import cache
import config

from vertexai import rag


# Clearing Caches
print("--------------------")
print("--------Cache-----------")
print("--------------------")
from cache import CacheManager

CacheManager().list_caches(cleanup=True)

# Clearing RAG Corpora
print("--------------------")
print("--------RAG Corpora-----------")
print("--------------------")
vertexai.init(project=config.PROJECT_ID, location=config.LOCATION_RAG)

for corpora in rag.list_corpora():
    if corpora.display_name != config.RAG_CORPUS_DISPLAY_NAME:
        continue
    print(f"Name: {corpora.display_name} | {corpora.name}")
    rag.delete_corpus(corpora.name)
    print(f"Name: {corpora.display_name} | {corpora.name} deleted!")
