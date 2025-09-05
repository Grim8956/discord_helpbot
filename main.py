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
    cogs_to_load = ['cogs.apex_cog', 'cogs.emoji_cog', 'cogs.maplestory_cog']
    
    for cog in cogs_to_load:
        try:
            await bot.load_extension(cog)
            print(f"✅ {cog}가 성공적으로 로드되었습니다!")
        except Exception as e:
            print(f"❌ {cog} 로드 실패: {e}")

# 명령어 도움말 기능
@bot.command(name='명령어')
async def help_command(ctx):
    """사용 가능한 모든 명령어와 설명을 보여주는 명령어"""
    
    # 임베드 생성
    embed = discord.Embed(
        title="🤖 망통방 도우미 명령어 목록",
        description="사용 가능한 모든 명령어와 설명입니다.",
        color=discord.Color.blue()
    )
    
    # 기본 명령어 섹션
    embed.add_field(
        name="📋 기본 명령어",
        value="`!명령어` - 이 도움말을 표시합니다",
        inline=False
    )
    
    # Apex 관련 명령어 섹션
    embed.add_field(
        name="🎮 Apex 레전드 명령어",
        value=(
            "`!전적 <플레이어명>` - 플레이어의 전적을 조회합니다\n"
            "`!맵테스트` - 현재 맵 로테이션을 확인합니다\n"
            "`!맵알림` - E-District, Broken Moon 맵 자동 알림 (1시간 30분마다)"
        ),
        inline=False
    )
    
    # 메이플스토리 관련 명령어 섹션
    embed.add_field(
        name="🍁 메이플스토리 명령어",
        value=(
            "`!내캐릭터 <캐릭터명>` - 캐릭터 기본 정보를 조회합니다\n"
            "`!스타포스결과 <캐릭터명>` - 스타포스 강화 결과를 조회합니다 (최대 1000개)\n"
            "`!잠재능력결과 <캐릭터명>` - 잠재능력 강화 결과를 조회합니다 (최대 1000개)\n"
            "`!큐브결과 <캐릭터명>` - 큐브 사용 결과를 조회합니다 (최대 1000개)"
        ),
        inline=False
    )
    
    # 이모티콘 관련 명령어 섹션
    embed.add_field(
        name="😀 이모티콘 명령어",
        value=(
            "`!서버이모지` - 서버의 모든 커스텀 이모티콘을 보여줍니다\n"
            "`자동 이모티콘 확대` - 메시지에 이모티콘이 있으면 자동으로 확대합니다"
        ),
        inline=False
    )
    
    # 사용법 안내
    embed.add_field(
        name="💡 사용법",
        value=(
            "• 명령어는 `!` 접두사를 사용합니다\n"
            "• `<플레이어명>` 같은 괄호는 실제 값으로 바꿔서 입력하세요\n"
            "• 예시: `!전적 Wraith`"
        ),
        inline=False
    )
    
    # 봇 정보
    embed.set_footer(text=f"요청자: {ctx.author.display_name} | 봇 버전: 1.0")
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    
    await ctx.send(embed=embed)

# .env 파일에서 불러온 토큰으로 봇을 실행합니다.
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)