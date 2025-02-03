from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import tool
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

class GeoCode(TypedDict):
    lat: float
    lon: float
    city: str
    state:str

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

chat_prompt = ChatPromptTemplate.from_messages([
    HumanMessage(
        content="{city}"
    ),
    SystemMessage(
        content="""You are an AI assistant who is expert in geography and that finds geocode of city name provided by the user. 
        Return only in JSON format with city name and state, latitude and longitude as keys. """
    )
])
@tool
def get_geoCode(city: str) -> GeoCode:
    """Tool that returns the latitude and longitude of a city"""
    print(f"Getting geocode for {city}")
    response = llm.invoke(chat_prompt, {"city": city})
    print(response)
    
    return {"lat": response["latitude"], "lon": response["longitude"], "city": response["city"], "state": response["state"]}

if __name__ == "__main__":
    load_dotenv()
    print(get_geoCode("New York"))