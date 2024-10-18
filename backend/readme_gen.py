# readme_generator.py

import os
import logging
from github import Github
from github.GithubException import UnknownObjectException, RateLimitExceededException
import groq
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    logger.error("GROQ_API_KEY environment variable is not set")
    raise ValueError("GROQ_API_KEY environment variable is not set")

groq_client = groq.Groq(api_key=groq_api_key)

async def get_repo_info(repo_link):
    try:
        parts = repo_link.split('/')
        username = parts[-2]
        repo_name = parts[-1].rstrip('.git')  # Remove .git if present

        logger.info(f"Fetching info for repo: {username}/{repo_name}")
        g = Github()
        repo = await asyncio.to_thread(g.get_repo, f"{username}/{repo_name}")

        description = repo.description or "No description provided."
        stars = repo.stargazers_count
        forks = repo.forks_count
        language = repo.language or "Not specified"
        
        contents = await asyncio.to_thread(repo.get_contents, "")
        files = [content.name for content in contents if content.type == "file"]
        
        logger.info(f"Successfully fetched info for repo: {username}/{repo_name}")
        return {
            "name": repo_name,
            "description": description,
            "stars": stars,
            "forks": forks,
            "language": language,
            "files": files,
            "clone_url": repo.clone_url
        }
    except UnknownObjectException:
        logger.error(f"Repository not found: {repo_link}")
        raise ValueError(f"The repository '{repo_link}' does not exist or is not publicly accessible.")
    except RateLimitExceededException:
        logger.error("GitHub API rate limit exceeded")
        raise ValueError("GitHub API rate limit exceeded. Please try again later.")
    except Exception as e:
        logger.error(f"Error fetching repo info: {str(e)}", exc_info=True)
        raise ValueError(f"An error occurred while fetching repository information: {str(e)}")

# The generate_readme function remains the same
    # ... (keep the existing implementation)

async def generate_readme(repo_info):
    try:
        prompt = f"""Generate a comprehensive README for the following GitHub repository:

Repository Name: {repo_info['name']}
Description: {repo_info['description']}
Stars: {repo_info['stars']}
Forks: {repo_info['forks']}
Primary Language: {repo_info['language']}
Files in Root Directory: {', '.join(repo_info['files'])}

Please include the following sections:
1. Project Title
2. Description
3. Features
4. Installation
5. Usage
6. Contributing
7. License

Use Markdown formatting and make the README informative and well-structured."""

        logger.info("Sending request to Groq API")
        response = await asyncio.to_thread(
            groq_client.chat.completions.create,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that generates README files for GitHub repositories."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=1000
        )
        
        logger.info("Successfully received response from Groq API")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating README: {str(e)}", exc_info=True)
        raise