import discord
from discord.ext import commands, tasks
import requests
import os
from dotenv import load_dotenv
import asyncio

# 에이펙스 레전드 영어-한글 맵 이름 매핑
MAP_NAME_MAP = {
    "Broken Moon": "브로큰 문",
    "Storm Point": "좆톰포인트",
    "E-District": "E-디스트릭트",
    "Olympus": "올림푸스",
    "World's Edge": "세상의 끝",
    "King's Canyon": "킹스 캐년"
}

# 에이펙스 레전드 영어-한글 이름 매핑
LEGEND_NAME_MAP = {
    "Bloodhound": "블러드하운드",
    "Gibraltar": "지브롤터", 
    "Lifeline": "라이프라인",
    "Pathfinder": "패스파인더",
    "Wraith": "레이스",
    "Bangalore": "방갈로르",
    "Caustic": "코스틱",
    "Mirage": "미라지",
    "Octane": "옥테인",
    "Wattson": "왓슨",
    "Crypto": "크립토",
    "Revenant": "레버넌트",
    "Loba": "로바",
    "Rampart": "램파트",
    "Horizon": "호라이즌",
    "Fuse": "퓨즈",
    "Valkyrie": "발키리",
    "Seer": "시어",
    "Ash": "애쉬",
    "Mad Maggie": "매드 매기",
    "Newcastle": "뉴캐슬",
    "Vantage": "반티지",
    "Catalyst": "캐털리스트",
    "Ballistic": "발리스틱",
    "Conduit": "콘딧"
}

def translate_legend_name(english_name):
    """영어 레전드 이름을 한글로 변환하는 함수"""
    return LEGEND_NAME_MAP.get(english_name, english_name)

def translate_map_name(english_name):
    """영어 맵 이름을 한글로 변환하는 함수"""
    return MAP_NAME_MAP.get(english_name, english_name)

class ApexCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.APEX_API_KEY = os.getenv('APEX_API_KEY')
        
        # 주기적 태스크 시작
        if not self.periodic_api_request.is_running():
            self.periodic_api_request.start()

    # 주기적으로 맵 로테이션 API 요청을 보내는 태스크 (1시간 30분 = 5400초)
    @tasks.loop(seconds=5400)
    async def periodic_api_request(self):
        """1시간 30분마다 API 요청을 보내는 태스크"""
        try:
            url = f"https://api.mozambiquehe.re/maprotation?auth={self.APEX_API_KEY}&version=2"
            
            response = requests.get(url)
            data = response.json()
            
            if "Error" not in data:
                current_br_map = data['battle_royale']['current']['map']
                current_rank_map = data['ranked']['current']['map']
                print(f"[주기적 요청] 맵 로테이션 데이터를 성공적으로 가져왔습니다.")
                print(f"맵: {current_br_map}, 남은시간: {data['battle_royale']['current']['remainingTimer']}")
                
                # E-District나 Broken Moon일 경우 메시지 전송
                if current_br_map in ["E-District", "Broken Moon"]:
                    print(f"[맵 알림] {current_br_map} 맵이 감지되었습니다. 메시지 전송을 시작합니다...")
                    
                    # 모든 텍스트 채널에 메시지 전송
                    for guild in self.bot.guilds:
                        print(f"[맵 알림] 서버 '{guild.name}'에서 메시지 전송 시도 중...")
                        
                        for channel in guild.text_channels:
                            try:
                                # 봇이 해당 채널에 메시지를 보낼 권한이 있는지 확인
                                if channel.permissions_for(guild.me).send_messages:
                                    await channel.send(f"🎮 **맵 알림** 🎮\n현재 일반게임 맵이 **{translate_map_name(current_br_map)}**입니다!\n남은시간: {data['battle_royale']['current']['remainingTimer']}\n현재 랭크 맵은 **{translate_map_name(current_rank_map)}**입니다.")
                                    print(f"[맵 알림] '{guild.name}' 서버의 '{channel.name}' 채널에 메시지 전송 성공!")
                                    break  # 각 서버당 하나의 채널에만 메시지 전송
                                else:
                                    print(f"[맵 알림] '{guild.name}' 서버의 '{channel.name}' 채널에 메시지 전송 권한이 없습니다.")
                            except Exception as e:
                                print(f"[맵 알림] '{guild.name}' 서버의 '{channel.name}' 채널에 메시지 전송 실패: {e}")
                                continue
                        else:
                            print(f"[맵 알림] '{guild.name}' 서버에서 메시지를 보낼 수 있는 채널이 없습니다.")
            else:
                print(f"[주기적 요청] 맵 로테이션 데이터를 가져올 수 없습니다.")
                
        except Exception as e:
            print(f"[주기적 요청] 오류 발생: {e}")

    @commands.command(name='전적')
    async def get_apex_stats(self, ctx, player_name: str):
        # API 요청 URL (플랫폼은 PC 기본)
        url = f"https://api.mozambiquehe.re/bridge?auth={self.APEX_API_KEY}&player={player_name}&platform=PC"

        try:
            # API에 데이터 요청
            response = requests.get(url)
            data = response.json() # 응답을 JSON 형태로 변환

            # 에러 처리: 플레이어 정보가 없을 경우
            if "Error" in data:
                await ctx.send(f"플레이어 '{player_name}'를 찾을 수 없거나 API 오류가 발생했습니다. 닉네임을 확인해주세요.")
                return

            # 성공적으로 데이터를 받아왔을 때, 임베드(Embed) 형태로 가공
            # 임베드는 디스코드 메시지를 보기 좋게 꾸며주는 기능입니다.
            embed = discord.Embed(
                title=f"{data['global']['name']}님의 에이펙스 레전드 전적",
                description=f"레벨: {data['global']['level']} | 플랫폼: {data['global']['platform']}",
                color=discord.Color.red() # 임베드 색상
            )
            embed.set_thumbnail(url=data['global']['rank']['rankImg']) # 랭크 아이콘을 썸네일로 설정

            # 주요 정보 추가
            embed.add_field(name="현재 랭크", value=f"{data['global']['rank']['rankName']} {data['global']['rank']['rankDiv']} ({data['global']['rank']['rankScore']} RP)", inline=True)
            embed.add_field(name="상위", value=f"{data['global']['rank']['ALStopPercentGlobal']}%", inline=True)
            embed.add_field(name="순위", value=f"{data['global']['rank']['ALStopIntGlobal']}위", inline=True)
            embed.add_field(name="총 킬", value=f"{data.get('total', {}).get('kills', {}).get('value', 'N/A')}회", inline=True)
            embed.add_field(name="K/D", value=f"{data.get('total', {}).get('kd', {}).get('value', 'N/A')}", inline=True)
            embed.add_field(name="\u200b", value="\u200b", inline=True)  # 빈 필드

            # 선택된 레전드 정보 추가
            selected_legend = None
            max_kills = 0
            topPercent = 0
            
            # 모든 레전드의 킬 정보를 저장할 리스트
            legend_kills = []
            
            # 모든 레전드의 킬 데이터 수집
            for legend_name, legend_data in data['legends']['all'].items():
                if legend_data is not None and legend_data.get('data'):
                    for stat in legend_data['data']:
                        if stat.get('name') == 'BR Kills':
                            kills = stat.get('value', 0)
                            top_percent = stat.get('rank', {}).get('topPercent', 'N/A')
                            legend_info = {
                                'name': legend_name,
                                'data': legend_data,
                                'kills': kills,
                                'topPercent': top_percent
                            }
                            legend_kills.append(legend_info)

            # 킬 수로 정렬하여 상위 3개 레전드 선택
            legend_kills.sort(key=lambda x: x['kills'], reverse=True)
            top_3_legends = legend_kills[:3]

            # 레전드 데이터가 있는 경우에만 표시
            if top_3_legends:
                for i, legend in enumerate(top_3_legends, 1):
                    korean_legend_name = translate_legend_name(legend['name'])
                    embed.add_field(name=f"#{i} 주력 레전드", value=korean_legend_name, inline=True)
                    embed.add_field(name="킬", value=f"{legend['kills']}회", inline=True)
                    embed.add_field(name="상위", value=f"{legend['topPercent']}%", inline=True)
                
                # 첫 번째 레전드의 배너 이미지 표시
                embed.set_image(url=top_3_legends[0]['data']['ImgAssets']['banner'])
            else:
                # 레전드 데이터가 없는 경우 기본 메시지 표시
                embed.add_field(name="주력 레전드", value="데이터 없음", inline=True)
                embed.add_field(name="킬", value="N/A", inline=True)
                embed.add_field(name="상위", value="N/A", inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"오류가 발생했습니다: {e}")

    # 테스트용 명령어 - 맵 알림 기능 테스트
    @commands.command(name='맵테스트')
    async def test_map_alert(self, ctx):
        """맵 알림 기능을 테스트하는 명령어"""
        try:
            url = f"https://api.mozambiquehe.re/maprotation?auth={self.APEX_API_KEY}&version=2"
            response = requests.get(url)
            data = response.json()
            
            if "Error" not in data:
                current_br_map = data['battle_royale']['current']['map']
                current_rank_map = data['ranked']['current']['map']
                
                embed = discord.Embed(
                    title="🎮 현재 맵 로테이션",
                    color=discord.Color.blue()
                )
                embed.add_field(name="일반게임 맵", value=f"{translate_map_name(current_br_map)}", inline=True)
                embed.add_field(name="랭크 맵", value=f"{translate_map_name(current_rank_map)}", inline=True)
                embed.add_field(name="남은 시간", value=data['battle_royale']['current']['remainingTimer'], inline=True)
                
                if current_br_map in ["E-District", "Broken Moon"]:
                    embed.add_field(name="알림 상태", value="🔔 알림 대상 맵입니다!", inline=False)
                else:
                    embed.add_field(name="알림 상태", value="🔕 알림 대상이 아닙니다.", inline=False)
                    
                await ctx.send(embed=embed)
            else:
                await ctx.send("맵 로테이션 데이터를 가져올 수 없습니다.")
                
        except Exception as e:
            await ctx.send(f"테스트 중 오류가 발생했습니다: {e}")

async def setup(bot):
    await bot.add_cog(ApexCog(bot))