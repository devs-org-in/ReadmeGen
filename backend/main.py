# main.py

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from readme_gen import get_repo_info, generate_readme

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GitHub README Generator",
              description="An API that generates README files for GitHub repositories using Groq AI",
              version="1.0.0")

# CORS middleware configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5000",
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
        logger.info(f"Fetching repo info for: {repo_link.repo_link}")
        repo_info = await get_repo_info(repo_link.repo_link)
        logger.info("Successfully fetched repo info")
    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")

    try:
        logger.info("Generating README")
        readme_content = await generate_readme(repo_info)
        logger.info("Successfully generated README")
        return {"readme": readme_content}
    except Exception as e:
        logger.error(f"Failed to generate README: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate README: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)