import discord
from discord.ext import commands
import requests
import os
from datetime import datetime, timedelta

MAPLESTORY_API_KEY = os.getenv('MAPLESTORY_API_KEY')

class MapleStoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_headers = {"x-nxopen-api-key": MAPLESTORY_API_KEY}
        # 오늘 날짜를 YYYY-MM-DD 형식으로 가져옵니다. (어제자 데이터 조회를 위함)
        # 넥슨 API는 보통 전날 데이터를 기준으로 조회해야 안정적입니다.
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')


    @commands.command(name='내캐릭터')
    async def get_maple_info(self, ctx, character_name: str):
        # 1단계: 캐릭터 이름으로 ocid 조회
        ocid_url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={character_name}"
        ocid_res = requests.get(ocid_url, headers=self.api_headers)
        
        if ocid_res.status_code != 200:
            await ctx.send(f"캐릭터 '{character_name}'의 ocid를 조회하는 데 실패했습니다. API 서버 문제일 수 있습니다.")
            return
            
        ocid_data = ocid_res.json()
        if 'ocid' not in ocid_data:
            await ctx.send(f"캐릭터 '{character_name}'를 찾을 수 없습니다. 닉네임을 확인해주세요.")
            return
        
        ocid = ocid_data['ocid']

        # 2단계: ocid로 캐릭터 기본 정보 조회
        char_url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={self.yesterday}"
        char_res = requests.get(char_url, headers=self.api_headers)
        char_data = char_res.json()

        embed = discord.Embed(
            title=f"{char_data.get('character_name')}님의 메이플스토리 정보",
            description=f"기준일: {self.yesterday}",
            color=discord.Color.orange()
        )
        # 썸네일 대신 더 큰 이미지로 표시
        embed.set_image(url=char_data.get('character_image'))
        embed.add_field(name="레벨", value=f"Lv. {char_data.get('character_level')}", inline=True)
        embed.add_field(name="직업", value=char_data.get('character_class'), inline=True)
        embed.add_field(name="서버", value=char_data.get('world_name'), inline=True)
        embed.add_field(name="길드", value=char_data.get('character_guild_name', '없음'), inline=True)
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MapleStoryCog(bot))