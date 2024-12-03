from .system_callbacks import system_router
from .check_predictions import predictions_router
from .subscribe_to_bonds import subscribe_router
from .single_bond import choose_bond_router

callbacks_routers = [
    predictions_router,
    system_router,
    subscribe_router,
    choose_bond_router
]