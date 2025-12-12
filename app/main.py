from fastapi import FastAPI
# Импортируем роутеры из соответствующих модулей
from app.api.v1.auth import router as auth_router
from app.api.v1.flights import router as flights_router
from app.api.v1.bookings import router as bookings_router
from app.api.v1.payments import router as payments_router
from app.api.v1.notification import router as notifications_router
from app.api.v1.cache_availability import router as cache_availability_router
from app.api.v1.system import router as system_router
from app.api.v1.admin import router as admin_router

app = FastAPI(
    title="Flight Booking Platform",
    version="0.1.0",
    description="Backend API for flight booking platform application",
)


@app.get("/health", tags=["tech"])
def health_check():
    return {"status": "ok"}


# Подключаем роутеры
app.include_router(auth_router, prefix="/api/v1")
app.include_router(flights_router)
app.include_router(bookings_router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(payments_router)
app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(cache_availability_router)
app.include_router(system_router)
app.include_router(admin_router)




