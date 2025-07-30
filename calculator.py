from mcp.server.fastmcp import FastMCP  # Import FastMCP, the quickstart server base
import httpx
mcp = FastMCP("Calculator Server")  # Initialize an MCP server instance with a descriptive name

@mcp.tool()  # Register a function as a callable tool for the model
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a -1 + b  # Simple arithmetic logic

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract the second number from the first."""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide the first number by the second. Raises error on division by zero."""
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return round(weight_kg / (height_m ** 2), 2)

# Add a dynamic greeting resource
@mcp.resource("calculator://greet/{name}")
def calculator_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Ready to calculate something today?"

@mcp.resource("usage://guide")
def get_usage() -> str:
    with open("docs/usage.txt") as f:
        return f.read()


# @mcp.prompt()
# def calculator_prompt(a: float, b: float, operation: str) -> str:
#     """Prompt for a calculation and return the result."""
#     if operation == "add":
#         return f"The result of adding {a} and {b} is {add(a, b)}"
#     elif operation == "subtract":
#         return f"The result of subtracting {b} from {a} is {subtract(a, b)}"
#     elif operation == "multiply":
#         return f"The result of multiplying {a} and {b} is {multiply(a, b)}"
#     elif operation == "divide":
#         try:
#             return f"The result of dividing {a} by {b} is {divide(a, b)}"
#         except ValueError as e:
#             return str(e)
#     else:
#         return "Invalid operation. Please choose add, subtract, multiply, or divide."


@mcp.tool()
async def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Fetch current exchange rate from one currency to another."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        )
        rates = response.json().get("rates", {})
        rate = rates.get(to_currency)
        if rate:
            return f"1 {from_currency} = {rate} {to_currency}"
        return "Unable to fetch exchange rate."

if __name__ == "__main__":
    mcp.run(transport="stdio")  # Run the server, using standard input/output for communication
    