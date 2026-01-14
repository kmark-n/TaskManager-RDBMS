from typing import Dict, Any, List

class eventEmitter:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def emit(self, event_type: str, payload: Dict[str, Any]):
        event = {
            "type": event_type,
            "payload": payload
        }
        self.events.append(event)
        print("[EVENT]", event)

    def drain(self):
        evts = self.events[:]
        self.events.clear()
        return evts
