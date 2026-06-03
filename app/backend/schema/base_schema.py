from pydantic import BaseModel, Field

# 공통 BaseSchema - Java @ToString 역할
class BaseSchema(BaseModel):
    def __str__(self):
        return str(self.model_dump())
# 공통 스키마 - 페이징 처리 기본값 적용.
class PaginationRequest(BaseModel):
    page: int = Field(1, ge=1, description="페이지 번호")
    size: int = Field(5, ge=1, le=5, description="페이지당 항목 수")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PaginationResponse(BaseModel):
    total: int
    page: int
    size: int