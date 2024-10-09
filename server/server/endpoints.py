from loguru import logger

from server.devices import heater
from server.trash_manager import trash_manager

from . import app, sio, fastapi_app


@sio.on("heaterOn")
def heater_on(sid, data):
    logger.debug(f"Received event 'heaterOn' with data: ", data)
    try:
        heater.turn_on(int(data))
        remaining_minutes = heater.timer.get_remaining_minutes()
        return {"result":"OK", "remainingMinutes":remaining_minutes}
    except:
        return {"result":"FAIL"}

    

@sio.on("heaterOff")
def heater_off(sid):
    logger.debug(f"Received event 'heaterOff'")
    try:
        heater.turn_off()
        return "OK"
    except:
        return "FAIL"


@sio.on("getTrash")
def send_trash(sid):
    logger.debug(f"Received event 'getTrash'")
    try:
        trashData = trash_manager.get_trash_data()
        trashData["result"] = "OK"
        return trashData
    except Exception as ex:
        print(ex)
        return {"result": "FAIL"}
    

@sio.on("updateTrashDb")
def update_trash_db(sid):
    try:
        logger.debug(f"Received event 'updateTrashDb'")
        trash_manager.update_yearly_data()

        trashData = trash_manager.get_trash_data()
        trashData["result"] = "OK"
        return trashData
    except:
        return {"result": "FAIL"}

    
@sio.on("getLastTrashDbUpdateDate")
def get_trash_db_last_update_date(sid):
    logger.debug(f"Received event 'getLastTrashDbUpdateDate'")
    try:
        trashData = trash_manager.get_trash_data()
        trashData["result"] = "OK"
        return trashData
    except:
        return {"result": "FAIL"}


@fastapi_app.get('/status')
def status():
    return "Running..."




# @sio.event
# def connect(sid, environ):
#     print("connect ", sid)


# @sio.event
# def disconnect(sid):
#     print('disconnect ', sid)

