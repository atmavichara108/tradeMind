#!/usr/bin/env python3
"""Хвост чата «🧶Препарыночная🪢»: последние N сообщений (текст+id+автор).

tg-read.py требует TRADEMIND_GROUP_ID в env-файле; менять глобальный env
в зоне агента нельзя — читаем хвост напрямую сессией Maya (только чтение).
Запуск: python3 09_Meta/tools/read_chat_tail.py [N]
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.local/bin"))
import tg_profile  # noqa: E402

ENV = os.path.expanduser("~/.config/portal-tg/tg.env")
SESSION = os.path.expanduser("~/.local/state/portal-tg/portal.session")
GROUP = int(os.environ.get("TRADEMIND_GROUP_ID")
            or tg_profile.PROFILES["trademind"]["group_default"])
WORK = "/tmp/opencode/tmfresh"


async def main(n):
    env = tg_profile.load_env(ENV)
    proxy = tg_profile.parse_proxy(env.get("TG_PROXY", ""))
    from telethon import TelegramClient
    client = TelegramClient(WORK, int(env["TG_API_ID"]), env["TG_API_HASH"],
                            proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        print("сессия не авторизована"); return
    async for m in client.iter_messages(GROUP, limit=n):
        who = m.sender.username if getattr(m.sender, "username", None) else str(m.sender_id)
        media = " [photo]" if m.photo else (" [doc]" if m.document else "")
        txt = (m.text or "").replace("\n", " ⏎ ")
        print(f"id={m.id} {m.date:%d.%m %H:%M} {who}: {txt}{media}")
    await client.disconnect()

asyncio.run(main(int(sys.argv[1]) if len(sys.argv) > 1 else 20))
