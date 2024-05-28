from re import search

import requests
from discord import Message, SyncWebhook
from discord.ext import tasks, commands

from assets.functions import YouTube
from config import ORLEANS, WEBHOOK_URL_1, WEBHOOK_URL_2

CHANNEL_ID_1 = "UChzTbosoH1cba3fyA1H_fRQ"
CHANNEL_ID_2 = "UCpocUkY2iwmDAWRboPTRy3Q"


class YTNotifier(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.konekovibes.start()
        self.whitephoenix.start()

    @tasks.loop(hours=1)
    async def konekovibes(self):
        try:
            print(f"Now Checking For {CHANNEL_ID_1}")
            youtube = YouTube(CHANNEL_ID_1)
            channel = f"https://www.youtube.com/channel/{CHANNEL_ID_1}"
            html = requests.get(f"{channel}/videos").text
            last_video = search('(?<="videoId":").*?(?=")', html).group()
            latest_video_url = f"https://www.youtube.com/watch?v={last_video}"

            latest_video = youtube.get_latest_vid()

            if latest_video is None:
                return

            if latest_video != latest_video_url:
                youtube.update_video(latest_video_url)

                for webhook_url in [WEBHOOK_URL_1, WEBHOOK_URL_2]:
                    webhook = SyncWebhook.from_url(webhook_url)
                    channel_name = youtube.get_channel()

                    msg = f"{channel_name} just uploaded a new video!\nCheck it out: {latest_video_url}"
                    webhook.send(msg)
                    print(f"{latest_video_url} found and posted")
        except:
            return

    @tasks.loop(hours=1)
    async def whitephoenix(self):
        try:
            print(f"Now Checking For {CHANNEL_ID_2}")
            youtube = YouTube(CHANNEL_ID_2)
            channel = f"https://www.youtube.com/channel/{CHANNEL_ID_2}"
            html = requests.get(f"{channel}/videos").text
            last_video = search('(?<="videoId":").*?(?=")', html).group()
            latest_video_url = f"https://www.youtube.com/watch?v={last_video}"

            latest_video = youtube.get_latest_vid()

            if latest_video is None:
                return

            if latest_video != latest_video_url:
                youtube.update_video(latest_video_url)

                channel_name = youtube.get_channel()

                msg = f"{channel_name} just uploaded a new video!\nCheck it out: {latest_video_url}"
                webhook=SyncWebhook.from_url(ORLEANS)
                m:Message=await webhook.send(f"<@&1045345555485823036>\n{msg}")
                await m.publish()

                print(f"{latest_video_url} found and posted")
        except:
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(YTNotifier(bot))
