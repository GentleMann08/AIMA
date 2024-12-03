from .system_callbacks import system_router
from .check_predictions import predictions_router
from .bonds import bonds_router

callbacks_routers = [
    predictions_router,
    system_router,
    bonds_router
]