
import aiohttp
from datetime import datetime
from plyer import notification

from core.utils.speaker import Speaker
from core.utils.logger import LogManager

from config import API_KEY, CITY, LOG_PATH

class WeatherAPI:
    def __init__(self):
        self.speaker = Speaker()
        self.log = LogManager(log_path=LOG_PATH, level="DEBUG").get_logger()
        
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.params = {
            "q": CITY,
            "appid": API_KEY,
            "units": "metric",
            "lang": "ru"
        }
    
    async def get_weather(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=self.params) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    
                    await self.speaker.speak(f"[{datetime.now().strftime('%H:%M')}] {temp}°C — {desc.capitalize()}")
                    notification.notify(
                        title="Weather-tray",
                        message=f"{temp}°C — {desc.capitalize()}",
                        timeout=3
                    )
                    
                    self.log.info(f"{temp}°C — {desc.capitalize()}")
                    
                else:
                    self.log.error(f"Ошибка: {response.status}")
                    self.log.warning(await response.text())