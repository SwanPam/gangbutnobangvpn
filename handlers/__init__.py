from .start import start_router
from .other_handlers import other_router
from .devices import devices_router

def register_handlers(dp):
    dp.include_router(start_router)
    dp.include_router(other_router)
    dp.include_router(devices_router)