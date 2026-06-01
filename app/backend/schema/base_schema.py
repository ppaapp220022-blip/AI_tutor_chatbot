from pydantic import BaseModel


# 공통 BaseSchema - Java @ToString 역할
class BaseSchema(BaseModel):
    def __str__(self):
        return str(self.model_dump())
