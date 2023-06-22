import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import ChatOpenAI

app = FastAPI()

# Enable CORS
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MessageInput(BaseModel):
    message: str
    character: Dict[str, str]  # New field


OPENAI_API_KEY = "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"


@app.post("/chat")
async def chat(message_input: MessageInput):
    # Extract character details
    character = message_input.character

    # Create a wrapper for GPT model with API key passed directly
    chat = ChatOpenAI(model_name="gpt-3.5-turbo",
                      temperature=0.3, openai_api_key=OPENAI_API_KEY)

    # Construct the SystemMessage with the character details
    system_message = f"You are a helpful human/friend, your name is {character['name']} and you have the personality traits of a {character['ethnicity']}, {character['gender']}, {character['age']} aged, {character['profession']} by profession, single. You express your ethnicity while talking in your accent and language. Keep the conversation casual and friendly and less like a chat bot and dont repeat previous answers, give it a bit human touch. Talk more like a human and less like a bot. Answer every question and try to be a good friend to the user. Just have a casual conversation with the user like their friend, avoid asking things like how can I assist you today."

    # Initialize a list with a SystemMessage
    messages = [SystemMessage(content=system_message)]

    # Add the user's message to the chat history
    messages.append(HumanMessage(content=message_input.message))

    try:
        # Generate chatbot response
        response = chat(messages)

        # Extract the actual response content
        response_content = response.content

        # Return the chatbot response
        return {"message": response_content}

    except Exception as e:
        # Handle any exceptions
        return {"message": f"Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
