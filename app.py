import os
import json
import openai
from dotenv import load_dotenv
from tools import tools,available_tools
load_dotenv()
client = openai.AsyncOpenAI(
   base_url=os.getenv("base_url"),
    api_key=os.getenv("api_key")
)
Model="qwen2.5:3b"

async def run_conversation(user_query:str):
  messages = [
    {"role": "system", "content":("You are a helpful assistant. You can use a tool to answer questions using a MySQL database. "
            "You must never show SQL queries to the user. Only return clear, helpful summaries of the results."
            "If no data is found, say so politely. Use the `documents` table with columns: "
            "`document_number`, `title`, `publication_date`, `agency_names`, and `summary`."
        )
    },
  {"role":"user","content":user_query}
  ]
  response= await client.chat.completions.create(
    model=Model,
    messages=messages,
    tools=tools,
    tool_choice="auto",
  )
  response_message = response.choices[0].message
  tool_calls= response_message.tool_calls

  if tool_calls:
    messages.append(response_message)

    for tool_call in tool_calls:
      function_name = tool_call.function.name
      args = json.loads(tool_call.function.arguments)

      if function_name not in available_tools:
        return f"Error: Function '{function_name}' is not available."
      function_response = await available_tools[function_name](**args)
      messages.append(
         {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
      final_response = await client.chat.completions.create(
        model=Model,
            messages=messages,
            )
      return final_response.choices[0].message.content
    else:
        return response_message.content
    
