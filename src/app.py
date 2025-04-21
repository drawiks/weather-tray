
import asyncio

from services.weather import WeatherService

from config import API_KEY, CITY, LOG_PATH

class App:
    def __init__(self):
        self.weather = WeatherService(api_key=API_KEY, city=CITY, log_path=LOG_PATH)
    
    async def main_loop(self, interval_seconds: int = 3600):
        while True:
            await self.weather.get_weather()
            await asyncio.sleep(interval_seconds)
        
if __name__ == "__main__":
    app = App()
    asyncio.run(app.main_loop())
