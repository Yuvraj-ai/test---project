# GitHub & Gemini Assistant

A Python-based CLI tool that combines GitHub API and Google's Gemini AI to help you manage repositories and get AI-powered answers to your questions.

## Features

- List your GitHub repositories
- Get detailed information about specific repositories
- Ask questions to Gemini AI
- Secure token handling using getpass

## Requirements

- Python 3.7+
- GitHub Personal Access Token
- Google Gemini API Key

## Setup

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Get your API keys:
   - [Create a GitHub Personal Access Token](https://github.com/settings/tokens)
   - [Get a Gemini API Key](https://makersuite.google.com/app/apikey)

## Usage

Run the script:
```bash
python github_assistant.py
```

The program will prompt you for:
1. Your GitHub token
2. Your Gemini API key

Then you can:
- List your repositories
- Get detailed repository information
- Ask questions to Gemini AI
<br>
this is a test repo
<br>
WOrKING / 
Testing
Author --> Yuvraj Singh on Ipad pro

## New Feature: GIThelper Plugin

A new Git plugin has been added to help you merge multiple branches and automatically resolve conflicts. This plugin integrates with Google's Gemini AI to intelligently resolve merge conflicts when needed.

### GIThelper Features

- Merge multiple branches (2 or more) into a temporary branch
- Clearly show what branches are being merged
- Identify conflicts that occur during merging
- Provide options to resolve conflicts:
  - Manually (choose between versions or create custom resolution)
  - Automatically using Gemini AI
- Show a detailed summary of the merge process

### Using GIThelper

For detailed instructions on how to use the GIThelper plugin, see [GITHELPER_README.md](GITHELPER_README.md).

Basic usage:
```bash
python git_helper.py merge-multi branch1 branch2 [branch3 ...]
```

For AI-assisted conflict resolution:
```bash
python git_helper.py merge-multi --ai branch1 branch2 [branch3 ...]
```