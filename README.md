# HackRx – LLM Intelligent Query Retrieval System  

## 📌 Project Overview  
This project is an **LLM-powered Intelligent Query Retrieval System** built during **HackRx 5.0**. It is designed to process large, unstructured documents such as **PDFs, Word files, and emails**, and deliver **fast, context-aware answers**.  

The system combines **Pinecone** for vector storage, **Gemini** for ultra-fast inference, and **LLMs for context generation** to provide precise and structured responses.  

## ✨ Key Features  
- 🔍 **Semantic Search with Pinecone** – Stores document embeddings for efficient and relevant retrieval.  
- ⚡ **Gemini-powered Inference** – High-speed, low-latency query handling.  
- 🧠 **Context Generation with LLMs** – Delivers detailed, structured answers with supporting context.  
- 📑 **Multi-format Document Support** – Works with PDFs, Word documents, and email data.  
- 🔐 **Secure API Layer** – Built with FastAPI and token-based authentication.  
- 📊 **Explainable Responses** – Includes sources, metadata, and confidence levels.  

## 🛠️ Tech Stack  
- **Vector Store:** Pinecone  
- **LLM Models:** Gemini + supporting LLMs for context generation  
- **Backend Framework:** FastAPI (with async support)  
- **Authentication:** Bearer Token Security  
- **Document Processing:** Python (text extraction, chunking, embedding)  

## ⚙️ How It Works  
1. **Upload Documents** → PDFs, Word docs, or emails are ingested.  
2. **Preprocessing** → Text is extracted, cleaned, and split into chunks.  
3. **Embedding Generation** → Chunks are embedded and stored in Pinecone.  
4. **Query Input** → User submits a query through the API/UI.  
5. **Vector Search** → Relevant chunks are retrieved from Pinecone.  
6. **LLM Context Generation** → Gemini + LLMs generate structured, context-aware answers.  
7. **Response Delivery** → User receives a JSON response with answer, metadata, and confidence score.  

## 🚀 Getting Started  

### Prerequisites  
- Python 3.9+  
- Pinecone API Key  
- Google Gemini API Key  
- FastAPI & Uvicorn

  
### Installation  
```bash
# Clone the repo
git clone https://github.com/WHitE-TITaN/HackRx-LLM-IntelligentQueryRetrievalSystem.git
cd HackRx-LLM-IntelligentQueryRetrievalSystem

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```


### Environment Variables  
Create a `.env` file in the root directory with:  
```ini
#your PineCorn api key command if for windows
setx API_KEY_PineCone "your_secret_key"
# >SUCCESS: Specified value was saved.
setx PINECONE_ENV "your_hosted_region"
# >SUCCESS: Specified value was saved.

setx API_KEY_GeminiAi "your Gemini api key"
# >SUCCESS: Specified value was saved.

setx  mongo_auth "your api key"
# >SUCCESS: Specified value was saved.

setx default_token "your key for normal users"
# >SUCCESS: Specified value was saved.

setx API_KEY_Cohere "your_secret_key" 
# >SUCCESS: Specified value was saved.
#this set the enviromewnt variable that can be use later.
```

### Run the Server  
```bash
uvicorn app.main:app --reload
```

### API Endpoints  
- `POST /upload` → Upload a document  
- `POST /query` → Submit a query and get context-aware response  
- `GET /health` → Health check endpoint  

## 📚 Example Usage  

#### Upload Document  
```bash
curl -X POST "http://127.0.0.1:8000/upload"      -H "Authorization: Bearer <your_token>"      -F "file=@document.pdf"
```

#### Query the System  
```bash
curl -X POST "http://127.0.0.1:8000/query"      -H "Authorization: Bearer <your_token>"      -H "Content-Type: application/json"      -d '{"query": "What are the key clauses in this contract?"}'
```

Response Example:  
```json
{
  "answer": "The contract includes key clauses on payment, termination, and liability.",
  "sources": ["document.pdf - page 3", "document.pdf - page 7"],
  "confidence": 0.92
}
```

## 📈 Future Improvements  
- Add support for real-time streaming responses.  
- Expand multi-language support.  
- Integrate a simple web dashboard for uploads & queries.  
