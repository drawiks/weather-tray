
import aiohttp
from datetime import datetime
from plyer import notification

from utils.speaker import Speaker
from utils.logger import LogManager

class WeatherService:
    def __init__(self, api_key: str, city: str, log_path:str):
        self.speaker = Speaker()
        self.log = LogManager(log_path=log_path, level="DEBUG").get_logger()
        
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.params = {
            "q": city,
            "appid": api_key,
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