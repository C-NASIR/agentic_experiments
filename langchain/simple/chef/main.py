import sys
import base64
from langchain.agents import create_agent 
from langchain.messages import HumanMessage
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from tavily import TavilyClient
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
tavily_client = TavilyClient()

system_prompt = """
 # About you as AI assistant 
 You are an AI chef assistant that helps people decide what food to make based on what they have in their refrigerator. 
 
 # To work successfully you need this things 
 - a picture of their refrigerator, so you can see what they have.

 # Process you follow to help them
 1 - You take the provided image and get all the ingredients 
 2 - You have access to a tool that can search the internet. Use that tool to find recipes that can be made with the provided ingredients 
 3 - you provide the recommendation to the user 
 4 - you answer follow up questions 

"""

@tool
def web_search(query):
    """ Search the web for information """
    return tavily_client.search(query)

agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    checkpointer=InMemorySaver(),
    system_prompt=system_prompt)

def encode_image(image_path):
    return base64.b64encode(image_path.read_bytes()).decode('utf-8')

def handle_input(user_input):
    image_data = None 
    text_query = []

    for word in user_input.split():
        clean_word = word.strip("'").strip('"')
        path = Path(clean_word).expanduser().resolve()

        if path.suffix.lower() in ['.jpg', '.jpeg', '.png'] and path.exists():
            image_data = encode_image(path)
        else:
            text_query.append(clean_word)
    
    final_text = " ".join(text_query).strip()
    return image_data, final_text



Intro = """
    ========= Welcome ========= 

I am a helpful AI chef assissant that can help you find what to eat. 
- Give me a path to a photo of your refrigerator. 
- You can provide full path or just image name if its in the current directory.
- type: "exit" to quit 
"""

def agent_loop():
    first_run = True
    image_received = False

    while True: 
        if first_run:
            print(Intro)
            first_run = False

        user_input = input("> ")
        img_b64, text = handle_input(user_input)

        if text and text.lower() == "exit": break

        question_content = []

        if text:
            question_content.append({ "type": "text", "text": text})
        if img_b64:
            question_content.append({"type": "image", "base64": img_b64, "mime_type": "image/png"})
            image_received = True
        elif not image_received:
            img_b64, _ = handle_input(
                input("Please enter picture of ingredients you have? \n"))

            if not img_b64:
                print("You did not provide valid image \n")
                continue

            question_content.append({"type": "image", "base64": img_b64, "mime_type": "image/png"})
            image_received = True
        
        question = HumanMessage(content=question_content)

        response = agent.invoke(
            {"messages": [question]},
            config={"configurable": {"thread_id": "1"}})


        print()
        print(response['messages'][-1].content)
        print()

    
    print("Goodbye")
        
    

def main():
    agent_loop()


if __name__ == "__main__":
    main()