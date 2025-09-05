import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수를 불러옵니다.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# 봇이 기본적인 명령어와 메시지 내용을 인식할 수 있도록 권한(intents)을 설정합니다.
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents) # 봇의 명령어 접두사를 '!'로 설정

# 봇이 성공적으로 로그인했을 때 실행되는 이벤트입니다.
@bot.event
async def on_ready():
    print(f'{bot.user.name} 봇이 성공적으로 로그인했습니다!')
    print('-----------------------------------------')
    
    # Cogs 로드
    cogs_to_load = ['cogs.apex_cog', 'cogs.emoji_cog']
    
    for cog in cogs_to_load:
        try:
            bot.load_extension(cog)
            print(f"✅ {cog}가 성공적으로 로드되었습니다!")
        except Exception as e:
            print(f"❌ {cog} 로드 실패: {e}")

# .env 파일에서 불러온 토큰으로 봇을 실행합니다.
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)