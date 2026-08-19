import pandas as pd
from metrics.metrics import Metrics

class MetricsHistory:

    def __init__(self, metrics):

        self.metrics = metrics

        self.time = []

        self.waiting = []
        self.ready = []
        self.assigned = []
        self.picked = []
        self.delivered = []

        self.busy_riders = []
        self.available_riders = []  
    
    def record(self, current_time, city):

        snapshot = self.metrics.get_snapshot(city)

        self.time.append(current_time)

        self.waiting.append(snapshot["waiting"])
        self.ready.append(snapshot["ready"])
        self.assigned.append(snapshot["assigned"])
        self.picked.append(snapshot["picked"])
        self.delivered.append(snapshot["delivered"])

        self.available_riders.append(snapshot["available"])
        self.busy_riders.append(snapshot["busy"])

    def to_dataframe(self):
        return pd.DataFrame({
            "time": self.time,
            "waiting": self.waiting,
            "ready": self.ready,
            "assigned": self.assigned,
            "picked": self.picked,
            "delivered": self.delivered,
            "busy_riders": self.busy_riders,
            "available_riders": self.available_riders,
        })