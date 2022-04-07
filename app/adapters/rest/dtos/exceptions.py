from pydantic import ValidationError
from app.business_logic.exceptions import BusinessLogicException, ServerException
import inspect

Exception_Error_Code_Mapping = {
    # Uncategorized Exceptions
    Exception: 3000,
    ValueError: 3001,
    ValidationError: 3002,

    # Business Logic Exceptions
    BusinessLogicException: 4100,

    # Server Exceptions
    ServerException: 5000,
}


def get_error_code_for_exception(exception: Exception) -> int:
    if type(exception) == object:
        return -1

    if type(exception) in Exception_Error_Code_Mapping:
        return Exception_Error_Code_Mapping[type(exception)]

    next_class_in_mro = inspect.getmro(type(exception))[1]
    return get_error_code_for_exception(next_class_in_mro())
