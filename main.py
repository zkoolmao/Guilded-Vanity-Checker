import asyncio, aiohttp, json, random
from modules.console import Logger

async def fetch(session, url, headers=None, json_data=None):
    async with session.get(url, headers=headers, json=json_data) as response:
        return await response.json(), response.status, response.headers

async def check_vanity(session, mode):
    while True:
        try:
            with open(f"./urls/{mode}.txt") as f:
                lines = f.readlines()

            word = random.choice(lines).strip()
            response_data, status_code, _ = await fetch(session, f"https://www.guilded.gg/api/teams/lookup?value={word}")
            if status_code == 200:
                if response_data.get("exists") is False:
                    Logger.info(f"{status_code} | Vanity {word} is available")
                else:
                    Logger.error(f"{status_code} | Vanity {word} is not available")
            elif status_code == 429:
                Logger.error(f"{status_code} | Ratelimited, sleeping for 30 seconds..")
                await asyncio.sleep(30)
            else:
                Logger.error(f"{status_code} | Error: {response_data}")
        except Exception as e:
            Logger.error(f"Error: {e}")

async def setup():
    with open("./data/config.json") as f:
        config = json.load(f)

    async with aiohttp.ClientSession() as session:
        await check_vanity(session, config["mode"])

if __name__ == "__main__":
    asyncio.run(setup())