from bs4 import BeautifulSoup
import aiohttp
import asyncio

base_url = "https://market.yandex.ru"
max_pages = 10


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url + "/partners/news") as response:
            soup = BeautifulSoup(await response.text(), "lxml")

            pages = soup.find_all("a", class_="news-list__item-active")

        for i in range(min(10, len(pages))):
            async with session.get(base_url + pages[i]["href"]) as response:
                soup = BeautifulSoup(await response.text(), "lxml")

                title = soup.find("div", class_="news-info__title")
                # TODO: Убрать рекламу
                # TODO: Распарсить мелкие сектора
                desc = soup.find("div", class_="news-info__post-body html-content page-content")
                tags = [tag.text for tag in soup.find_all("a", class_="news-info__tag")]

                print(title.text)
                print(desc)
                print(tags)
            print()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
