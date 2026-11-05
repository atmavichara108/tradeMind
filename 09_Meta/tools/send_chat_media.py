#!/usr/bin/env python3
"""Отправить изображение-разметку в чат «🧶Препарыночная🪢» с подписью и reply.

tg-upload.py заточен под topic-33 (SSA) и для chat_scope не годится.
Здесь — тот же профиль trademind: получатель жёстко group_default,
переопределения нет; --dry-run ничего не отправляет.
Запуск: python3 09_Meta/tools/send_chat_media.py [--dry-run] [--reply-to ID] FILE [ПОДПИСЬ]
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


def usage():
    sys.exit(__doc__)


async def send(path, caption, reply_to, dry):
    env = tg_profile.load_env(ENV)
    proxy = tg_profile.parse_proxy(env.get("TG_PROXY", ""))
    from telethon import TelegramClient
    if not os.path.isfile(path):
        sys.exit(f"файла нет: {path}")
    if dry:
        print(f"DRY-RUN: chat={GROUP} reply_to={reply_to} file={path} "
              f"({os.path.getsize(path)} bytes)\ncaption: {caption!r}")
        return
    client = TelegramClient(WORK, int(env["TG_API_ID"]), env["TG_API_HASH"],
                            proxy=proxy)
    await client.connect()
    if not await client.is_user_authorized():
        sys.exit("сессия не авторизована — останов")
    m = await client.send_file(GROUP, path, caption=caption,
                               reply_to=reply_to)
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
        if i + 1 >= len(argv):
            usage()
        reply_to = int(argv[i + 1])
        del argv[i:i + 2]
    if not argv:
        usage()
    path = argv[0]
    caption = " ".join(argv[1:]) or None
    asyncio.run(send(path, caption, reply_to, dry))
