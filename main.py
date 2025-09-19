import util_tools
import local_model
import cloud_model
import git_tools
import os
import code_tools
import json

tool_calls = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
                    "enum": ["celsius", "fahrenheit"],
                },
            },
            "required": ["location", "format"],
        },
    },
]


def create_payload(repo, issue):
    # Available models: llama3.2, qwen3:30b, gpt-oss:20b, deepseek-r1:8b, deepseek-r1:32b, mistral
    payload = {
        "model": "llama3.2",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert software engineer helping fix GitHub issues. "
                    "Based on the issue below and the current codebase context, propose a solution or code fix."
                ),
            },
            {
                "role": "user",
                "content": f"Issue Title: {issue.title}\n\nIssue Description:\n{issue.body}",
            },
        ],
        "stream": False,
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather for a location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to get the weather for, e.g. San Francisco, CA",
                            },
                            "format": {
                                "type": "string",
                                "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
                                "enum": ["celsius", "fahrenheit"],
                            },
                        },
                        "required": ["location", "format"],
                    },
                },
            }
        ],
    }

    # Add context from files in repo
    payload = add_code_to_payload(
        payload,
        repo.working_tree_dir,
        rel_path=repo.working_tree_dir.rsplit("/", 1)[-1],
    )

    return payload


def add_code_to_payload(payload, dir_path, rel_path=""):
    for obj_name in os.listdir(dir_path):
        obj_path = os.path.join(dir_path, obj_name)

        if os.path.isdir(obj_path):
            if obj_name == ".git":
                continue
            else:
                new_rel_path = os.path.join(rel_path, obj_name)
                add_code_to_payload(payload, obj_path, rel_path=new_rel_path)

        with open(obj_path, "r") as f:
            py_content = f.read()

        payload["messages"].append(
            {
                "role": "user",
                "content": f"Here is the content of {os.path.join(rel_path, obj_name)}:\n```python\n{py_content}\n```",
            }
        )

    return payload


def main():
    g, repo = git_tools.git_pull()

    issues = git_tools.git_get_issues(repo)
    for issue in issues:
        print(f"{issue.number}: {issue.title} \n   {issue.body}")
    issue_number = input("Enter the issue number to solve: ")

    issue = git_tools.git_get_issue(repo, issue_number)

    local_repo = git_tools.git_clone_repo()
    issue_branch = git_tools.git_create_branch(local_repo, issue_number)

    payload = create_payload(local_repo, issue)

    response = local_model.call_model(payload)
    # response = cloud_model.call_model(payload)

    if response.status_code == 200:
        print(response.json())
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

    # Check if function_call was returned
    if "tool_calls" in response:
        for tool_call in response["tool_calls"]:
            tool_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])
            # result = handle_tool_call(tool_name, arguments)
            # print(f"Tool '{tool_name}' executed with result:\n{result}")


if __name__ == "__main__":
    main()
