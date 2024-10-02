import uvicorn

from server.devices import temp_sensor
from loguru import logger

from server.trash_manager import trash_manager



temp_sensor.start_sending_ambient_data()

logger.debug("Start")


# Manage trash sending
trash_manager.update_data()
trash_manager.schedule_trash_sending()


if __name__ == "__main__":
    uvicorn.run("endpoints:app", port=5000, log_level="info")

