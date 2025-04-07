from fastapi import FastAPI, File, UploadFile, Form
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import tempfile
import os
import requests
from fastapi.exceptions import HTTPException



load_dotenv()

strapi_endpoint = os.getenv("STRAPI_ENDPOINT")
next_endpoint = os.getenv("NEXT_ENDPOINT")


from script import StrapiDocUploader  # import your uploader class

app = FastAPI()

# Enable CORS for your Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_admin_token(token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(f"{strapi_endpoint}/admin/users/me", headers=headers)
    
    if res.status_code == 200:
        return res.json()
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")

@app.post("/upload")
async def upload_docs(
    files: List[UploadFile],
    api_url: str = Form(...),
    api_token: str = Form(...)
):
    
    verify_admin_token(api_token)
    

    uploader = StrapiDocUploader(api_url)

    results = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        blog_data = uploader.parse_doc_file(tmp_path)
        if blog_data:
            result = uploader.upload_to_strapi(blog_data)
            results.append(result)

        os.remove(tmp_path)

    return {"message": "Upload completed", "results": results}
