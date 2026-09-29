from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a basic mathematical expression.

    Examples: 2+2, 10*5, 100/4, (15-7)*3.
    """
    allowed = set("0123456789+-*/().% ")
    if not expression or any(ch not in allowed for ch in expression):
        return "Invalid expression. Use numbers and + - * / % ( )."

    try:
        # Restricted namespace; this is only intended for basic arithmetic.
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as exc:
        return f"Could not calculate expression: {exc}"
