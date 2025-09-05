import discord
from discord.ext import commands
import re

class EmojiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """메시지에서 이모티콘을 감지하고 확대해서 보여주는 기능"""
        # 봇의 메시지는 무시
        if message.author.bot:
            return
        
        # 이모티콘 패턴 찾기 (커스텀 이모티콘과 유니코드 이모티콘)
        custom_emoji_pattern = r'<a?:(\w+):(\d+)>'
        unicode_emoji_pattern = r'[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U0001F1E0-\U0001F1FF]|[\U00002600-\U000027BF]|[\U0001f900-\U0001f9ff]|[\U0001f1e0-\U0001f1ff]'
        
        custom_emojis = re.findall(custom_emoji_pattern, message.content)
        unicode_emojis = re.findall(unicode_emoji_pattern, message.content)
        
        # 커스텀 이모티콘 처리
        if custom_emojis:
            for emoji_name, emoji_id in custom_emojis:
                try:
                    # 이모티콘 객체 생성
                    emoji = discord.PartialEmoji(name=emoji_name, id=int(emoji_id), animated=message.content.startswith('<a:'))
                    
                    # 확대된 이모티콘 메시지 전송
                    embed = discord.Embed(
                        title=f"{message.author.display_name}",
                        description=f"",
                        color=discord.Color.blue()
                    )
                    embed.set_image(url=emoji.url)
                    
                    await message.channel.send(embed=embed)
                    
                except Exception as e:
                    print(f"이모티콘 처리 중 오류: {e}")
        
        # 유니코드 이모티콘 처리
        if unicode_emojis:
            return

    @commands.command(name='서버이모지')
    async def server_emojis(self, ctx):
        """서버의 모든 커스텀 이모티콘을 보여주는 명령어""" 
        if not ctx.guild:
            await ctx.send("이 명령어는 서버에서만 사용할 수 있습니다.")
            return
        
        emojis = ctx.guild.emojis
        if not emojis:
            await ctx.send("이 서버에는 커스텀 이모티콘이 없습니다.")
            return
        
        # 이모티콘을 10개씩 나누어서 표시
        for i in range(0, len(emojis), 10):
            emoji_batch = emojis[i:i+10]
            emoji_list = []
            
            for emoji in emoji_batch:
                emoji_list.append(f"{emoji} `{emoji.name}`")
            
            embed = discord.Embed(
                title=f"📋 서버 이모티콘 목록 ({i+1}-{min(i+10, len(emojis))}/{len(emojis)})",
                description="\n".join(emoji_list),
                color=discord.Color.purple()
            )
            
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EmojiCog(bot))
