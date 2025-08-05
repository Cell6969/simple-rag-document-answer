# Home Quiz: Python Developer
## Simple RAG for answer user question based on document
AI - Powered Used:
- Vector DB (Qdrant)
- LLM (Open AI)
- SentenceTransformer (all-MiniLM-L6-v2)

## Project Structure
```markdown
.
├── app.py                # Flask API entry point
├── ingest
│   └── ingest.py       # Script to ingest documents into Qdrant
├── .env                  
├── requirements.txt      # Dependencies
├── rag
│   └── rag.py            # Script to answer user question based on document
├── data/                 # Folder with text documents
├── example.json          # Sample input/output
├── run.sh                # Script to run app and ingest
├── wait-for.sh           # Script to wait for Qdrant to start
└── README.md
```

## Quickstart without docker
### 1. Set environment variables
Create a .env file based on .env.example. Provide: 
- OPENAI_API_KEY
- QDRANT_HOST
- QDRANT_PORT

### 2. Setup Qdrant
for setup qdrant, can be done using docker locally
```sh
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant:latest
```

### 2. Install Library
```bash
pip install -r requirements.txt
```

### 3. Ingest documents
```bash
python ingest.py
```

### 4. Run API
```bash
python app.py
```

## Quickstart with docker
### 1. Set environment variables
Create a .env file based on .env.example. Provide: 
- OPENAI_API_KEY
- QDRANT_HOST
- QDRANT_PORT
### 2. Build and run docker
```bash
docker-compose build --no-cache
docker-compose up
```

## Parameters
- question: user question (required:true)
- top_k: number of documents to retrieve by most relevan (default: 3, required:false)
