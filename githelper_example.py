#!/usr/bin/env python3
"""
Example script demonstrating how to use the GitHelper class programmatically.
"""

from git_helper import GitHelper

def example_merge_workflow():
    """
    Example workflow for merging multiple branches using GitHelper.
    """
    print("=== GitHelper Example: Merging Multiple Branches ===\n")
    
    # Initialize GitHelper (optionally with Gemini API key)
    gemini_key = input("Enter your Gemini API key (or press Enter to skip AI-assisted conflict resolution): ").strip()
    git_helper = GitHelper(gemini_api_key=gemini_key if gemini_key else None)
    
    # Get current branch
    current_branch = git_helper.get_current_branch()
    print(f"Current branch: {current_branch}")
    
    # Get all branches
    all_branches = git_helper.get_all_branches()
    print("\nAvailable branches:")
    for i, branch in enumerate(all_branches, 1):
        print(f"{i}. {branch}")
    
    # Select branches to merge
    print("\nSelect branches to merge (comma-separated numbers, e.g., 1,3,4):")
    selection = input("> ")
    try:
        selected_indices = [int(idx.strip()) - 1 for idx in selection.split(',')]
        selected_branches = [all_branches[idx] for idx in selected_indices if 0 <= idx < len(all_branches)]
    except (ValueError, IndexError):
        print("Invalid selection. Please enter valid branch numbers.")
        return
    
    if len(selected_branches) < 2:
        print("Please select at least two branches to merge.")
        return
    
    # Select base branch
    print("\nSelect base branch (Enter a number, or press Enter to use current branch):")
    base_selection = input("> ")
    if base_selection:
        try:
            base_idx = int(base_selection.strip()) - 1
            if 0 <= base_idx < len(all_branches):
                base_branch = all_branches[base_idx]
            else:
                print("Invalid selection. Using current branch.")
                base_branch = current_branch
        except ValueError:
            print("Invalid selection. Using current branch.")
            base_branch = current_branch
    else:
        base_branch = current_branch
    
    # Confirm merge operation
    print(f"\nYou are about to merge the following branches into {base_branch}:")
    for branch in selected_branches:
        if branch != base_branch:
            print(f"- {branch}")
    
    confirm = input("\nProceed with merge? (y/n): ")
    if confirm.lower() != 'y':
        print("Merge operation cancelled.")
        return
    
    # Use AI for conflict resolution?
    use_ai = False
    if gemini_key:
        ai_confirm = input("Use AI to resolve conflicts? (y/n): ")
        use_ai = ai_confirm.lower() == 'y'
    
    # Perform the merge
    git_helper.multi_branch_merge(selected_branches, base_branch, use_ai)

if __name__ == "__main__":
    example_merge_workflow()