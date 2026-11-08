import main


def test_handlers_are_defined():
    for handler in (main.start, main.help, main.honk, main.dank_face, main.main):
        assert callable(handler)
