from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, FunctionMessage, AIMessage
from langchain import PromptTemplate

function_descriptions = [
    {
        "name": "add_contact",
        "description": "Adds a contact to a specific email list",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The email address of the contact"
                },
                "list": {
                    "type": "string",
                    "description": "The email list to add the contact to"
                }
            },
            "required": ["email", "list"]
        }
    },
    {
        "name": "create_list",
        "description": "Creates a new email list",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the list"
                }
            },
            "required": ["name"]
        }
    },
    {
        "name": "send_email",
        "description": "Sends an email to all contacts in a list",
        "parameters": {
            "type": "object",
            "properties": {
                "list": {
                    "type": "string",
                    "description": "The email list to send the email to"
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email"
                },
                "body": {
                    "type": "string",
                    "description": "The body of the email"
                }
            },
            "required": ["list", "subject", "body"]
        }
    }
]

template = """/
Use the provided functions the carry out the following requests
and respond with short summary of what you did

Requests: {requests}
"""


def add_contact(email, list):
    return f"Added {email} to {list}"


def create_list(name):
    return f"Created list {name}"


def send_email(list, subject, body):
    return f"Sent email to {list} with subject {subject} and body {body}"


def main():
    load_dotenv()

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state["messages"] = []

    # Initialize OpenAI API
    llm = ChatOpenAI(model="gpt-4-0613")

    # Set page title
    st.write("# OpenAI Functions Demo")

    # Create status box
    status = st.empty()

    # Create form
    form = st.form('requests', clear_on_submit=True)
    requests = form.text_area("What is your request?")
    submitted = form.form_submit_button('Go')

    # Create results box
    results = st.empty()

    # Process form
    if submitted:
        tasksCompleted = False

        status = status.info("Processing request...")
        prompt = PromptTemplate.from_template(template)
        content = prompt.format(requests=requests)

        st.session_state["messages"].append(HumanMessage(content=content))

        response = llm.predict_messages(
            st.session_state.messages,
            functions=function_descriptions
        )

        tasksCompleted = response.additional_kwargs == {}

        while not tasksCompleted:

            st.session_state["messages"].append(AIMessage(
                content=response.content,
                additional_kwargs=response.additional_kwargs))

            func = response.additional_kwargs['function_call']['name']
            result = ""

            if func == "add_contact":
                result = add_contact(
                    **eval(response.additional_kwargs['function_call']['arguments']))
            elif func == "create_list":
                result = create_list(
                    **eval(response.additional_kwargs['function_call']['arguments']))
            elif func == "send_email":
                result = send_email(
                    **eval(response.additional_kwargs['function_call']['arguments']))
            print(result)

            st.session_state["messages"].append(
                FunctionMessage(
                    content=result,
                    name=response.additional_kwargs['function_call']['name'])
            )

            response = llm.predict_messages(
                st.session_state.messages,
                functions=function_descriptions
            )

            tasksCompleted = response.additional_kwargs == {}

        results.write(response.content)
        status = status.success("Tasks completed")


if __name__ == '__main__':
    main()
