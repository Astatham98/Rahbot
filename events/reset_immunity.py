from events.base_event import BaseEvent

from datetime import datetime
from database import Database


# Your friendly example event
# You can name this class as you like, but make sure to set BaseEvent
# as the parent class
class ResetImmunityEvent(BaseEvent):
    def __init__(self):
        interval_minutes = 60  # Set the interval for this event
        self.db = Database()
        super().__init__(interval_minutes)

    # Override the run() method
    # It will be called once every {interval_minutes} minutes
    async def run(self, client):
        now = datetime.now()

        if now.hour == 5:
            self.db.reset_immunity()
