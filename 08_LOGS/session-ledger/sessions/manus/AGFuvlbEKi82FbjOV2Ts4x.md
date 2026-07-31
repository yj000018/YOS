---
id: "AGFuvlbEKi82FbjOV2Ts4x"
title: "[✓] Y-Downloads Shelf — macOS SwiftUI Menu-Bar App for Recent Downloads"
date: "2026-06-30"
importance: "3"
depth_score: "substantial"
projects: ["Y-Downloads Shelf"]
tags: ["macOS", "SwiftUI", "Menu Bar App", "Downloads", "File Management", "Productivity", "Utility"]
summary: ""
executive_summary: "A macOS SwiftUI menu-bar app, 'Y-Downloads Shelf', was developed to streamline the management of recent downloads. It monitors the `~/Downloads` folder, displays the 15 most recent completed files, and offers quick actions such as drag-and-drop, copy path, open, reveal in Finder, and Quick Look. The project successfully delivered a functional application, comprising 902 lines of Swift code across 11 source files."
context_and_intent: "The intent was to create a minimal macOS SwiftUI menu-bar/floating-panel app called 'Y-Downloads Shelf' to reduce friction when managing recently downloaded files across various applications."
what_was_done: "A SwiftUI app was developed with an NSPanel floating window, accessible via a menu bar and global hotkey. It monitors `~/Downloads` for the 15 most recent completed files, ignoring temporary download files. Each file row supports drag-and-drop, copying file URL/path, opening, revealing in Finder, and Quick Look. The app uses `FileManager` for scanning, `NSPasteboard` for copying, and includes a lightweight refresh mechanism (every 2 seconds or file system watcher). Simple preferences for the number of files shown and ignored extensions are persisted."
outputs_produced: [{"description": "A functional macOS application delivered with 902 lines of Swift code across 11 source files, meeting the specified requirements for monitoring downloads and providing quick actions.", "name": "Y-Downloads Shelf", "type": "macOS SwiftUI Menu-Bar App"}]
key_decisions: ["Utilize SwiftUI for the application framework.", "Implement an NSPanel for the floating window, with an optional always-on-top feature.", "Monitor `~/Downloads` for recent files.", "Filter out partial/temporary download files (.download, .crdownload, .part, .tmp).", "Provide quick actions for each file: drag to another app, copy file URL/path, open file, reveal in Finder, Quick Look preview.", "Use `FileManager` for scanning and `NSPasteboard` for clipboard operations.", "Include persistence for user preferences like the number of files shown and ignored extensions."]
lessons_learned: {"discoveries": [], "failed_or_suboptimal": [], "worked_well": ["The project successfully delivered a functional macOS SwiftUI application as requested, including core features and architectural considerations."]}
challenges_and_blockers: ["Reducing friction when moving recently downloaded files between Finder, ChatGPT, Manus, browser, and automation tools."]
open_questions: []
next_steps: []
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