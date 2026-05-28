import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from backend.services.rag_service import rag_service
query = "search_query: O marido pode retirar a esposa do seguro saúde?"
docs_with_scores = rag_service.vector_store.similarity_search_with_score(query, k=4)
for i, (doc, score) in enumerate(docs_with_scores):
    print(f"--- Score: {score} ---")
    print(doc.page_content.split('\n')[0].encode("utf-8", "ignore").decode("utf-8"))





