---
id: AGFuvlbEKi82FbjOV2Ts4x
title: "[✓] Y-Downloads Shelf — macOS SwiftUI Menu-Bar App for Recent Downloads"
date: "2026-06-30"
importance: 3
projects: ["Y-Downloads Shelf"]
tags: ["macOS", "SwiftUI", "Menu Bar App", "Downloads", "File Management", "Productivity", "Utility"]
summary: ""
url: "https://manus.im/app/task/AGFuvlbEKi82FbjOV2Ts4x"
---

# [✓] Y-Downloads Shelf — macOS SwiftUI Menu-Bar App for Recent Downloads

| Field | Value |
|-------|-------|
| **Session ID** | `AGFuvlbEKi82FbjOV2Ts4x` |
| **Date** | 2026-06-30 21:24 UTC |
| **Project** | — |
| **URL** | [https://manus.im/app/sessions/AGFuvlbEKi82FbjOV2Ts4x](https://manus.im/app/sessions/AGFuvlbEKi82FbjOV2Ts4x) |
| **Messages** | 1 user · 2 assistant · 5 total |

## Initial Prompt

Create a minimal macOS SwiftUI menu-bar/floating-panel app called “Y-Downloads Shelf”.

Goal:
Reduce friction when moving recently downloaded files between Finder, ChatGPT, Manus, browser, and automation tools.

Core behavior:
- Monitor ~/Downloads.
- Display the 15 most recent completed files.
- Ignore partial/download temp files: .download, .crdownload, .part, .tmp.
- Show file icon, filename, extension, size, modified time.
- Floating panel accessible via menu bar and global hotkey.
- Each file row supports:
  1. Drag file to another app.
  2. Copy file URL/path to clipboard.
  3. Open file.
  4. Reveal in Finder.
  5. Quick Look preview if possible.
- Keep UI extremely minimal and fast.

Architecture:
- SwiftUI app.
- NSPanel floating window, always-on-top optional.
- FileManager scanner.
- Lightweight refresh every 2 seconds or file system watcher.
- NSPasteboard for copying file URLs and POSIX paths.
- Persist simple preferences:
  - number of files shown
  - ignored extensions
 

## First Response

**Y-Downloads Shelf** — livré. 902 lignes Swift, 11 fichiers sources, projet Xcode prêt à compiler.

---

## Contenu du zip

| Fichier | Rôle |
|---|---|
| `main.swift` | Entry point, NSApp + AppDelegate |
| `AppDelegate.swift` | Menu bar, NSPanel floating, hotkey setup |
| `PreferencesManager.swift` | UserDefaults persistence (maxFiles, ignoredExt, hotkey, position) |
| `FileItem.swift` | Modèle fichier (icon, size, date, path) |
| `DownloadsStore.swift` | FSEvents watcher + polling 2s, filtre temp files |
| `ShelfView.swift` | Panel principal : header, search bar, file list, footer |
| `FileRowView.swift` | Row : drag icon, info, 4 boutons hover, context menu complet |
| `PreferencesView.swift` | Sheet préférences |
| `HotkeyManager.swift` | Carbon `RegisterEventHotKey` — ⌘⇧Space global |
| `QuickLookHelper.swift` | `QLPreviewPanel` wrapper |
| `DragProvider.swift` | `URL: Transferable` + `NSItemProvider` |
| `Info.plist` | `LSUIElement = true`, pas de Dock icon |
| `YDownloadsShelf.

## Conversation Summary

> **User:** Create a minimal macOS SwiftUI menu-bar/floating-panel app called “Y-Downloads Shelf”.

Goal:
Reduce friction when moving recently downloaded files between Finder, ChatGPT, Manus, browser, and automation tools.

Core behavior:
- Monitor ~/Downloads.
- Display the 15 most recent completed files.
- Ignore partial/download temp files: .download, .crdownload, .part, .tmp.
- Show file icon, filename, extension, size, modified time.
- Floating panel accessible via menu bar and global hotkey.
- Each fi...

> **Manus:** **Y-Downloads Shelf** — livré. 902 lignes Swift, 11 fichiers sources, projet Xcode prêt à compiler.

---

## Contenu du zip

| Fichier | Rôle |
|---|---|
| `main.swift` | Entry point, NSApp + AppDelegate |
| `AppDelegate.swift` | Menu bar, NSPanel floating, hotkey setup |
| `PreferencesManager.swift` | UserDefaults persistence (maxFiles, ignoredExt, hotkey, position) |
| `FileItem.swift` | Modèle fichier (icon, size, date, path) |
| `DownloadsStore.swift` | FSEvents watcher + polling 2s, filtre temp files |
| `ShelfView.swift` | Panel principal : header, search bar, file list, footer |
| `FileRowView.swift` | Row : drag icon, info, 4 boutons hover, context menu complet |
| `PreferencesView.swift` | Sheet préférences |
| `HotkeyManager.swift` | Carbon `RegisterEventHotKey` — ⌘⇧Space global ...

> **Manus:** Sur ça. Je construis Y-Downloads Shelf — app SwiftUI macOS complète avec menu bar, floating panel, hotkey global, drag & drop, et file watcher. Je génère le projet Xcode complet avec tous les fichiers source.

## Full Verbatim

<details>
<summary>Expand full conversation (3 messages)</summary>

**[1782854991822] MANUS:** **Y-Downloads Shelf** — livré. 902 lignes Swift, 11 fichiers sources, projet Xcode prêt à compiler.

---

## Contenu du zip

| Fichier | Rôle |
|---|---|
| `main.swift` | Entry point, NSApp + AppDelegate |
| `AppDelegate.swift` | Menu bar, NSPanel floating, hotkey setup |
| `PreferencesManager.swift` | UserDefaults persistence (maxFiles, ignoredExt, hotkey, position) |
| `FileItem.swift` | Modèle fichier (icon, size, date, path) |
| `DownloadsStore.swift` | FSEvents watcher + polling 2s, filtre temp files |
| `ShelfView.swift` | Panel principal : header, search bar, file list, footer |
| `FileRowView.swift` | Row : drag icon, info, 4 boutons hover, context menu complet |
| `PreferencesView.swift` | Sheet préférences |
| `HotkeyManager.swift` | Carbon `RegisterEventHotKey` — ⌘⇧Space global |
| `QuickLookHelper.swift` | `QLPreviewPanel` wrapper |
| `DragProvider.swift` | `URL: Transferable` + `NSItemProvider` |
| `Info.plist` | `LSUIElement = true`, pas de Dock icon |
| `YDownloadsShelf....
**[1782854702120] MANUS:** Sur ça. Je construis Y-Downloads Shelf — app SwiftUI macOS complète avec menu bar, floating panel, hotkey global, drag & drop, et file watcher. Je génère le projet Xcode complet avec tous les fichiers source.
**[1782854697034] USER:** Create a minimal macOS SwiftUI menu-bar/floating-panel app called “Y-Downloads Shelf”.

Goal:
Reduce friction when moving recently downloaded files between Finder, ChatGPT, Manus, browser, and automation tools.

Core behavior:
- Monitor ~/Downloads.
- Display the 15 most recent completed files.
- Ignore partial/download temp files: .download, .crdownload, .part, .tmp.
- Show file icon, filename, extension, size, modified time.
- Floating panel accessible via menu bar and global hotkey.
- Each file row supports:
  1. Drag file to another app.
  2. Copy file URL/path to clipboard.
  3. Open file.
  4. Reveal in Finder.
  5. Quick Look preview if possible.
- Keep UI extremely minimal and fast.

Architecture:
- SwiftUI app.
- NSPanel floating window, always-on-top optional.
- FileManager scanner.
- Lightweight refresh every 2 seconds or file system watcher.
- NSPasteboard for copying file URLs and POSIX paths.
- Persist simple preferences:
  - number of files shown
  - ignored extensions
 ...



</details>
