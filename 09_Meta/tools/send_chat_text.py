#!/usr/bin/env python3
"""Текст в чат «🧶Препарыночная🪢» с reply (chat_scope, без topic).

Обходной путь для дефекта tg-send.py в chat_scope: Telethon этой сборки
не принимает message_thread_id=None при reply. Профиль trademind:
получатель жёстко group_default, переопределения нет; --dry-run без сети.
Запуск: python3 send_chat_text.py [--dry-run] [--reply-to ID] ТЕКСТ...
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.local/bin"))
import tg_profile  # noqa: E402

ENV = os.path.expanduser("~/.config/portal-tg/tg.env")
GROUP = int(os.environ.get("TRADEMIND_GROUP_ID")
            or tg_profile.PROFILES["trademind"]["group_default"])
WORK = "/tmp/opencode/tmfresh"


async def send(text, reply_to, dry):
    if dry:
        print(f"DRY-RUN chat={GROUP} reply_to={reply_to}\n{text}")
        return
    env = tg_profile.load_env(ENV)
    proxy = tg_profile.parse_proxy(env.get("TG_PROXY", ""))
    from telethon import TelegramClient
    client = TelegramClient(WORK, int(env["TG_API_ID"]), env["TG_API_HASH"],
                            proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("сессия не авторизована — останов")
    m = await client.send_message(GROUP, text, reply_to=reply_to)
    print(f"ОТПРАВЛЕНО: message_id={m.id}")
    await client.disconnect()


if __name__ == "__main__":
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    if dry:
        argv.remove("--dry-run")
    reply_to = None
    if "--reply-to" in argv:
        i = argv.index("--reply-to")
        reply_to = int(argv[i + 1])
        del argv[i:i + 2]
    if not argv:
        sys.exit(__doc__)
    asyncio.run(send(" ".join(argv), reply_to, dry))
