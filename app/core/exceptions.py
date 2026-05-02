class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class EntityNotFoundException(CustomException):
    def __init__(self, entity_name: str):
        super().__init__(f"{entity_name} not found", status_code=404)
