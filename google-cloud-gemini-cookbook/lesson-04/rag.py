import google.generativeai as genai


class RagManager:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.model_name = model_name
        self.corpus = []  # list of documents
        self.corpus_embeddings = []  # list of embeddings

    def add_to_corpus(self, documents: list[str]):
        """Adds documents to the corpus and generates embeddings."""
        self.corpus.extend(documents)
        print(f"Adding {len(documents)} documents to the corpus.")
        response = genai.embed_content(
            model="models/text-embedding-004",
            content=documents,
            task_type="retrieval_document",
        )
        self.corpus_embeddings.extend(response["embedding"])
        print("Embeddings generated.")

    def query(self, query: str, top_k=3):
        """Queries the corpus and returns a response from the generative model."""
        query_embedding = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query",
        )["embedding"]

        # Find the most similar documents in the corpus
        similarities = self._cosine_similarity(query_embedding, self.corpus_embeddings)
        top_k_indices = sorted(
            range(len(similarities)), key=lambda i: similarities[i], reverse=True
        )[:top_k]
        top_k_documents = [self.corpus[i] for i in top_k_indices]

        # Prepare the context for the generative model
        context = "\n".join(top_k_documents)
        prompt = f"""
        You are a helpful assistant. Answer the user's question based on the following context:
        Context:
        {context}

        Question: {query}
        """

        # Generate the response
        model = genai.GenerativeModel(self.model_name)
        response = model.generate_content(prompt)
        return response.text

    def _cosine_similarity(self, vec1, vec2_list):
        """Calculates cosine similarity between a vector and a list of vectors."""
        similarities = []
        for vec2 in vec2_list:
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm_vec1 = sum(a * a for a in vec1) ** 0.5
            norm_vec2 = sum(b * b for b in vec2) ** 0.5
            if norm_vec1 == 0 or norm_vec2 == 0:
                similarities.append(0)
            else:
                similarities.append(dot_product / (norm_vec1 * norm_vec2))
        return similarities


if __name__ == "__main__":
    # Example usage
    rag = RagManager()
    documents = [
        "The sky is blue.",
        "The sun is bright.",
        "The moon is a natural satellite of the Earth.",
        "Gemini is a family of multimodal models developed by Google.",
        "Streamlit is an open-source Python library that makes it easy to create and share beautiful, custom web apps for machine learning and data science.",
    ]
    rag.add_to_corpus(documents)

    question = "What is Gemini?"
    answer = rag.query(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

    question = "What is streamlit?"
    answer = rag.query(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
