import asyncio
from inspect import cleandoc
import time
from datetime import date, datetime, timedelta
import json
from loguru import logger
import requests
import schedule
import threading
import pymongo

DB_NAME = "trash_db"

class TrashManager:

    def __init__(self):
        db_client = pymongo.MongoClient("mongoDb", 27017)

        # Get db collection
        trash_db = db_client[DB_NAME]
        self.trash_coll = trash_db["trash"]

    
    def _get_yearly_data_from_site(self):
        logger.debug("TrashManager - Gathering annual data from site")
        today_date = date.today()
        today_year = today_date.year

        # Gather all months data from site
        days = []
        for month in range(1, 13):
            address = f'http://www.convenzionerifiutisesto.it/RaccolteDomicilio/LoadCalendarioMensile?comuneId=18&year={today_year}&month={month}'
            json_data = json.loads(requests.get(address).content)
            days = days + json_data['Giorni']

        # Parse gathered data and pack it into a dictionary
        trash_data = []
        for day in days:
            day_date = datetime.fromtimestamp(int(day["Data"].replace("/Date(","").replace(")/",""))/1000)
            is_festivo = day["Festivo"]
            festivita = day["Festivita"]

            day_trash = []
            for x in day['Eventi']:
                day_trash.append(x["Testo"])

            trash_data.append({
                "date": day_date,
                "festivo": is_festivo,
                "festivita": festivita,
                "trash": day_trash
            })

        return trash_data


    # return today's and tomorrow's trash from db data
    def get_trash_data(self):

        tmp_date = date.today()
        today_date = datetime(tmp_date.year, tmp_date.month, tmp_date.day)
        tomorrow_date = today_date + timedelta(days=1)

        today_trash = self.trash_coll.find_one({"date": today_date})
        tomorrow_trash = self.trash_coll.find_one({"date": tomorrow_date})

        lastDbUpdate = self.trash_coll.find_one({"name": "TrashDbInfo"})

        return {'today': today_trash["trash"], 'tomorrow': tomorrow_trash["trash"], 'lastDbUpdate': lastDbUpdate["lastDataUpdate"].isoformat()}
    

    def _emit_trash_data(self):
        from . import sio

        async def emit(event, msg):
            await sio.emit(event, msg)
            logger.debug(f"TrashManager - emitting trash data. Event: {event}, Data: {str(msg)}")

        data = self.get_trash_data()
        asyncio.run(emit("trashData", data))


    def _send_trash(self):
        self._emit_trash_data()


    def schedule_trash_sending(self):
        schedule.every().day.at("00:01").do(self._send_trash)

        def run_continuously():
            while True:
                schedule.run_pending()
                time.sleep(20)

        threading.Thread(target=run_continuously, daemon=True).start()


    def update_yearly_data(self):
        # Get trash data
        trash_data = self._get_yearly_data_from_site()

        # Reset db data
        self.trash_coll.delete_many({})

        # Insert trash data
        self.trash_coll.insert_many(trash_data)

        self.trash_coll.insert_one({"name": "TrashDbInfo", "lastDataUpdate": datetime.now()})
        

trash_manager = TrashManager()



