from typing import Generic, TypeVar, Optional

T = TypeVar('T')  # Generic type variable

class Result(Generic[T]):
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error

    @classmethod
    def ok(cls, data: T) -> "Result[T]":
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> "Result[T]":
        return cls(success=False, error=error)

    def is_success(self) -> bool:
        return self.success