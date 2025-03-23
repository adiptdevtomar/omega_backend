from typing import Any, Dict

def format_response(data: Any = None, message: str = "Success", success: bool = True) -> Dict[str, Any]:
    """
    Standardize API responses.
    :param data: The response data (optional).
    :param message: A message describing the response.
    :param success: Indicates if the operation was successful.
    :return: A dictionary with the standardized response format.
    """
    return {
        "success": success,
        "message": message,
        "data": data,
    }
