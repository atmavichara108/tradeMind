#!/usr/bin/env python3
"""Достать пропавшие вложения чата «🧶Препарыночная🪢» по message id.

Сторож (trademind-tg-guard) пишет только filename+sha256 — файлы на диск
не сохраняются (задокументированный дефект канала). Скрипт читает те же id
напрямую через Maya-сессию (только чтение чата, никакой отправки) и
складывает медиа в папку вольта.

Запуск:
    python3 09_Meta/tools/fetch_chat_media.py [ИД ...]
Без аргументов — список id из guard-journal с type=file.
"""
import asyncio
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.expanduser("~/.local/bin"))
import tg_profile  # noqa: E402

ENV = os.path.expanduser("~/.config/portal-tg/tg.env")
SESSION = os.path.expanduser("~/.local/state/portal-tg/portal.session")
STATE = os.path.expanduser("~/.local/state/trademind-tg/guard-journal.jsonl")
GROUP = int(os.environ.get("TRADEMIND_GROUP_ID")
            or tg_profile.PROFILES["trademind"]["group_default"])
OUTDIR = os.path.expanduser("~/Projects/TradingMind/02_Mentor/Import_2026-11-05")
# рабочая копия сессии — чтобы не тянуть sqlite-замок живого сторожа
WORK_SESSION = "/tmp/opencode/tmfresh"


def journal_file_ids():
    ids = []
    with open(STATE, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("type") == "file" and r.get("id"):
                ids.append(int(r["id"]))
    return sorted(set(ids))


async def main(ids):
    env = tg_profile.load_env(ENV)
    proxy = tg_profile.parse_proxy(env.get("TG_PROXY", ""))
    from telethon import TelegramClient
    os.makedirs(OUTDIR, exist_ok=True)
    # консистентная копия sqlite-сессии (мокрый cp даёт неавторизованную БД)
    os.makedirs(os.path.dirname(WORK_SESSION), exist_ok=True)
    if not os.path.exists(WORK_SESSION + ".session"):
        import sqlite3
        src = sqlite3.connect(SESSION)
        dst = sqlite3.connect(WORK_SESSION + ".session")
        src.backup(dst)
        dst.close(); src.close()
    client = TelegramClient(WORK_SESSION, int(env["TG_API_ID"]), env["TG_API_HASH"],
                            proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        print("сессия не авторизована — останов")
        return
    got, missing = [], []
    for mid in ids:
        m = await client.get_messages(GROUP, ids=mid)
        if m is None:
            missing.append((mid, "not found"))
            print(f"id={mid}: не найдено")
            continue
        if not (m.photo or m.document):
            missing.append((mid, "no media"))
            print(f"id={mid}: нет медиа (text: {str(m.text)[:50]!r})")
            continue
        ts = m.date.strftime("%Y-%m-%d_%H-%M-%S")
        path = await m.download_media(file=os.path.join(OUTDIR, f"image_{ts}"))
        if path:
            got.append((mid, path))
            print(f"id={mid}: -> {os.path.basename(path)} "
                  f"({os.path.getsize(path)} bytes)")
        else:
            missing.append((mid, "download empty"))
    await client.disconnect()
    print(f"ИТОГ: скачано {len(got)}, недоступно {len(missing)} {missing}")

if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:] if a.isdigit()]
    asyncio.run(main(args or journal_file_ids()))
