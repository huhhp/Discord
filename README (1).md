# Discord Music Bot (Python + wavelink)

โปรเจกต์นี้เป็น Discord Bot ที่มีความสามารถด้านเพลงและระบบจัดการเซิร์ฟเวอร์

## ฟีเจอร์หลัก

- 🎵 **ระบบเพลง**: เปิดเพลงจาก YouTube ด้วย wavelink
- 🤖 **AI Chat**: คุยกับบอท AI ภาษาไทย
- 🏆 **ระบบ XP/Rank**: เพิ่ม XP ให้สมาชิก พร้อม Auto XP
- 🛡️ **Anti-Spam**: ป้องกันการส่งข้อความซ้ำ
- 👑 **จัดการยศ**: สร้างและแจกยศใหม่
- 🏠 **ห้องส่วนตัว**: สร้างห้องแชทส่วนตัว
- 📢 **ประกาศ**: ระบบประกาศข่าวสาร
- ✨ **ตกแต่งข้อความ**: เพิ่ม emoji ให้ข้อความ

## การ Deploy บน Render

### วิธีที่ 1: Deploy ด้วย Web Interface

1. **เตรียม Repository**
   - Fork repository นี้ไปยัง GitHub ของคุณ
   - หรือสร้าง repository ใหม่และ upload ไฟล์ทั้งหมด

