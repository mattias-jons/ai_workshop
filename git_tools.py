from github import Github
from git import Repo
import os

USERNAME = "mattias-jons"
REPO = "ai_workshop"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def git_pull():
    # Pull repo
    g = Github("GITHUB_TOKEN")
    repo = g.get_repo(f"{USERNAME}/{REPO}")
    return repo


def git_get_issues(repo):
    # Get issues
    issues = repo.get_issues(state="open")
    for issue in issues:
        print(issue.title, issue.number)
    return issues


def git_choose_issue(repo):
    # Choose issue to fix
    issue_number = input("Enter the issue number to solve: ")
    selected_issue = repo.get_issue(number=int(issue_number))
    return selected_issue


def git_clone_repo():
    # Clone repo
    repo_url = f"https://github.com/{USERNAME}/{REPO}.git"
    local_path = "./repo"
    repo = Repo.clone_from(repo_url, local_path)
    return repo


def git_create_branch(repo, issue_number):
    # Create new branch
    issue_branch = f"issue-{issue_number}"
    repo.git.checkout("HEAD", b=issue_branch)


def git_commit(repo, issue_number, selected_issue, issue_branch):
    repo.git.add(A=True)
    repo.index.commit(f"Fixes #{issue_number}: {selected_issue.title}")
    origin = repo.remote(name="origin")
    origin.push(refspec=f"{issue_branch}:{issue_branch}")


def git_create_pull_request(g, issue_number, issue_branch):
    repo = g.get_repo(f"{USERNAME}/{REPO}")
    pr = repo.create_pull(
        title=f"Fixes #{issue_number}",
        body="This PR addresses the issue as described.",
        head=issue_branch,
        base="main",
    )
    return pr
