# GIThelper

A Python-based Git plugin that helps you merge multiple branches and automatically resolve conflicts. This plugin integrates with Google's Gemini AI to intelligently resolve merge conflicts when needed.

## Features

- Merge multiple branches (2 or more) into a temporary branch
- Clearly show what branches are being merged
- Identify conflicts that occur during merging
- Provide options to resolve conflicts:
  - Manually (choose between versions or create custom resolution)
  - Automatically using Gemini AI
- Show a detailed summary of the merge process

## Requirements

- Python 3.7+
- Git installed and configured
- Google Gemini API Key (for AI-assisted conflict resolution)

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make the script executable:
   ```bash
   chmod +x git_helper.py
   ```
4. Optionally, create a symbolic link to make it available system-wide:
   ```bash
   sudo ln -s $(pwd)/git_helper.py /usr/local/bin/git-helper
   ```

## Usage

### Basic Usage

To merge multiple branches:

```bash
python git_helper.py merge-multi branch1 branch2 [branch3 ...]
```

This will:
1. Create a temporary branch from your current branch
2. Attempt to merge each specified branch into the temporary branch
3. If conflicts occur, help you resolve them
4. Show a summary of the merge process

### Advanced Options

Specify a base branch to merge into:

```bash
python git_helper.py merge-multi --base main branch1 branch2 [branch3 ...]
```

Use AI to automatically resolve conflicts:

```bash
python git_helper.py merge-multi --ai branch1 branch2 [branch3 ...]
```

### Conflict Resolution

When conflicts occur, you have several options:

1. **Manual Resolution**: The tool will show you both versions of the conflicting code and let you choose:
   - Keep your version
   - Keep the other version
   - Keep both versions
   - Enter a custom resolution

2. **AI-Assisted Resolution**: If you use the `--ai` flag, the tool will attempt to use Gemini AI to automatically resolve conflicts. If AI resolution fails, it will fall back to manual resolution.

## API Key Management

The tool can use the Gemini API key stored in the `.env.sh` file. If you're using the `--ai` flag and no API key is found, you'll be prompted to enter one.

## Example

```bash
# Merge feature1 and feature2 branches into a temporary branch based on main
python git_helper.py merge-multi --base main --ai feature1 feature2
```

This will:
1. Create a temporary branch from main
2. Merge feature1 into the temporary branch
3. Merge feature2 into the temporary branch
4. Use Gemini AI to resolve any conflicts
5. Show a summary of the merge process

## Notes

- The tool creates a temporary branch for the merge process, so your original branches remain unchanged
- After reviewing the merged result, you can merge the temporary branch back to your target branch
- The tool provides clear instructions on how to proceed after the merge process is complete