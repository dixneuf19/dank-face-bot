import asyncio
from unittest.mock import AsyncMock, MagicMock

from telegram.ext import Application

import main


def test_main_registers_handlers(monkeypatch):
    monkeypatch.setattr(main, "TELEGRAM_TOKEN", "123:abc")
    captured = {}

    def fake_run_polling(self, *a, **k):
        captured["handlers"] = self.handlers
        captured["errors"] = self.error_handlers
        captured["request"] = self.bot.request

    monkeypatch.setattr(Application, "run_polling", fake_run_polling)
    main.main()
    assert len(captured["handlers"][0]) == 4
    assert len(captured["errors"]) == 1
    # get_file and downloads use these, not the library's 5 s default
    assert captured["request"].read_timeout == main.DEFAULT_TIMEOUT


def test_dank_face_no_face(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "FIND_FACES_PIC_FOLDER", str(tmp_path))
    photo_file = MagicMock(file_id="abc")
    photo_file.download_to_drive = AsyncMock()
    size = MagicMock()
    size.get_file = AsyncMock(return_value=photo_file)
    update = MagicMock()
    update.message.photo = (size,)
    update.message.reply_photo = AsyncMock()
    res = MagicMock()
    res.json.return_value = {"status": "NO_FACE_FOUND"}
    monkeypatch.setattr(main.requests, "get", MagicMock(return_value=res))
    asyncio.run(main.dank_face(update, MagicMock()))
    photo_file.download_to_drive.assert_awaited_once()
    kwargs = update.message.reply_photo.await_args.kwargs
    assert kwargs["write_timeout"] == main.DEFAULT_TIMEOUT


def test_start():
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    asyncio.run(main.start(update, MagicMock()))
    update.message.reply_text.assert_awaited_once_with("Hi!")