2. **สร้าง Discord Bot**
   - ไปที่ [Discord Developer Portal](https://discord.com/developers/applications)
   - สร้าง Application ใหม่
   - ไปที่ Bot tab และสร้าง Bot
   - คัดลอก Token ไว้

3. **Deploy บน Render**
   - เข้า [Render.com](https://render.com) และสมัครสมาชิก
   - คลิก "New +" และเลือก "Web Service"
   - Connect กับ GitHub repository
   - ตั้งค่าดังนี้:
     - **Name**: discord-music-bot (หรือชื่อที่ต้องการ)
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`

4. **ตั้งค่า Environment Variables**
   - ไปที่ Environment tab
   - เพิ่ม Environment Variable:
     - **Key**: `DISCORD_TOKEN`
     - **Value**: Discord Bot Token ที่คัดลอกไว้

5. **Deploy**
   - คลิก "Create Web Service"
   - รอให้ build เสร็จสิ้น (ประมาณ 2-5 นาที)

### วิธีที่ 2: Deploy ด้วย render.yaml

1. ใช้ไฟล์ `render.yaml` ที่มีอยู่แล้ว
2. ไปที่ Render Dashboard
3. คลิก "New +" และเลือก "Blueprint"
4. Connect กับ repository และ Deploy

### การตั้งค่า Discord Bot Permissions

เมื่อเชิญบอทเข้าเซิร์ฟเวอร์ ให้เลือก permissions เหล่านี้:

**Text Permissions:**
- View Channels
- Send Messages
- Read Message History
- Use External Emojis
- Manage Messages
- Pin Messages

**Voice Permissions:**
- Connect
- Speak
- Use Voice Activity

**Advanced Permissions:**
- Manage Roles
- Manage Channels

### URL สำหรับเชิญบอท

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_BOT_CLIENT_ID&permissions=8&scope=bot
```

แทนที่ `YOUR_BOT_CLIENT_ID` ด้วย Client ID ของบอทจาก Discord Developer Portal

## การแก้ไขปัญหา

### ปัญหาที่พบบ่อย

1. **Build Failed - Python Version**
   - ใช้ Python 3.11.9 ที่ระบุใน runtime.txt
   - หลีกเลี่ยง Python 3.13 เนื่องจาก yarl dependency ไม่รองรับ

2. **Discord Token Missing**
   - ตรวจสอบให้แน่ใจว่าได้ตั้งค่า Environment Variable `DISCORD_TOKEN` ใน Render
   - Token ต้องเป็น Bot Token ไม่ใช่ Client Secret

3. **Bot ไม่ตอบสนอง**
   - ตรวจสอบ Bot Permissions ในเซิร์ฟเวอร์
   - ลองใช้คำสั่ง `!pinhelp` เพื่อทดสอบ

4. **Music ไม่เล่น**
   - ตรวจสอบการเชื่อมต่อ Lavalink server
   - ลองใช้คำสั่ง `!lavalink_status` เพื่อตรวจสอบ

## คำสั่งหลัก

### 🎵 คำสั่งเพลง
- `!join` - เข้าห้องเสียง
- `!leave` - ออกจากห้องเสียง
- `!play [ชื่อเพลง/URL]` - เปิดเพลงจาก YouTube
- `!stop` - หยุดเพลง
- `!pause` - หยุดชั่วคราว
- `!resume` - เล่นต่อ
- `!skip` - ข้ามเพลง

### 🤖 AI & ระบบ
- `!ai [ข้อความ]` - คุยกับ AI
- `!upgrade_ai` - ขอข้อเสนอปรับปรุงบอท

### 🏆 ระบบ XP/Rank
- `!rank [@user]` - ดู XP และ Level
- `!leaderboard` - ดูอันดับ 10 อันดับแรก
- `!addxp @user [จำนวน]` - เพิ่ม XP (ต้องมีสิทธิ์ Manage Roles)

### 👑 จัดการเซิร์ฟเวอร์
- `!giverole @user [ยศ]` - แจกยศ (ต้องมีสิทธิ์ Manage Roles)
- `!create_private [ชื่อห้อง]` - สร้างห้องส่วนตัว (ต้องมีสิทธิ์ Manage Channels)
- `!delete_private` - ลบห้องส่วนตัว
- `!announce [ข้อความ]` - ประกาศ (ต้องมีสิทธิ์ Manage Messages)

### ✨ อื่นๆ
- `!emoji [ข้อความ]` - ตกแต่งข้อความด้วย emoji
- `!pinhelp` - แสดงคู่มือใช้งาน

## ฟีเจอร์เพิ่มเติม

### ระบบ Anti-Spam
- ตรวจจับและลบข้อความซ้ำอัตโนมัติ
- แจ้งเตือนผู้ใช้เมื่อส่งข้อความซ้ำ

### ระบบ Auto XP
- ได้ 1 XP ต่อการส่งข้อความ (ไม่รวมคำสั่ง)
- Level = XP ÷ 100
- ระบบ Leaderboard แสดงอันดับผู้ใช้

### ระบบ Logging
- บันทึกการใช้คำสั่งในไฟล์ `self_improve.log`
- Log ข้อมูลสำหรับการพัฒนาบอทต่อไป

## ข้อมูลทางเทคนิค

### Dependencies
- **discord.py**: 2.3.2 (Discord API wrapper)
- **wavelink**: 2.6.3 (Music streaming library)

### Lavalink Servers
- Primary: lavalink.darrennathanael.com:2333
- Fallback: lavalink.eu.org:2333
- Secondary: lavalink.oops.wtf:443

### File Structure
```
discord-music-bot/
├── main.py              # Main bot file
├── rank.json            # User XP data
├── self_improve.log     # Command usage logs
├── runtime.txt          # Python version
├── render.yaml          # Render deployment config
└── README.md           # This documentation
```

### Environment Variables
- `DISCORD_TOKEN`: Discord Bot Token (required)
- `TOKEN`: Alternative token variable name

## การพัฒนาต่อ

บอทนี้สามารถพัฒนาต่อได้ง่าย เช่น:
- เพิ่มระบบ Economy
- ระบบ Mini-games
- Database integration
- Advanced music features (queue, playlist)
- Web dashboard

## License

MIT License - ใช้งานได้อย่างอิสระ

## Support

หากมีปัญหาการใช้งาน สามารถ:
1. ตรวจสอบ logs ใน Render Dashboard
2. ดู troubleshooting guide ด้านบน
3. สร้าง issue ใน GitHub repository

---

**หมายเหตุ**: บอทนี้ใช้ Lavalink servers ฟรี ซึ่งอาจมีข้อจำกัดด้านประสิทธิภาพ สำหรับการใช้งานจริงแนะนำให้ setup Lavalink server เอง
