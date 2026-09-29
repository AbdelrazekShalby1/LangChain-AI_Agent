from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Return mock weather information for a city.

    Replace this implementation with a real weather API in production.
    """
    return f"The current demo weather in {city} is sunny, 25°C."
