import asyncio
import time
from datetime import date
import json
from loguru import logger
import requests
import schedule
import threading


class TrashManager:

    def __init__(self):
        self.data = {}  # date -> string_array
        #self.update_data()

    # parse data from trash site and update dictionary
    def update_data(self):
        logger.debug("TrashManager - Gathering data from site")
        today_date = date.today()
        today_year = today_date.year
        today_month = today_date.month

        address = f'http://www.convenzionerifiutisesto.it/RaccolteDomicilio/LoadCalendarioMensile?comuneId=18&year={today_year}&month={today_month}'
        json_data = json.loads(requests.get(address).content)

        days = json_data['Giorni']

        days_counter = 1
        monthly_trash = {}
        for day in days:
            for x in day['Eventi']:
                if days_counter not in monthly_trash:
                    monthly_trash[days_counter] = [x["Testo"]]
                else:
                    monthly_trash[days_counter].append(x["Testo"])
            days_counter += 1

        self.data = monthly_trash

    # return today's and tomorrow's trash from data gathered from site
    def get_trash_data(self):
        actual_date = date.today()
        today_number = actual_date.day

        today_trash = self.data.get(today_number, "--")
        tomorrow_trash = self.data.get(today_number+1, "--")

        return {'today': today_trash, 'tomorrow': tomorrow_trash}
    
    def _emit_trash_data(self):
        from . import sio

        async def emit(event, msg):
            await sio.emit(event, msg)
            logger.debug(f"TrashManager - emitting trash data. Event: {event}, Data: {str(msg)}")

        data = self.get_trash_data()
        asyncio.run(emit("trashData", data))


    def send_trash(self):
        trash_manager.update_data()
        self._emit_trash_data()


    def schedule_trash_sending(self):
        schedule.every().day.at("00:01").do(self.send_trash)

        def run_continuously():
            while True:
                schedule.run_pending()
                time.sleep(20)

        threading.Thread(target=run_continuously, daemon=True).start()


trash_manager = TrashManager()



