from discord.ext import commands
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
        await ctx.reply(f"Try:\n{base_url}\nIf the above link does not work, try:\n{base_url[:15]+'xyz'+base_url[17:]}\n\nIf the above link does not work as well... well all the best finding it.")

    
async def setup(bot):
    await bot.add_cog(Streamer(bot))