from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
from typing import Optional
from dotenv import load_dotenv
import tmdbsimple as tmdb
import os
import re
from utils.logger import send_error_message
import inspect

tmdb.api_key = os.getenv("TMDB_API_KEY")

class Streamer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @staticmethod
    async def extract_id(ctx, input_id):
        pattern = r'\b(tt\d{7,8}|\d{1,10})\b'
        matches = re.findall(pattern, input_id)
        if len(matches)==0:
            return await send_error_message(ctx, "Invalid ID provided. Please re-verify.")
        return matches[0]
    
    @staticmethod
    async def get_video_id(ctx, name, video_type):
        if name is None:
            return await send_error_message(ctx, "You need to provide either the name of the movie or show as in IMDB or TMDB or their IDs from the same websites. Please re-verify.")
        searcher = tmdb.Search()
        if video_type == 'movie':
            searcher.movie(query=name)
        else:
            searcher.tv(query=name)
        results = searcher.results
        if len(results)==0 or not results:
            return await send_error_message(ctx, "Show not found! Please look it up in IMDB or TMDB and provide the ID from the URL as a parameter.")
        return searcher.results[0]['id']

    @commands.hybrid_command(name="get-movie-or-tv", with_app_command=True, description="Get a movie or TV show embed", aliases=['movie', 'tv'])
    async def get_movie_or_tv(self, ctx:commands.Context, video_type, name: Optional[str]=None, imdb_id: Optional[str]=None, tmdb_id: Optional[str]=None, season: Optional[int]=None, episode: Optional[int]=None):
        base_url = "https://vidsrc.to/embed/"
        if not video_type:
            return send_error_message(ctx, "Please provide some details.")
        if video_type=='movie':
            base_url+="movie/"
        else:
            base_url+="tv/"
        if imdb_id is None and tmdb_id is None:
            video_id = await Streamer.get_video_id(ctx, name, video_type)
        else:
            video_id = await Streamer.extract_id(ctx, tmdb_id if tmdb_id else imdb_id)
        if not video_id or inspect.iscoroutine(video_id):
            return
        base_url+=f"{video_id}/"
        if season:
            base_url+=f"{season}/"
            if episode:
                base_url+=str(episode)
        final_url1 = base_url
        final_url2 = base_url[:15]+'xyz'+base_url[17:]
        button1 = Button(label="Watch Here", style=ButtonStyle.primary, row=0, url=final_url1)
        button2 = Button(label="If above didn't work, Try This", style=ButtonStyle.secondary, row=1, url=final_url2)
        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await ctx.reply("Here you go. If both don't work... well all the best finding it.", view=view)

    
async def setup(bot):
    await bot.add_cog(Streamer(bot))
