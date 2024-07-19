import streamlit as st
from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()
import json
from upload import upload_db, delete_db, search_db
import tools

tools = tools.tools

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def run_conversation(user_input):
    messages=user_input
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto",  
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    if tool_calls:
        available_functions = {
        "search_db": search_db,
        "upload_db": upload_db, 
        "delete_db": delete_db, 
        }
        messages.append(response_message)  
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name == "search_db":
                function_response = function_to_call(
                    input=function_args.get("input"),
                )
            elif function_name == "upload_db":
                function_response = function_to_call(
                    name=function_args.get("name"),
                    age=function_args.get("age"),
                    city=function_args.get("city"),
                )
            elif function_name == "delete_db":
                function_response = function_to_call(
                    id=function_args.get("id"),
                )
                
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  
        second_response = client.chat.completions.create(model="gpt-4o-mini",messages= messages,max_tokens=50)
        output=second_response.choices[0].message.content
        return str(output)
    else:
        return str(response_message.content)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

previous_role = None

for msg in st.session_state.messages:
    if isinstance(msg, dict):
        role = msg["role"]
        content = msg["content"]

        if role == "tool" or ("tool_calls" in msg):
            continue

        if role == previous_role:
            continue

        with st.chat_message(role):
            st.write(content)

        previous_role = role


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    msg = run_conversation(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    print(st.session_state.messages)
    st.chat_message("assistant").write(msg)

