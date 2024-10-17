import os
from github import Github
import groq
from dotenv import load_dotenv
# Set up Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")
groq_client = groq.Groq(api_key=groq_api_key)

def get_repo_info(repo_link):
    parts = repo_link.split('/')
    username = parts[-2]
    repo_name = parts[-1]

    g = Github()
    repo = g.get_repo(f"{username}/{repo_name}")

    description = repo.description or "No description provided."
    stars = repo.stargazers_count
    forks = repo.forks_count
    language = repo.language or "Not specified"
    
    contents = repo.get_contents("")
    files = [content.name for content in contents if content.type == "file"]
    
    return {
        "name": repo_name,
        "description": description,
        "stars": stars,
        "forks": forks,
        "language": language,
        "files": files,
        "clone_url": repo.clone_url
    }

def generate_readme(repo_info):
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

    response = groq_client.chat.completions.create(
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
    
    return response.choices[0].message.content