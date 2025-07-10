# Discord Music Bot (Python + wavelink)

## Overview

This is a Discord bot built with Python that provides music streaming capabilities, AI chat features, and server management tools. The bot uses wavelink for YouTube music streaming and includes various community features like XP/ranking systems, anti-spam protection, and private room creation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a single-file monolithic architecture with a simple Discord bot built using discord.py and wavelink for music functionality.

### Core Technologies
- **Language**: Python 3.10/3.11
- **Framework**: discord.py 2.3.2
- **Music Library**: wavelink 2.6.3
- **Data Storage**: JSON file-based storage
- **Deployment**: Render.com (cloud hosting)

### Architecture Pattern
- **Monolithic**: Single main.py file containing all bot logic
- **Event-driven**: Uses Discord.py's event system and command framework
- **Stateless**: No persistent database, uses JSON files for simple data storage

## Key Components

### 1. Bot Core
- **Discord Bot Client**: Main bot instance with all intents enabled
- **Command Handler**: Uses discord.py's commands extension with "!" prefix
- **Event System**: Handles Discord events like on_ready, on_message

### 2. Music System
- **Lavalink Integration**: Connects to external Lavalink servers for audio processing
- **Voice Channel Management**: Join/leave voice channels
- **Audio Streaming**: Play music from YouTube via wavelink
- **Fallback Servers**: Multiple Lavalink endpoints for reliability

### 3. User Management
- **XP/Ranking System**: JSON-based user experience tracking
- **Role Management**: Dynamic role creation and assignment
- **Anti-spam Protection**: Message filtering and user moderation

### 4. Additional Features
- **AI Chat**: Integrated AI conversation capabilities
- **Private Rooms**: Channel creation and management
- **Announcement System**: Server-wide messaging
- **Message Enhancement**: Emoji and formatting tools

## Data Flow

### Music Playback Flow
1. User issues !play command
2. Bot searches for track via wavelink
3. Connects to Lavalink server
4. Streams audio to Discord voice channel
5. Manages playback state and user interactions

### User Data Flow
1. User activity triggers XP calculation
2. Data loaded from rank.json file
3. User stats updated and saved back to file
4. Ranking displayed to users on request

### Command Processing Flow
1. Discord message received
2. Command prefix checked
3. Command parsed and routed
4. Business logic executed
5. Response sent back to Discord

## External Dependencies

### Required Services
- **Discord API**: Bot authentication and messaging
- **Lavalink Servers**: Audio processing and streaming
  - Primary: lavalink.darrennathanael.com:2333
  - Fallback: lavalink.eu.org:2333
- **YouTube**: Music source via wavelink integration

### Python Dependencies
- discord.py==2.3.2 (Discord API wrapper)
- wavelink==2.6.3 (Music streaming library)

### Environment Requirements
- **DISCORD_TOKEN**: Bot authentication token
- **TOKEN**: Alternative token variable name
- Python 3.10+ runtime

## Deployment Strategy

### Render.com Deployment
- **Platform**: Render.com web service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Runtime**: Python 3.11.9 (specified in runtime.txt)

### Local Development
- Environment variable setup for bot token
- Direct execution with `python main.py`
- Development-friendly with hot reloading capabilities

### Recent Changes (July 2025)
- ✅ **FULLY RESOLVED**: Render deployment compatibility
  - Fixed Python 3.11.9 runtime configuration
  - Resolved discord.py==2.3.2 and wavelink==2.6.3 compatibility
  - Added PyNaCl for voice support
  - Implemented HTTP health check server (port 10000)
  - Fixed yarl dependency compilation errors
  - Enhanced error handling for voice channels
  - Bot now 100% operational on Render platform

### Deployment Status
- ✅ **Discord Connection**: Fully working
- ✅ **Core Features**: All commands operational  
- ✅ **Render Compatibility**: Production ready
- ✅ **Health Checks**: HTTP endpoint active
- ✅ **Error Handling**: Comprehensive coverage

### Known Issues
- Lavalink server connectivity can be unstable (fallback servers configured)
- JSON file storage not suitable for high-concurrency scenarios
- Music features require external Lavalink servers

### Scalability Considerations
- Single-file architecture limits maintainability
- JSON storage doesn't scale beyond small user bases
- No database connections or advanced caching
- Stateless design allows for easy horizontal scaling if refactored

The bot is designed for small to medium Discord communities with basic music and management needs. The simple architecture makes it easy to deploy and maintain, but would require significant refactoring for enterprise-scale usage.