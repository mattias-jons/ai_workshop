import util_tools
import local_model

# Public








tools = {
    "get_current_weather": util_tools.get_current_weather,
}

tool_calls = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get the weather for, e.g. San Francisco, CA"
                },
                "format": {
                    "type": "string",
                    "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
                    "enum": ["celsius", "fahrenheit"]
            }
            },
            "required": ["location", "format"]
        }
    },
]

# Available models: llama3.2, qwen3:30b, gpt-oss:20b, deepseek-r1:8b, deepseek-r1:32b, mistral
payload = {
  "model": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather today in Paris?"
    }
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
              "description": "The location to get the weather for, e.g. San Francisco, CA"
            },
            "format": {
              "type": "string",
              "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["location", "format"]
        }
      }
    }
  ]
}

def main():
    response = local_model.call_model(payload)
    print(response.json())
    # print(response.json()['response'])

if __name__ == "__main__":
    main()