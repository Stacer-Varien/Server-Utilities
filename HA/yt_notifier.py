from re import search
import requests
from discord import SyncWebhook
from discord.ext import tasks, commands
from assets.functions import YouTube
from config import HAZEADS, LOA, ORLEANS, WEBHOOK_URL_1, WEBHOOK_URL_2

CHANNELS = {
    "CHANNEL_ID_1": "UChzTbosoH1cba3fyA1H_fRQ",
    "CHANNEL_ID_2": "UCpocUkY2iwmDAWRboPTRy3Q",
}


class YTNotifier(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.setup_notifier("CHANNEL_ID_1", WEBHOOK_URL_1, WEBHOOK_URL_2)
        self.setup_notifier("CHANNEL_ID_2", ORLEANS, HAZEADS, LOA)

    def setup_notifier(self, channel_id:int, *webhook_urls):
        task_method = getattr(self, f"check_{channel_id.lower()}")
        task = tasks.loop(minutes=5)(task_method)
        setattr(self, channel_id.lower(), task)
        task.start()

    def check_channel(self, channel_id:int, *webhook_urls):
        try:
            print(f"Now Checking For {channel_id}")
            youtube = YouTube(channel_id)
            channel_url = f"https://www.youtube.com/channel/{channel_id}"
            html = requests.get(f"{channel_url}/videos").text
            last_video = search('(?<="videoId":").*?(?=")', html).group()
            latest_video_url = f"https://www.youtube.com/watch?v={last_video}"

            latest_video = youtube.get_latest_vid()

            if latest_video is None:
                return

            if latest_video != latest_video_url:
                youtube.update_video(latest_video_url)

                for webhook_url in webhook_urls:
                    webhook = SyncWebhook.from_url(webhook_url)
                    channel_name = youtube.get_channel()

                    msg = f"{channel_name} just uploaded a new video!\nCheck it out: {latest_video_url}"
                    webhook.send(msg)
                    print(f"{latest_video_url} found and posted")
        except:
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(YTNotifier(bot))