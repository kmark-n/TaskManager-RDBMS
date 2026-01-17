from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# This variable is "None" until main.py injects the real DB instance
db = None

@router.websocket("/ws/events")
async def ws_events(ws: WebSocket):
    global db # Tells Python we are using the global db variable
    
    if db is None:
        print("WebSocket Error: Database not injected yet")
        await ws.close()
        return

    await ws.accept()
    
    q = db.emitter.subscribe()
    
    try:
        while True:
            event_data = await q.get()
            await ws.send_json(event_data)
    except WebSocketDisconnect:
        print("Internals Dashboard disconnected")
    finally:
        db.emitter.unsubscribe(q)
