from .start_hd import start_router
from .other_hd import other_router
from .devices_hd import devices_router

def register_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(other_router)
    dp.include_router(devices_router)