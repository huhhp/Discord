import os
import json
import random
import discord
from discord.ext import commands
import wavelink
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get token from environment variable
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    logger.error("Discord token not found in environment variables!")
    exit(1)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

RANK_FILE = "rank.json"

# Initialize rank file
def init_rank_file():
    if not os.path.exists(RANK_FILE):
        try:
            with open(RANK_FILE, "w") as f:
                json.dump({}, f)
        except Exception as e:
            logger.error(f"Failed to create rank file: {e}")

def load_rank():
    try:
        with open(RANK_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Rank file not found or corrupted, creating new one")
        init_rank_file()
        return {}

def save_rank(rank):
    try:
        with open(RANK_FILE, "w") as f:
            json.dump(rank, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save rank file: {e}")

# Initialize rank file on startup
init_rank_file()

# ---------- Music Node Setup ----------
@bot.event
async def on_ready():
    logger.info(f"Bot {bot.user} is ready!")
    
    # Initialize music functionality (optional - bot works perfectly without it)
    logger.info("🎯 Discord Bot fully operational!")
    logger.info("💡 Features available: AI chat, XP/rank system, roles, announcements, private rooms")
    logger.info("🎵 Music system: Available for future enhancement with Lavalink")

# ---------- 1. Music Commands ----------
@bot.command()
async def join(ctx):
    """Join the voice channel"""
    if ctx.author.voice and ctx.author.voice.channel:
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send(f"🔗 เชื่อมต่อกับ {ctx.author.voice.channel.name}")
        except Exception as e:
            await ctx.send(f"❌ ไม่สามารถเข้าห้องเสียงได้: {e}")
            logger.error(f"Failed to join voice channel: {e}")
    else:
        await ctx.send("❌ คุณต้องเข้าห้องเสียงก่อน!")

@bot.command()
async def leave(ctx):
    """Leave the voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ออกจากห้องเสียงแล้ว!")
    else:
        await ctx.send("❌ ไม่ได้อยู่ในห้องเสียง")

@bot.command()
async def play(ctx, *, search: str):
    """Play music from YouTube (feature in development)"""
    embed = discord.Embed(
        title="🎵 ระบบเพลง",
        description="ฟีเจอร์เพลงกำลังพัฒนา จะเปิดใช้งานในอนาคต",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="🎯 ฟีเจอร์ที่พร้อมใช้งาน",
        value="```!ai - คุยกับ AI\n!rank - ดู XP\n!leaderboard - ดูอันดับ\n!emoji - ตกแต่งข้อความ\n!announce - ประกาศ\n!pinhelp - คู่มือ```",
        inline=False
    )
    await ctx.send(embed=embed)

    vc: wavelink.Player = ctx.voice_client
    if not vc:
        if ctx.author.voice:
            try:
                vc = await ctx.author.voice.channel.connect(cls=wavelink.Player)
                await ctx.send(f"🔗 เชื่อมต่อกับ {ctx.author.voice.channel.name}")
            except Exception as e:
                await ctx.send(f"❌ ไม่สามารถเข้าห้องเสียงได้: {e}")
                return
        else:
            await ctx.send("❌ คุณต้องเข้าห้องเสียงก่อน!")
            return

    try:
        # Search for tracks
        tracks = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            await ctx.send("❌ ไม่พบเพลงที่ค้นหา!")
            return

        track = tracks[0]
        await vc.play(track)

        # Create embed for now playing
        embed = discord.Embed(
            title="🎵 กำลังเล่น",
            description=f"**{track.title}**",
            color=discord.Color.green()
        )
        
        if hasattr(track, 'author') and track.author:
            embed.add_field(name="ศิลปิน", value=track.author, inline=True)
        
        if hasattr(track, 'duration') and track.duration:
            minutes, seconds = divmod(track.duration // 1000, 60)
            embed.add_field(name="ความยาว", value=f"{minutes:02d}:{seconds:02d}", inline=True)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"❌ เกิดข้อผิดพลาดในการเล่นเพลง: {e}")
        logger.error(f"Play error: {e}")

@bot.command()
async def stop(ctx):
    """Stop music playback"""
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        await ctx.send("❌ ไม่ได้อยู่ในห้องเสียง")
        return
    await vc.stop()
    await ctx.send("⏹️ หยุดเล่นเพลงแล้ว")

@bot.command()
async def pause(ctx):
    """Pause music playback"""
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        await ctx.send("❌ ไม่ได้อยู่ในห้องเสียง")
        return
    await vc.pause(True)
    await ctx.send("⏸️ หยุดเพลงชั่วคราว")

@bot.command()
async def resume(ctx):
    """Resume music playback"""
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        await ctx.send("❌ ไม่ได้อยู่ในห้องเสียง")
        return
    await vc.pause(False)
    await ctx.send("▶️ เล่นเพลงต่อ")

@bot.command()
async def skip(ctx):
    """Skip current track"""
    vc: wavelink.Player = ctx.voice_client
    if not vc:
        await ctx.send("❌ ไม่ได้อยู่ในห้องเสียง")
        return
    await vc.stop()
    await ctx.send("⏭️ ข้ามเพลงแล้ว")

@bot.command()
async def lavalink_status(ctx):
    """Check Lavalink server status"""
    if not wavelink.Pool.nodes:
        await ctx.send("❌ ไม่มี Lavalink server เชื่อมต่อ!")
        return
    
    embed = discord.Embed(
        title="🔗 Lavalink Server Status",
        color=discord.Color.green()
    )
    
    for node in wavelink.Pool.nodes.values():
        status = "🟢 Online" if node.connected else "🔴 Offline"
        embed.add_field(
            name=f"Server: {node.identifier}",
            value=f"Status: {status}",
            inline=False
        )
    
    await ctx.send(embed=embed)

# ---------- 2. AI Chat ----------
@bot.command()
async def ai(ctx, *, question=None):
    """Chat with AI bot"""
    RESPONSES = [
        "วันนี้เป็นไงบ้างเอ่ย 😊", "สู้ๆ นะ!", "มีอะไรให้ช่วยก็บอกได้เลย",
        "ขอบคุณที่คุยกับฉัน!", "รักทุกคนในเซิร์ฟนี้เสมอ!", "พร้อมพัฒนาไปกับคุณ!",
        "วันนี้มีอะไรใหม่ๆ บ้างไหม?", "ฟังเพลงกันเถอะ!", "อยากให้ช่วยอะไรไหม?",
        "หวังว่าทุกคนจะมีความสุขนะ", "มาคุยกันได้เสมอเลย!", "พูดคุยกับฉันได้ทุกเมื่อ!",
        "มีคำถามอะไรถามได้เลย", "ฉันพร้อมฟังคุณเสมอ", "วันนี้เป็นวันที่ดีใช่ไหม?"
    ]
    
    if not question:
        await ctx.send("🤖 ถามหรือปรึกษาอะไรก็ได้เลย~")
    else:
        response = random.choice(RESPONSES)
        await ctx.send(f"🤖 {response}")

# ---------- 3. Rank/Level System ----------
@bot.command()
async def addxp(ctx, user: discord.Member, xp: int):
    """Add XP to a user"""
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
        return
    
    rank = load_rank()
    uid = str(user.id)
    rank[uid] = rank.get(uid, 0) + xp
    save_rank(rank)
    
    total_xp = rank[uid]
    level = total_xp // 100
    
    embed = discord.Embed(
        title="✨ เพิ่ม XP สำเร็จ",
        description=f"{user.display_name} ได้รับ XP เพิ่ม {xp}!",
        color=discord.Color.gold()
    )
    embed.add_field(name="XP ทั้งหมด", value=total_xp, inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def rank(ctx, user: discord.Member = None):
    """Check user's rank and XP"""
    rank = load_rank()
    user = user or ctx.author
    uid = str(user.id)
    xp = rank.get(uid, 0)
    level = xp // 100
    
    embed = discord.Embed(
        title="🏆 ข้อมูลผู้ใช้",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=user.avatar.url if user.avatar else None)
    embed.add_field(name="ชื่อผู้ใช้", value=user.display_name, inline=True)
    embed.add_field(name="XP", value=xp, inline=True)
    embed.add_field(name="Level", value=level, inline=True)
    
    await ctx.send(embed=embed)

@bot.command()
async def leaderboard(ctx):
    """Show top 10 users by XP"""
    rank = load_rank()
    if not rank:
        await ctx.send("📊 ยังไม่มีข้อมูล XP ของใครเลย!")
        return

    sorted_users = sorted(rank.items(), key=lambda x: x[1], reverse=True)[:10]
    
    embed = discord.Embed(
        title="🏆 Leaderboard Top 10",
        color=discord.Color.gold()
    )
    
    description = ""
    for i, (user_id, xp) in enumerate(sorted_users, 1):
        try:
            user = bot.get_user(int(user_id))
            name = user.display_name if user else f"User {user_id}"
            level = xp // 100
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            description += f"{medal} {name} - XP: {xp} | Level: {level}\n"
        except:
            continue
    
    embed.description = description
    await ctx.send(embed=embed)

# ---------- 4. Anti-Spam System ----------
last_message = {}

@bot.event
async def on_message(message):
    """Handle message events for anti-spam and auto XP"""
    if message.author.bot:
        return

    channel_id = message.channel.id
    user_id = message.author.id

    # Anti-spam check
    if channel_id not in last_message:
        last_message[channel_id] = {}

    last = last_message[channel_id].get(user_id, "")
    if message.content == last and len(message.content) > 5:
        try:
            await message.delete()
            warning = await message.channel.send(
                f"⚠️ {message.author.mention} อย่าสแปมข้อความซ้ำเกินไปนะ!"
            )
            await asyncio.sleep(5)
            await warning.delete()
        except discord.errors.NotFound:
            pass
        except Exception as e:
            logger.error(f"Anti-spam error: {e}")
    else:
        last_message[channel_id][user_id] = message.content
        
        # Auto XP system (1 XP per message)
        if not message.content.startswith('!'):
            rank = load_rank()
            uid = str(user_id)
            rank[uid] = rank.get(uid, 0) + 1
            save_rank(rank)

    await bot.process_commands(message)

# ---------- 5. Emoji Decoration ----------
@bot.command()
async def emoji(ctx, *, msg: str):
    """Add random emojis to your message"""
    EMOJIS = ["✨", "🔥", "💎", "🌈", "🎉", "⭐", "🌟", "💫", "🎊", "🎈", "🦄", "🌸", "🎭", "🎪", "🎨"]
    left_emoji = random.choice(EMOJIS)
    right_emoji = random.choice(EMOJIS)
    result = f"{left_emoji} {msg} {right_emoji}"
    await ctx.send(result)

# ---------- 6. Announcement System ----------
@bot.command()
async def announce(ctx, *, msg: str):
    """Make an announcement"""
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
        return
    
    embed = discord.Embed(
        title="📢 ประกาศสำคัญ",
        description=msg,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"ประกาศโดย {ctx.author.display_name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    embed.timestamp = ctx.message.created_at
    
    await ctx.send(embed=embed)

# ---------- 7. Room & Role Management ----------
@bot.command()
async def create_private(ctx, *, name: str):
    """Create a private text channel"""
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
        return
    
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    
    try:
        channel = await ctx.guild.create_text_channel(name, overwrites=overwrites)
        await channel.send(f"🏠 ห้องส่วนตัวสำหรับ {ctx.author.mention}!\nพิมพ์ `!delete_private` เพื่อลบห้องนี้")
        await ctx.send(f"✅ สร้างห้องส่วนตัว {channel.mention} เรียบร้อยแล้ว!")
    except Exception as e:
        await ctx.send(f"❌ ไม่สามารถสร้างห้องได้: {e}")

@bot.command()
async def delete_private(ctx):
    """Delete the current private channel"""
    if ctx.channel.name.startswith(ctx.author.name.lower()) or ctx.author.guild_permissions.manage_channels:
        try:
            await ctx.channel.delete()
        except Exception as e:
            await ctx.send(f"❌ ไม่สามารถลบห้องได้: {e}")
    else:
        await ctx.send("❌ คุณไม่มีสิทธิ์ลบห้องนี้!")

@bot.command()
async def giverole(ctx, member: discord.Member, *, role_name: str):
    """Give a role to a member"""
    if not ctx.author.guild_permissions.manage_roles:
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
        return
    
    try:
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            role = await ctx.guild.create_role(name=role_name, colour=discord.Colour.random())
        
        await member.add_roles(role)
        
        embed = discord.Embed(
            title="👑 มอบยศสำเร็จ",
            description=f"{member.mention} ได้รับยศ **{role.name}** แล้ว!",
            color=role.color
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ ไม่สามารถให้ยศได้: {e}")

# ---------- 8. Logging System ----------
@bot.event
async def on_command(ctx):
    """Log command usage"""
    logger.info(f"Command: {ctx.command} by {ctx.author} in {ctx.channel}")
    try:
        with open("self_improve.log", "a", encoding="utf-8") as f:
            f.write(f"[{ctx.message.created_at}] {ctx.author} used {ctx.command} in {ctx.channel}\n")
    except Exception as e:
        logger.error(f"Log error: {e}")

# ---------- 9. AI Suggestions ----------
@bot.command()
async def upgrade_ai(ctx):
    """Get AI suggestions for bot improvements"""
    suggestions = [
        "ควรเพิ่ม mini-game หรือระบบกิจกรรมในเซิร์ฟ",
        "เพิ่มโมดูล AI Chat ภาษาไทย-อังกฤษ (แปล/ถามตอบอัตโนมัติ)",
        "สร้างระบบแจ้งเตือน event, schedule หรือ countdown",
        "พัฒนาระบบ anti-spam ให้ฉลาดขึ้น เช่น ใช้ AI จับ pattern ข้อความ",
        "เก็บ log การใช้งานแบบสรุปรายเดือน/รายสัปดาห์",
        "เชื่อมกับฐานข้อมูลหรือระบบความจำระยะยาว",
        "ใส่ระบบความปลอดภัย/ตรวจจับบัญชีใหม่/auto-ban",
        "เพิ่มระบบ queue เพลง และ playlist",
        "สร้างระบบ economy และ shop",
        "เพิ่มระบบ moderation อัตโนมัติ",
        "ระบบ backup ข้อมูลอัตโนมัติ",
        "การแจ้งเตือนผ่าน DM สำหรับสมาชิกใหม่"
    ]
    
    embed = discord.Embed(
        title="🧠 AI Suggestion",
        description=random.choice(suggestions),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# ---------- 10. Help System ----------
@bot.command()
async def pinhelp(ctx):
    """Pin help message with all commands"""
    embed = discord.Embed(
        title="🎉 คู่มือใช้งานบอทในเซิร์ฟเวอร์นี้",
        description="รายการคำสั่งทั้งหมดที่ใช้ได้",
        color=discord.Color.green()
    )
    
    embed.add_field(
        name="🎵 คำสั่งเพลง",
        value="```!join - เข้าห้องเสียง\n!leave - ออกจากห้องเสียง\n!play [ชื่อเพลง] - เปิดเพลง\n!stop - หยุดเพลง\n!pause - หยุดชั่วคราว\n!resume - เล่นต่อ\n!skip - ข้ามเพลง\n!lavalink_status - ตรวจสอบเซิร์ฟเวอร์เพลง```",
        inline=False
    )
    
    embed.add_field(
        name="🤖 AI & ระบบ",
        value="```!ai [ข้อความ] - คุยกับ AI\n!upgrade_ai - ขอข้อเสนอใหม่```",
        inline=False
    )
    
    embed.add_field(
        name="🏆 ระบบ XP/Rank",
        value="```!addxp @user [จำนวน] - เพิ่ม XP\n!rank [@user] - ดู XP\n!leaderboard - ดู top 10```",
        inline=False
    )
    
    embed.add_field(
        name="👑 จัดการเซิร์ฟเวอร์",
        value="```!giverole @user [ยศ] - แจกยศ\n!create_private [ชื่อห้อง] - สร้างห้องส่วนตัว\n!delete_private - ลบห้องส่วนตัว\n!announce [ข้อความ] - ประกาศ```",
        inline=False
    )
    
    embed.add_field(
        name="✨ อื่นๆ",
        value="```!emoji [ข้อความ] - ตกแต่งข้อความ\n!pinhelp - แสดงคู่มือนี้```",
        inline=False
    )
    
    embed.set_footer(text="Bot พัฒนาโดย Python + discord.py + wavelink")
    
    try:
        msg = await ctx.send(embed=embed)
        await msg.pin()
        await ctx.send("📌 ปักหมุดคู่มือการใช้งานเรียบร้อย!")
    except Exception as e:
        await ctx.send(f"❌ ไม่สามารถปักหมุดได้: {e}")

# ---------- Error Handling ----------
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ ข้อมูลไม่ครบ! ใช้ `!pinhelp` เพื่อดูคู่มือ")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ ไม่พบสมาชิกที่ระบุ!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ บอทไม่มีสิทธิ์ทำงานนี้!")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send("❌ เกิดข้อผิดพลาดที่ไม่คาดคิด!")

# ---------- Keep Alive for Render ----------
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Discord Bot is running!')
    
    def log_message(self, format, *args):
        return  # Suppress HTTP logs

def run_server():
    port = int(os.environ.get('PORT', 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), KeepAliveHandler)
        logger.info(f"HTTP server running on port {port}")
        server.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            logger.info(f"Port {port} already in use - server already running")
        else:
            logger.error(f"HTTP server error: {e}")

# Start HTTP server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# ---------- Run Bot ----------
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"Bot startup error: {e}")
        exit(1)
