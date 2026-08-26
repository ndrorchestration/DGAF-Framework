# DGAF Drive Sync Policy

> **Canonical cross-platform and cloud storage sync specification for the ndrorchestration ecosystem.**  
> Maintained by: **Agent COLLEEN** (continuity, archive) + **Agent Amethyst** (conductor)  
> Status: ✅ Active — Session 019 2026-05-01  
> Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)

---

## Architecture Overview

Hub-and-spoke model: **Google Drive as canonical storage control plane** across all devices.
Device-local state is treated as ephemeral working memory; Drive is the source of truth.

```
┌─────────────────────────────────────────────────────┐
│              Google Drive (Canonical)               │
│  My Drive/                                          │
│  ├── 00-Inbox/           (cross-device drop zone)  │
│  ├── 01-Projects/        (active portable assets)  │
│  ├── 02-Knowledge/       (reference docs / PDFs)   │
│  ├── 03-Shared/          (team / collab artifacts) │
│  └── 90-Archive/         (cold storage, old proj)  │
└──────────┬──────────────────────┬───────────────────┘
           │                      │
  ┌────────▼───────┐    ┌─────────▼──────────┐
  │  Windows PC    │    │     macOS Machine   │
  │  Stream mode   │    │  Stream mode        │
  │  Active folders│    │  Active folders     │
  │  offline-pinned│    │  offline-pinned     │
  └────────────────┘    └────────────────────┘
           │                      │
  ┌────────▼───────┐    ┌─────────▼──────────┐
  │  Android Phone │    │    iPhone           │
  │  Google Photos │    │  Google Photos      │
  │  Camera/SS/Exp │    │  Drive app backup   │
  └────────────────┘    └────────────────────┘
```

---

## Desktop Sync Policy

### Client

- **Google Drive for Desktop** on Windows and macOS
- Set My Drive to **Stream files** (default)
- Right-click only critical active folders → mark **Available offline**

### macOS-Specific

- Grant Privacy & Security full disk access for Drive helper
- Verify Apple File Provider behavior on macOS 12.1+ (some stream/mirror mode interactions vary)
- Do not use Finder integration for repos — GitHub Desktop or CLI handles git; Drive handles docs only

### Exclusion Rules

The following MUST be excluded from Drive sync (local-only):

```
.git/
node_modules/
.venv/
venv/
__pycache__/
build/
dist/
.gradle/
*.pyc
*.class
*.tmp
*.log
.DS_Store
Thumbs.db
```

Place a `.gdriveignore` (or configure Drive's ignore list) to block these paths.

---

## Mobile Sync Policy

| Device | Media Backup | Doc Backup | Selected Folders |
|--------|-------------|-----------|------------------|
| Android | Google Photos (auto) | Google Drive | Camera, Screenshots, Exports |
| iPhone | Google Photos (auto) | Google Drive app backup | Camera Roll, Screenshots |

- Media backup runs on Wi-Fi only by default — confirm setting on each device
- Drive document sync is for exported files (PDFs, markdown, reports), not app-internal data

---

## External Drive Policy

| Use Case | Sync to Drive? | Notes |
|----------|---------------|-------|
| Archives / old project tarballs | ✅ Recommended | Sync to `90-Archive/` |
| Media libraries (photos, audio) | ✅ Recommended | Sync to `03-Shared/media/` or `02-Knowledge/` |
| Large reference corpora | ✅ Optional | Mark offline only on primary workstation |
| node_modules / build artifacts | ❌ Never | Exclude at all times |
| VM disk images | ❌ Never | Binary blobs cause extreme churn |
| Active dev repos | ❌ Never | Git manages these; Drive adds no value |

**Reconnect behavior:** When an external drive is disconnected, sync pauses for that folder tree.
Do not use removable drives as the primary live workspace for high-churn dev folders — reconnect
timing and rescan latency degrades sync reliability at scale.

---

## Conflict Control Rules

1. **Single-writer rule** — only one device actively edits a hot folder at a time
2. **Stable folder names** — renaming folders causes full rescan and bandwidth spike; batch renames offline
3. **No cross-mount edits** — do not open Drive-synced files in a second app simultaneously on two devices
4. **Version history** — enable 30-day version history on all critical folders via Drive settings
5. **Conflict files** — if Drive creates `filename (conflicted copy).ext`, resolve within 24h; never leave as-is

---

## Sync Policy JSON Manifest

```json
{
  "google_drive_sync_blueprint": {
    "version": "1.0",
    "last_updated": "2026-05-01",
    "canonical_store": {
      "platform": "Google Drive",
      "folders": {
        "00-Inbox": "cross-device drop zone",
        "01-Projects": "active portable project docs and assets",
        "02-Knowledge": "reference docs, PDFs, notes, architecture",
        "03-Shared": "team/shared artifacts",
        "90-Archive": "cold storage, old projects"
      }
    },
    "desktop_policy": {
      "windows": { "client": "Google Drive for Desktop", "mode": "stream_files", "offline_rule": "mark only active folders offline" },
      "macos": { "client": "Google Drive for Desktop", "mode": "stream_files", "requirements": ["grant Privacy & Security permissions", "verify File Provider on macOS 12.1+"] }
    },
    "mobile_policy": {
      "android": { "media_backup": "Google Photos", "selected_folders": ["Camera", "Screenshots", "Exports"] },
      "iphone": { "media_backup": "Google Photos", "device_backup": "Google Drive app backup" }
    },
    "external_drive_policy": {
      "allowed": true,
      "best_for": ["archives", "media libraries", "large static datasets"],
      "avoid_for": ["node_modules", "temp files", "VM images", "high-churn dev folders"]
    },
    "conflict_controls": {
      "single_writer_rule": "one device edits a hot folder at a time",
      "naming_rule": "stable folder names across devices",
      "exclusions": [".git", "cache", "tmp", ".venv", "build", "dist", "node_modules"]
    }
  }
}
```

---

## Quick Verify Protocol

1. Create `01-Projects/sync-test.md` on Desktop A
2. Confirm it appears on Desktop B in Drive (stream mode, ~30s)
3. Mark it offline on one machine, disconnect network, reopen locally
4. Pass condition: same file path cross-platform, edits converge without duplicates, mobile backup independent of doc sync

---

## GAP-06 Status

`GAP-06 — Drive ↔ GitHub sync register: ✅ CLOSED Session 004`

This policy extends GAP-06 with a full operational spec (Track A — Session 019).

---

*Policy authority: Agent COLLEEN. Conductor authorization: Agent Amethyst / Njineer ([@ndrorchestration](https://github.com/ndrorchestration))*
