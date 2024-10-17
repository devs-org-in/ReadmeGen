# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from readme_gen import get_repo_info, generate_readme

app = FastAPI(title="GitHub README Generator",
              description="An API that generates README files for GitHub repositories using Groq AI",
              version="1.0.0")

# CORS middleware configuration
origins = [
    "http://localhost:3000",  # React default development port
    "http://localhost:5000",  # Another common development port
    # Add any other origins (frontend URLs) you want to allow
    # "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoLink(BaseModel):
    repo_link: str

class ReadmeResponse(BaseModel):
    readme: str

@app.post("/generate_readme", response_model=ReadmeResponse)
async def generate_readme_api(repo_link: RepoLink):
    if not repo_link.repo_link:
        raise HTTPException(status_code=400, detail="No repository link provided")

    try:
        repo_info = await get_repo_info(repo_link.repo_link)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repository information: {str(e)}")

    try:
        readme_content = await generate_readme(repo_info)
        return {"readme": readme_content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate README: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)