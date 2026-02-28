# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Your Setup

### 🔍 Tavily Search

- **Location:** `/home/admin/.openclaw/workspace/skills/tavily-search/`
- **API Key:** Pre-configured (tvly-dev-2w8T5D-...)
- **Usage:** `node tavily.js "query" [max_results]`
- **Docs:** See `skills/tavily-search/README.md`

### 📈 Tushare Stock API

- **Location:** `/home/admin/.openclaw/workspace/skills/tushare/`
- **Token:** `828abf5aa2217e5f0d0ab35b0e57f0441149775885cdd7ec7588bac36c04`
- **API URL:** `http://lianghua.nanyangqiankun.top`
- **Usage:** `python3 tushare_api.py daily <ts_code> [start] [end]`
- **Docs:** See `skills/tushare/README.md`

### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

---

Add whatever helps you do your job. This is your cheat sheet.
