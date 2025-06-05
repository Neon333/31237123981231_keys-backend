from . import admin_router


@admin_router.get("/stats")
async def get_stats():
    pass
