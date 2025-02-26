#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import tempfile
import re
import google.generativeai as genai
from app import load_api_keys

class GitHelper:
    def __init__(self, gemini_api_key=None):
        self.repo_path = os.getcwd()
        self.gemini_api_key = gemini_api_key
        
        # Initialize Gemini if API key is provided
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def _run_git_command(self, command, capture_output=True):
        """Run a git command and return its output"""
        try:
            result = subprocess.run(
                command, 
                cwd=self.repo_path, 
                check=True, 
                text=True, 
                shell=True, 
                capture_output=capture_output
            )
            return result.stdout.strip() if capture_output else True
        except subprocess.CalledProcessError as e:
            print(f"Error executing git command: {e}")
            if capture_output and e.stdout:
                print(f"Output: {e.stdout}")
            if e.stderr:
                print(f"Error: {e.stderr}")
            return None
    
    def get_current_branch(self):
        """Get the name of the current branch"""
        return self._run_git_command("git rev-parse --abbrev-ref HEAD")
    
    def get_all_branches(self):
        """Get a list of all branches in the repository"""
        branches = self._run_git_command("git branch")
        if branches:
            # Parse branch names from the output
            return [b.strip('* ') for b in branches.split('\n')]
        return []
    
    def checkout_branch(self, branch_name):
        """Checkout to a specific branch"""
        return self._run_git_command(f"git checkout {branch_name}", capture_output=False)
    
    def create_temp_branch(self, base_branch, temp_branch_name):
        """Create a temporary branch from the base branch"""
        self.checkout_branch(base_branch)
        return self._run_git_command(f"git checkout -b {temp_branch_name}", capture_output=False)
    
    def merge_branch(self, branch_name):
        """Merge a branch into the current branch"""
        return self._run_git_command(f"git merge --no-commit --no-ff {branch_name}")
    
    def abort_merge(self):
        """Abort the current merge operation"""
        return self._run_git_command("git merge --abort", capture_output=False)
    
    def get_merge_conflicts(self):
        """Get a list of files with merge conflicts"""
        status = self._run_git_command("git status --porcelain")
        if not status:
            return []
        
        conflict_files = []
        for line in status.split('\n'):
            if line.startswith('UU '):
                conflict_files.append(line[3:])
        return conflict_files
    
    def get_file_content(self, file_path):
        """Get the content of a file"""
        try:
            with open(os.path.join(self.repo_path, file_path), 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    def write_file_content(self, file_path, content):
        """Write content to a file"""
        try:
            with open(os.path.join(self.repo_path, file_path), 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")
            return False
    
    def add_file(self, file_path):
        """Add a file to git staging"""
        return self._run_git_command(f"git add {file_path}", capture_output=False)
    
    def commit_changes(self, message):
        """Commit changes with a message"""
        return self._run_git_command(f'git commit -m "{message}"', capture_output=False)
    
    def resolve_conflict_with_ai(self, file_path, file_content):
        """Use Gemini AI to resolve merge conflicts in a file"""
        if not self.gemini_api_key:
            print("Gemini API key not provided. Cannot use AI to resolve conflicts.")
            return None
        
        prompt = f"""
        I have a merge conflict in a Git file. Please help me resolve it by analyzing the conflict markers and providing a clean, resolved version.
        
        Here's the file with conflicts:
        
        ```
        {file_content}
        ```
        
        Please provide ONLY the resolved content without any explanations or conflict markers (<<<<<<< HEAD, =======, >>>>>>> branch).
        Make sure to preserve the functionality from both versions when possible.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error getting response from Gemini: {e}")
            return None
    
    def extract_conflict_sections(self, content):
        """Extract the conflicting sections from the file content"""
        conflicts = []
        lines = content.split('\n')
        in_conflict = False
        current_conflict = {'ours': [], 'theirs': [], 'start_line': 0, 'end_line': 0}
        current_section = 'ours'
        
        for i, line in enumerate(lines):
            if line.startswith('<<<<<<<'):
                in_conflict = True
                current_conflict = {'ours': [], 'theirs': [], 'start_line': i, 'end_line': 0}
                current_section = 'ours'
            elif in_conflict and line.startswith('======='):
                current_section = 'theirs'
            elif in_conflict and line.startswith('>>>>>>>'):
                in_conflict = False
                current_conflict['end_line'] = i
                conflicts.append(current_conflict)
            elif in_conflict:
                current_conflict[current_section].append(line)
        
        return conflicts
    
    def resolve_conflict_manually(self, file_path, file_content):
        """Manually resolve conflicts by showing both versions and letting the user choose"""
        conflicts = self.extract_conflict_sections(file_content)
        if not conflicts:
            print(f"No conflict markers found in {file_path}")
            return file_content
        
        resolved_lines = file_content.split('\n')
        offset = 0  # Offset to account for removed conflict markers
        
        for conflict in conflicts:
            print(f"\nConflict in {file_path}:")
            print("\nOUR version (current branch):")
            print('\n'.join(conflict['ours']))
            print("\nTHEIR version (branch being merged):")
            print('\n'.join(conflict['theirs']))
            
            choice = input("\nChoose resolution:\n1. Keep our version\n2. Keep their version\n3. Keep both versions\n4. Enter custom resolution\nChoice (1/2/3/4): ")
            
            # Calculate the number of lines in the conflict section including markers
            conflict_length = conflict['end_line'] - conflict['start_line'] + 1
            
            # Prepare the replacement content based on user choice
            if choice == '1':
                replacement = conflict['ours']
            elif choice == '2':
                replacement = conflict['theirs']
            elif choice == '3':
                replacement = conflict['ours'] + conflict['theirs']
            elif choice == '4':
                print("Enter your custom resolution (end with a line containing only 'END'):")
                custom_lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    custom_lines.append(line)
                replacement = custom_lines
            else:
                print("Invalid choice. Keeping both versions.")
                replacement = conflict['ours'] + conflict['theirs']
            
            # Replace the conflict section in the resolved_lines
            resolved_lines[conflict['start_line'] - offset:conflict['end_line'] + 1 - offset] = replacement
            
            # Update the offset
            offset += conflict_length - len(replacement)
        
        return '\n'.join(resolved_lines)
    
    def multi_branch_merge(self, branches, base_branch=None, use_ai=False):
        """Merge multiple branches together and resolve conflicts"""
        if not branches or len(branches) < 2:
            print("Please provide at least two branches to merge.")
            return False
        
        # If no base branch is specified, use the current branch
        if not base_branch:
            base_branch = self.get_current_branch()
            if not base_branch:
                print("Failed to determine the current branch.")
                return False
        
        print(f"Base branch: {base_branch}")
        print(f"Branches to merge: {', '.join(branches)}")
        
        # Create a temporary branch for the merge
        temp_branch = f"temp_merge_{os.getpid()}"
        if not self.create_temp_branch(base_branch, temp_branch):
            print(f"Failed to create temporary branch {temp_branch}.")
            return False
        
        print(f"Created temporary branch: {temp_branch}")
        
        merge_results = {}
        success = True
        
        # Try to merge each branch
        for branch in branches:
            if branch == base_branch or branch == temp_branch:
                continue
                
            print(f"\nMerging branch: {branch}")
            merge_result = self.merge_branch(branch)
            
            if merge_result is None:  # Merge conflict
                conflict_files = self.get_merge_conflicts()
                if conflict_files:
                    print(f"Conflicts detected in {len(conflict_files)} files:")
                    for file_path in conflict_files:
                        print(f"  - {file_path}")
                        
                    # Resolve conflicts
                    for file_path in conflict_files:
                        file_content = self.get_file_content(file_path)
                        if file_content:
                            if use_ai and self.gemini_api_key:
                                print(f"Using AI to resolve conflicts in {file_path}...")
                                resolved_content = self.resolve_conflict_with_ai(file_path, file_content)
                                if resolved_content:
                                    print(f"AI successfully resolved conflicts in {file_path}")
                                else:
                                    print(f"AI failed to resolve conflicts. Falling back to manual resolution.")
                                    resolved_content = self.resolve_conflict_manually(file_path, file_content)
                            else:
                                resolved_content = self.resolve_conflict_manually(file_path, file_content)
                            
                            if resolved_content and self.write_file_content(file_path, resolved_content):
                                self.add_file(file_path)
                                print(f"Resolved conflicts in {file_path}")
                            else:
                                print(f"Failed to resolve conflicts in {file_path}")
                                success = False
                    
                    # Commit the resolved conflicts
                    if success:
                        self.commit_changes(f"Merge branch '{branch}' with resolved conflicts")
                        merge_results[branch] = "Merged with resolved conflicts"
                    else:
                        self.abort_merge()
                        merge_results[branch] = "Failed to resolve conflicts"
                else:
                    print("Unexpected error during merge.")
                    self.abort_merge()
                    merge_results[branch] = "Failed to merge"
                    success = False
            else:
                # Successful merge without conflicts
                self.commit_changes(f"Merge branch '{branch}' without conflicts")
                merge_results[branch] = "Merged successfully without conflicts"
        
        # Print merge summary
        print("\nMerge Summary:")
        for branch, result in merge_results.items():
            print(f"{branch}: {result}")
        
        if success:
            print(f"\nAll branches successfully merged into {temp_branch}.")
            print(f"You can now checkout to {temp_branch} to review the changes.")
            print(f"If satisfied, you can merge {temp_branch} back to {base_branch} with:")
            print(f"  git checkout {base_branch}")
            print(f"  git merge {temp_branch}")
            print(f"  git branch -d {temp_branch}")
        else:
            print(f"\nMerge process completed with some failures.")
            print(f"You may want to delete the temporary branch with: git branch -D {temp_branch}")
        
        return success

def main():
    parser = argparse.ArgumentParser(description='Git Helper - A tool to help with Git operations')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Multi-branch merge command
    merge_parser = subparsers.add_parser('merge-multi', help='Merge multiple branches')
    merge_parser.add_argument('branches', nargs='+', help='Branches to merge')
    merge_parser.add_argument('--base', '-b', help='Base branch to merge into (default: current branch)')
    merge_parser.add_argument('--ai', action='store_true', help='Use AI to resolve conflicts')
    
    args = parser.parse_args()
    
    if args.command == 'merge-multi':
        # Try to load API keys from config
        api_keys = load_api_keys()
        gemini_key = None
        
        if api_keys and 'GEMINI_API_KEY' in api_keys:
            gemini_key = api_keys['GEMINI_API_KEY']
        elif args.ai:
            gemini_key = input("Enter your Gemini API Key: ").strip()
        
        git_helper = GitHelper(gemini_api_key=gemini_key)
        git_helper.multi_branch_merge(args.branches, args.base, args.ai)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()