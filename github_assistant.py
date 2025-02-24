import os
import requests
import google.generativeai as genai
from app import main as get_api_keys

class GitHubAssistant:
    def __init__(self):
        self.github_token = None
        self.gemini_key = None
        self.github_api_url = "https://api.github.com"
        
    def setup_apis(self):
        print("\n=== GitHub & Gemini Assistant Setup ===")
        # Use the new API key management system
        api_keys = get_api_keys()
        if api_keys:
            self.github_token = api_keys.get("GITHUB_API_KEY")
            self.gemini_key = api_keys.get("GEMINI_API_KEY")
            
            # Configure Gemini
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel('gemini-pro')
            return True
        return False

    def get_user_repos(self):
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(f"{self.github_api_url}/user/repos", headers=headers)
            response.raise_for_status()
            repos = response.json()
            
            print("\nYour Repositories:")
            for idx, repo in enumerate(repos, 1):
                print(f"{idx}. {repo['name']} - {repo['description'] or 'No description'}")
            return repos
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            return None

    def get_repo_info(self, repo_name):
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            response = requests.get(
                f"{self.github_api_url}/repos/{repo_name}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository info: {e}")
            return None

    def ask_gemini(self, question):
        try:
            response = self.model.generate_content(question)
            return response.text
        except Exception as e:
            return f"Error getting response from Gemini: {e}"

def main():
    assistant = GitHubAssistant()
    if not assistant.setup_apis():
        print("Failed to set up API keys. Exiting...")
        return
    
    while True:
        print("\n=== GitHub & Gemini Assistant Menu ===")
        print("1. List your repositories")
        print("2. Get repository details")
        print("3. Ask Gemini a question")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            assistant.get_user_repos()
        
        elif choice == "2":
            repo_name = input("Enter repository name (format: owner/repo): ")
            repo_info = assistant.get_repo_info(repo_name)
            if repo_info:
                print("\nRepository Details:")
                print(f"Name: {repo_info['name']}")
                print(f"Description: {repo_info['description']}")
                print(f"Stars: {repo_info['stargazers_count']}")
                print(f"Forks: {repo_info['forks_count']}")
                print(f"Language: {repo_info['language']}")
        
        elif choice == "3":
            question = input("Enter your question for Gemini: ")
            answer = assistant.ask_gemini(question)
            print("\nGemini's Response:")
            print(answer)
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()