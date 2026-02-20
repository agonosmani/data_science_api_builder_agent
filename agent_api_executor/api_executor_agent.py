from dataclasses import dataclass
from typing import Any, Optional
import asyncio

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
import httpx
from typing import Any
from pydantic_ai import RunContext

load_dotenv()


# --------------------
# Output schema
# --------------------

class ApiExecutorOutput(BaseModel):
    response_text: str = Field(description="The response text to the user's request")


# --------------------
# Single agent
# --------------------

api_executor_agent = Agent(
    "openai:gpt-4o",
    output_type=ApiExecutorOutput,
    system_prompt=(
        "You are a API executor agent. You are responsible for executing the API calls and returning the response to the user."
    ),
)


# --------------------
# Tools
# --------------------


# === get_weather ===

@api_executor_agent.tool
async def get_weather(
    ctx: RunContext,
    location: str,
    date: str
) -> Any:
    """get_weather

Endpoint: Get the weather for a specific city and a specific day

Parameters:
location: The location to get the weather for.
date: The date to get the weather for.
"""

    url = f"http://127.0.0.1:8000/mock_api/weather"
    params = {}

    if location is not None:
        params["location"] = location
    if date is not None:
        params["date"] = date

    async with httpx.AsyncClient() as client:
        response = await client.request("GET", url, params=params)

    try:
        return response.json()
    except Exception:
        return response.text


# === stock_operation ===

@api_executor_agent.tool
async def stock_operation(
    ctx: RunContext,
    stock: str,
    operation: str
) -> Any:
    """stock_operation

Endpoint: Do a specific operation on a specific stock

Parameters:
stock: The stock to do the operation on.
operation: The operation to do, eg. buy, sell, short, cover etc.
"""

    url = f"http://127.0.0.1:8000/mock_api/stocks/operation"
    params = {}

    if stock is not None:
        params["stock"] = stock
    if operation is not None:
        params["operation"] = operation

    async with httpx.AsyncClient() as client:
        response = await client.request("POST", url, params=params)

    try:
        return response.json()
    except Exception:
        return response.text




# === sell_item_online ===

@api_executor_agent.tool
async def sell_item_online(
    ctx: RunContext,
    item: str,
    store: str
) -> Any:
    """sell_item_online

Endpoint: Sell a specific item at a specific online store

Parameters:
item: The item to sell.
store: The online store to sell the item at, eg. Amazon, Ebay, Taobao etc.
"""

    url = f"http://127.0.0.1:8000/mock_api/sell_item"
    params = {}

    if item is not None:
        params["item"] = item
    if store is not None:
        params["store"] = store

    async with httpx.AsyncClient() as client:
        response = await client.request("POST", url, params=params)

    try:
        return response.json()
    except Exception:
        return response.text





# === Country API ===

@api_executor_agent.tool
async def get_country_data(
    ctx: RunContext,
    name: str | None = None,
    currency: str | None = None,
    min_gdp: float | None = None,
    max_gdp: float | None = None,
    min_population: float | None = None,
    max_population: float | None = None,
    min_area: float | None = None,
    max_area: float | None = None,
    min_unemployment: float | None = None,
    max_unemployment: float | None = None,
    min_gdp_growth: float | None = None,
    max_gdp_growth: float | None = None
) -> Any:
    """Country API

The Country API provides key geographic, demographic, and economic statistics about every country in the world.

Endpoint: Get country data from given parameters. Returns a list of country statistics that satisfy the parameters.

Parameters:
name: Plain English name, 2-letter ISO-3166 alpha-2, or 3-letter ISO-3166 alpha-3 code of country.
currency: 3-letter currency code of country (e.g. USD).
min_gdp: Minimum gross domestic product (GDP) of country, in US Dollars.
max_gdp: Maximum gross domestic product (GDP) of country, in US Dollars.
min_population: Minimum population of country.
max_population: Maximum population of country.
min_area: Minimum surface area of country in km2.
max_area: Maximum surface area of country in km2.
min_unemployment: Minimum unemployment rate in %.
max_unemployment: Maximum unemployment rate in %.
min_gdp_growth: Minimum GDP growth rate in %.
max_gdp_growth: Maximum GDP growth rate in %.
"""

    url = f"http://127.0.0.1:8000/mock_api/get_country_data"
    params = {}

    if name is not None:
        params["name"] = name
    if currency is not None:
        params["currency"] = currency
    if min_gdp is not None:
        params["min_gdp"] = min_gdp
    if max_gdp is not None:
        params["max_gdp"] = max_gdp
    if min_population is not None:
        params["min_population"] = min_population
    if max_population is not None:
        params["max_population"] = max_population
    if min_area is not None:
        params["min_area"] = min_area
    if max_area is not None:
        params["max_area"] = max_area
    if min_unemployment is not None:
        params["min_unemployment"] = min_unemployment
    if max_unemployment is not None:
        params["max_unemployment"] = max_unemployment
    if min_gdp_growth is not None:
        params["min_gdp_growth"] = min_gdp_growth
    if max_gdp_growth is not None:
        params["max_gdp_growth"] = max_gdp_growth

    async with httpx.AsyncClient() as client:
        response = await client.request("GET", url, params=params)

    try:
        return response.json()
    except Exception:
        return response.text

