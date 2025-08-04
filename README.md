# HackRx-LLM-IntelligentQueryRetrievalSystem

### Install libraries.
> for project to work it need basic libraries use this command to install them

```bash
python -m venv venv
venv\Script\Activate
cd src/main/webapp/fastapi-llm-backend/utils
pip install -r requirment.txt 
```

### after installation we need Enviromewnt to be setuped.
```bash
#your PineCorn api key command if for windows
setx API_KEY_PineCone "your_secret_key"
# >SUCCESS: Specified value was saved.
setx PINECONE_ENV "your_hosted_region"
# >SUCCESS: Specified value was saved.


setx API_KEY_Cohere "your_secret_key"
# >SUCCESS: Specified value was saved.
#this set the enviromewnt variable that can be use later.
```

### run python in virtual enviroment.
> run Python Backend First 

``` bash
cd webapp/fastapi-llm-backend
uvicorn main:app --reload
```
