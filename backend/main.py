# import os
# import json
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from googletrans import Translator
# from datetime import datetime
# from dotenv import load_dotenv

# # Google Docs imports
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# load_dotenv()

# GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")

# if not GOOGLE_DOC_ID:
#     raise RuntimeError("GOOGLE_DOC_ID not set in .env")

# app = FastAPI()

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# translator = Translator()

# # Initialize Google Docs API
# SCOPES = [
#     'https://www.googleapis.com/auth/documents', 
#     'https://www.googleapis.com/auth/drive'
# ]

# # Load credentials
# if os.path.exists('credentials.json'):
#     credentials = service_account.Credentials.from_service_account_file(
#         'credentials.json', scopes=SCOPES)
# else:
#     creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
#     if creds_json:
#         creds_dict = json.loads(creds_json)
#         credentials = service_account.Credentials.from_service_account_info(
#             creds_dict, scopes=SCOPES)
#     else:
#         raise RuntimeError("No credentials found")

# docs_service = build('docs', 'v1', credentials=credentials)


# def save_to_google_doc(original_text: str, translated_text: str, doc_id: str):
#     """Append translation data to Google Doc"""
#     content = f"{'='*60}\n{original_text} → {translated_text}\n{'='*60}\n\n"
    
#     requests = [
#         {
#             'insertText': {
#                 'location': {'index': 1},
#                 'text': content
#             }
#         }
#     ]
    
#     docs_service.documents().batchUpdate(
#         documentId=doc_id,
#         body={'requests': requests}
#     ).execute()


# class TextRequest(BaseModel):
#     text: str


# @app.get("/")
# async def root():
#     return {"message": "Bangla Translation API is running"}


# @app.post("/translate")
# async def translate(request: TextRequest):
#     """Translate and save to Google Doc"""
#     try:
#         # Translate
#         result = translator.translate(request.text, dest="bn")
        
#         response_data = {
#             "original": request.text,
#             "bangla": result.text,
#             "timestamp": datetime.now().isoformat(),
#             "saved": False
#         }
        
#         # Save to Google Doc
#         try:
#             save_to_google_doc(request.text, result.text, GOOGLE_DOC_ID)
#             response_data["saved"] = True
#             print(f"✓ Saved to Google Doc")
#         except Exception as e:
#             print(f"❌ Error saving to Google Doc: {e}")
        
#         return response_data
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000) 



import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googletrans import Translator
from datetime import datetime
from dotenv import load_dotenv

# Google Docs imports
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

# GOOGLE_DOC_ID = os.getenv("GOOGLE_DOC_ID")
GOOGLE_DOC_ID = "1vdU7gUgnCJduBsxXe3KtYXmr4w5q_mdNZD8CgfncOiY"


if not GOOGLE_DOC_ID:
    raise RuntimeError("GOOGLE_DOC_ID not set in .env")

app = FastAPI()

# CORS - Updated configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600
)

translator = Translator()

# Initialize Google Docs API
SCOPES = [
    'https://www.googleapis.com/auth/documents', 
    'https://www.googleapis.com/auth/drive'
]

# Load credentials
try:
    if os.path.exists('credentials.json'):
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        print("✓ Credentials loaded from file")
    else:
        creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if creds_json:
            creds_dict = json.loads(creds_json)
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=SCOPES)
            print("✓ Credentials loaded from environment")
        else:
            raise RuntimeError("No credentials found")

    docs_service = build('docs', 'v1', credentials=credentials)
    print("✓ Google Docs service initialized")
except Exception as e:
    print(f"❌ Error initializing: {e}")
    raise


def save_to_google_doc(original_text: str, translated_text: str, doc_id: str):
    """Append translation data to Google Doc"""
    content = f"{'='*60}\n{original_text} → {translated_text}\n{'='*60}\n\n"
    
    requests = [
        {
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }
    ]
    
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': requests}
    ).execute()


class TextRequest(BaseModel):
    text: str


@app.get("/")
async def root():
    return {
        "message": "Bangla Translation API is running",
        "version": "1.0",
        "status": "healthy"
    }


@app.options("/translate")
async def translate_options():
    """Handle OPTIONS request for CORS preflight"""
    return {"message": "OK"}


@app.post("/translate")
async def translate(request: TextRequest):
    """Translate and save to Google Doc"""
    try:
        print(f"Translating: {request.text}")
        
        # Translate
        result = translator.translate(request.text, dest="bn")
        
        response_data = {
            "original": request.text,
            "bangla": result.text,
            "timestamp": datetime.now().isoformat(),
            "saved": False
        }
        
        # Skip test data
        skip_words = ["string", "test", "example"]
        if request.text.strip().lower() not in skip_words and request.text.strip():
            try:
                save_to_google_doc(request.text, result.text, GOOGLE_DOC_ID)
                response_data["saved"] = True
                print(f"✓ Saved to Google Doc: {request.text}")
            except Exception as e:
                print(f"❌ Error saving to Google Doc: {e}")
        else:
            print(f"⚠ Skipped test data: {request.text}")
        
        return response_data
        
    except Exception as e:
        print(f"❌ Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)