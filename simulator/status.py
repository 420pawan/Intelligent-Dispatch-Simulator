from enum import Enum


class OrderStatus(Enum):
    WAITING = "Waiting"
    READY = "Ready"
    ASSIGNED = "Assigned"
    PICKED_UP = "Picked Up"
    DELIVERED = "Delivered"


class RiderStatus(Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"


class TripStage(Enum):
    TO_RESTAURANT = "To Restaurant"
    TO_CUSTOMER = "To Customer"