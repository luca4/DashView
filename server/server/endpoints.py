from loguru import logger

from server.devices import heater
from server.trash_manager import trash_manager

from server import  sio


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
    logger.debug(f"Received event 'sendTrash'")
    try:
        trashData = trash_manager.get_trash_data()
        trashData["result"] = "OK"
        return trashData
    except:
        return {"result": "FAIL"}

#@fastapi_app.get('/heater/on/{minutes}')
#async def heater_on_endpoint(minutes: int):
#    heater.turn_on(int(minutes))
#    return "OK"
#
#
#@fastapi_app.get('/heater/off')
#async def heater_off_endpoint():
#    heater.turn_off()
#    return "OK"
#
#
#@fastapi_app.get('/smartplug/on/{minutes}')
#def smartplug_on_endpoint(minutes: int):
#    smartplug.turn_on(minutes)
#    return "OK"
#
#@fastapi_app.get('/smartplug/off')
#def smartplug_off_endpoint():
#    smartplug.turn_off()
#    return "OK"




# @sio.event
# def connect(sid, environ):
#     print("connect ", sid)


# @sio.event
# def disconnect(sid):
#     print('disconnect ', sid)

