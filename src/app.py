
import asyncio

from core.service.weather import WeatherAPI

class App:
    def __init__(self):
        self.weather = WeatherAPI()
    
    async def main_loop(self, interval_seconds: int = 3600):
        while True:
            await self.weather.get_weather()
            await asyncio.sleep(interval_seconds)
        
if __name__ == "__main__":
    app = App()
    asyncio.run(app.main_loop())
