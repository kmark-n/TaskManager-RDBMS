import asyncio
from typing import Dict, Any, List

class EventEmitter:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        # Keep track of active queues (subscribers)
        self.subscribers: List[asyncio.Queue] = []

    def subscribe(self) -> asyncio.Queue:
        """Creates a new queue for a subscriber (like a WebSocket)."""
        q = asyncio.Queue()
        self.subscribers.append(q)
        return q

    def unsubscribe(self, q: asyncio.Queue):
        """Removes the queue when the subscriber disconnects."""
        if q in self.subscribers:
            self.subscribers.remove(q)

    def emit(self, event_type: str, payload: Dict[str, Any]):
        event = {
            "type": event_type,
            "payload": payload
        }
        self.events.append(event)
        print("[EVENT]", event)

        # PUSH the event to all active subscribers (WebSockets)
        for q in self.subscribers:
            q.put_nowait(event)

    def drain(self):
        evts = self.events[:]
        self.events.clear()
        return evts
