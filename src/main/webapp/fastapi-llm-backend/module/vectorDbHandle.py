from pinecone import Pinecone, ServerlessSpec
import cohere
import numpy as np
from os import getenv

class VectorDbHandle:
    def __init__(self):
        # Initialize Pinecone with the API key from environment variables
        #get all api keys
        self.pineCone_key = getenv("API_KEY_PineCone")
        self.cohere_key = getenv("API_KEY_Cohere")
        self.pineCone_env = getenv("PINECONE_ENV")

        #check if the keys are missing
        if not self.pineCone_key or not self.cohere_key:
          raise ValueError("Missing API keys in environment variables.")

        # Initialize Pinecone and Cohere clients
        self.pinecone = Pinecone(api_key=self.pineCone_key)
        self.index_name = "hackrx"





    async def createEmbedding(self, textChunk: list[str], file_id: str) -> list:
        embbedCohere = cohere.Client(self.cohere_key)
        index = self.pinecone.Index(self.index_name)

        batch_size = 32

        fileCheck = index.fetch(ids=[f"{file_id}-chunk-0"])
        exists = bool(fileCheck.vectors) 

        if exists:
            
            print("✅ Embeddings already uploaded to Pinecone!")
        else :

            for i in range(0, len(textChunk), batch_size):
                batch_text = textChunk[i:i + batch_size]
                try:
                    embeddings = embbedCohere.embed(
                        texts=batch_text, 
                        model="embed-english-v3.0", 
                        input_type="search_document"
                        ).embeddings
                except cohere.CohereAPIError as e:
                    print(f"❌ Cohere API error: {e}")
                    continue

                vectors = [
                {
                    "id": f"{file_id}-chunk-{i + j}",
                    "values": embedding,
                    "metadata": {"text": batch_text[j]}
                }
                for j, embedding in enumerate(embeddings)
                ]
                try:
                    index.upsert(vectors=vectors)
                    print("✅ Embeddings uploaded to Pinecone!")
                except Exception as e:
                    print(f"❌ Failed to upsert to Pinecone: {e}")
                




    # Deletes embeddings for a specific file ID
    # after processing all the requests.
    def deleteEmbedding(self, file_id: str) -> None:
        index = self.pinecone.Index(self.index_name)
        try:
            index.delete(ids=[f"{file_id}-chunk-{i}" for i in range(1000)])  # Adjust range as needed
            print(f"✅ Deleted embeddings for file ID: {file_id}")
        except Exception as e:
            print(f"❌ Failed to delete embeddings: {e}")  




    
    # retreavte the data based on the  
    def retreaveData(self, query: str, topK: int = 5) -> list[str]:
        embbedCohere = cohere.Client(self.cohere_key)
        query_embedding = embbedCohere.embed(
            texts=[query],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings  # Only one query, so take the first


        overallQuery = np.mean(query_embedding, axis = 0).tolist()  # Convert to list for Pinecone
        # Connect to the Pinecone index
        index = self.pinecone.Index(self.index_name)

        # Query Pinecone
        results = index.query(
            vector=overallQuery,
            top_k=topK,
            include_metadata=True  # So we get the text back!
        )

        # Extract and return metadata (text chunks)
        matched_texts = [match['metadata']['text'] for match in results['matches']]
        return matched_texts
