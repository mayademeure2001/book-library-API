from fastapi import Query

class Pagination:
    def __init__(self, maximum_limit: int = 100):
        self.maximum_limit = maximum_limit

    async def __call__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(25, ge=1, description="Number of records to return"),
    ) -> tuple[int, int]:
        capped_limit = min(self.maximum_limit, limit)
        return (skip, capped_limit)

pagination = Pagination(maximum_limit=50)