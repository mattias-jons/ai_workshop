from github import Github
from git import Repo
import os
import sys

USERNAME = "mattias-jons"
REPO_NAME = "ai_workshop"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    print("Missing GITHUB_TOKEN")
    sys.exit(1)


def git_pull():
    # Pull repo
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(f"{USERNAME}/{REPO_NAME}")
    return g, repo


def git_get_issues(repo):
    issues = repo.get_issues(state="open")  # , assignee="AI")
    return issues


def git_get_issue(repo, issue_number):
    try:
        selected_issue = repo.get_issue(number=int(issue_number))
        return selected_issue
    except Exception as e:
        print(f"Error retrieving issue: {e}")


def git_clone_repo():
    repo_url = (
        f"https://x-access-token:{GITHUB_TOKEN}@github.com/{USERNAME}/{REPO_NAME}.git"
    )
    local_path = "./repo"
    if os.path.exists(local_path):
        repo = Repo(local_path)
    else:
        repo = Repo.clone_from(repo_url, local_path)

    print(f"Cloned to: {repo.working_tree_dir}")
    print(f"Files: {os.listdir(repo.working_tree_dir)}")
    return repo


def git_create_branch(repo, issue_number):
    issue_branch = f"issue-{issue_number}"
    repo.git.checkout("HEAD", b=issue_branch)

    print(f"Current branch: {repo.active_branch.name}")
    assert repo.active_branch.name == f"issue-{issue_number}"

    return issue_branch


def git_commit(repo, issue_number, selected_issue, issue_branch):
    repo.git.add(A=True)
    repo.index.commit(f"Fixes #{issue_number}: {selected_issue.title}")
    origin = repo.remote(name="origin")
    origin.push(refspec=f"{issue_branch}:{issue_branch}")


def git_create_pull_request(g, issue_number, issue_branch):
    repo = g.get_repo(f"{USERNAME}/{REPO_NAME}")
    pr = repo.create_pull(
        title=f"Fixes #{issue_number}",
        body="This PR addresses the issue as described.",
        head=issue_branch,
        base="main",
    )
    print(f"Pull request created: {pr.html_url}")
    return pr
