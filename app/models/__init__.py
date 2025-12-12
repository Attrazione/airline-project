from app.core.db import Base

from app.models.user import User
from app.models.flight import Flight
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.notification import Notification

__all__ = [
    "Base",
    "User",
    "Flight",
    "Booking",
    "Payment",
    "Notification",
]
