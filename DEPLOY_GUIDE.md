# 🚀 Render Deployment Guide

## ปัญหาที่แก้ไขแล้ว

### ❌ ปัญหาเดิม
```
ERROR: Failed building wheel for yarl
yarl/_quoting_c.c:10870:53: error: 'PyLongObject' has no member named 'ob_digit'
```

### ✅ การแก้ไข
1. **ปรับเปลี่ยน Python version**: จาก 3.10 เป็น 3.11.9
2. **ดาวน์เกรด dependencies**:
   - discord.py: 2.3.2 (แทน 2.5.2)
   - wavelink: 2.6.3 (แทน 3.4.1)
   - yarl: 1.8.2 (แทน 1.20.1)

## 📋 ขั้นตอนการ Deploy

### 1. เตรียมโปรเจกต์
```bash
# ไฟล์ที่จำเป็น
main.py              # หลักของบอท
runtime.txt          # python-3.11.9
render.yaml          # การตั้งค่า Render
README.md           # คู่มือใช้งาน
rank.json           # ข้อมูล XP (สร้างอัตโนมัติ)
```

### 2. สร้าง Discord Bot
1. ไปที่ https://discord.com/developers/applications
2. คลิก "New Application"
3. ตั้งชื่อบอท
4. ไปที่ "Bot" tab
5. คลิก "Add Bot"
6. คัดลอก **Bot Token** (ไม่ใช่ Client Secret!)

### 3. Deploy บน Render
1. ไปที่ https://render.com
2. สร้างบัญชี/เข้าสู่ระบบ
3. คลิก "New +" → "Web Service"
4. เชื่อมต่อ GitHub repository
5. ตั้งค่า:
   - **Name**: discord-music-bot
   - **Runtime**: Python 3
   - **Build Command**: (ปล่อยว่าง)
   - **Start Command**: `python main.py`
   - **Plan**: Free

### 4. ตั้งค่า Environment Variables
ไปที่ "Environment" tab และเพิ่ม:
- **Key**: `DISCORD_TOKEN`
- **Value**: Bot Token จาก Discord Developer Portal

### 5. Deploy
1. คลิก "Create Web Service"
2. รอให้ build เสร็จ (2-5 นาที)
3. ตรวจสอบ logs ว่าขึ้น "Bot [ชื่อบอท] is ready!"

## 🔧 การแก้ไขปัญหา

### Bot ไม่ออนไลน์
- ตรวจสอบว่า DISCORD_TOKEN ถูกต้อง
- ดูใน logs ว่ามีข้อผิดพลาดอะไร
- ลองรีสตาร์ท service

### เพลงไม่เล่น
- ใช้คำสั่ง `!lavalink_status` ตรวจสอบ
- Lavalink servers อาจไม่เสถียร
- ลองใช้คำสั่ง `!play` ใหม่

### คำสั่งไม่ตอบสนอง
- ตรวจสอบ permissions ของบอทในเซิร์ฟเวอร์
- ลองใช้ `!pinhelp` ทดสอบ

## 🎯 URL เชิญบอท

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&scope=bot
```

แทนที่ `YOUR_CLIENT_ID` ด้วย Client ID จาก Discord Developer Portal

## 📊 การตรวจสอบสถานะ

### Render Dashboard
- เข้า Render Dashboard
- ดู service status
- ตรวจสอบ logs

### Discord
- ใช้คำสั่ง `!lavalink_status`
- ใช้คำสั่ง `!pinhelp` ทดสอบ

## 🆘 ปัญหาที่พบบ่อย

| ปัญหา | สาเหตุ | วิธีแก้ |
|-------|-------|---------|
| Build Failed | Python version | ใช้ 3.11.9 |
| Bot Offline | Token ผิด | ตรวจสอบ DISCORD_TOKEN |
| No Music | Lavalink ขัดข้อง | ใช้ !lavalink_status |
| No Response | Permissions | ตรวจสอบสิทธิ์บอท |

## 📞 การติดต่อ

- GitHub Issues: สำหรับปัญหาโค้ด
- Discord Server: สำหรับการใช้งาน
- Render Support: สำหรับปัญหา deployment

---

**หมายเหตุ**: การใช้งาน Render ฟরีจะมีการ sleep หลัง 15 นาทีไม่มีการใช้งาน บอทจะกลับมาออนไลน์เมื่อมีการเรียกใช้