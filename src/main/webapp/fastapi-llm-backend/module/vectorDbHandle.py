from pinecone import Pinecone, ServerlessSpec
import cohere
from os import getenv

class VectorDbHandle:
    def __init__(self):
        # Initialize Pinecone with the API key from environment variables
        self.pineCone_key = getenv("API_KEY_PineCone")
        self.cohere_key = getenv("API_KEY_Cohere")
        self.pineCone_env = getenv("PINECONE_ENV")

        if not self.pineCone_key or not self.cohere_key:
          raise ValueError("Missing API keys in environment variables.")

        self.pinecone = Pinecone(api_key=self.pineCone_key)
        self.index_name = "hackrx"

    def createEmbedding(self, textChunk: list[str], file_id: str) -> list:
        embbedCohere = cohere.Client(self.cohere_key)
        index = self.pinecone.Index(self.index_name)

        batch_size = 32
        for i in range(0, len(textChunk), batch_size):
            batch_text = textChunk[i:i + batch_size]
            embeddings = embbedCohere.embed(texts=batch_text, model="embed-english-v3.0").embeddings

            vectors = [
              {
                  "id": f"{file_id}-chunk-{i + j}",
                  "values": embedding,
                  "metadata": {"text": batch_text[j]}
              }
              for j, embedding in enumerate(embeddings)
            ]
            index.upsert(vectors=vectors)
            print("✅ Embeddings uploaded to Pinecone!")


        
