import os
from typing import TypedDict, Annotated, List

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


# Load Environment Variables

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Define State

class PlannerState(TypedDict):
    messages: Annotated[
        List[HumanMessage | AIMessage],
        "the messages in the conversation"
    ]
    city: str
    interests: List[str]
    itinerary: str


llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="openai/gpt-oss-20b"
)


itinerary_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful travel assistant. "
        "Create a day trip itinerary for {city} based on "
        "the user's interests: {interests}. "
        "Provide a brief, bulleted itinerary."
    ),
    (
        "human",
        "Create an itinerary for my day trip."
    ),
])


def input_city(state: PlannerState) -> PlannerState:

    print("Please enter the city you want to visit for your day trip:")

    user_message = input("Your Input: ")

    return {
        **state,
        "city": user_message,
        "messages": state["messages"] + [
            HumanMessage(content=user_message)
        ]
    }


def input_interest(state: PlannerState) -> PlannerState:

    print(
        f"Please enter your interests for the trip to "
        f"{state['city']}:"
    )

    user_message = input("Your Input: ")

    return {
        **state,
        "interests": [
            interest.strip()
            for interest in user_message.split(",")
        ],
        "messages": state["messages"] + [
            HumanMessage(content=user_message)
        ]
    }


def create_itinerary(state: PlannerState) -> PlannerState:

    print(
        f"Creating an itinerary for {state['city']} "
        f"based on interests: "
        f"{', '.join(state['interests'])}"
    )

    response = llm.invoke(
        itinerary_prompt.format_messages(
            city=state["city"],
            interests=", ".join(state["interests"])
        )
    )

    print("\nFinal Itinerary:")
    print(response.content)

    return {
        **state,
        "messages": state["messages"] + [
            AIMessage(content=response.content)
        ],
        "itinerary": response.content
    }


# Graph

workflow = StateGraph(PlannerState)

workflow.add_node("input_city", input_city)
workflow.add_node("input_interest", input_interest)
workflow.add_node("create_itinerary", create_itinerary)

workflow.set_entry_point("input_city")

workflow.add_edge("input_city", "input_interest")
workflow.add_edge("input_interest", "create_itinerary")
workflow.add_edge("create_itinerary", END)

app = workflow.compile()

# Travel Planner

def travel_planner(user_request: str):
    print(f"Initial Request: {user_request}\n")

    state = {
        "messages": [
            HumanMessage(content=user_request)
        ],
        "city": "",
        "interests": [],
        "itinerary": ""
    }

    for output in app.stream(state):
        pass


if __name__ == "__main__":
    user_request = "I want to plan a day trip"
    travel_planner(user_request)