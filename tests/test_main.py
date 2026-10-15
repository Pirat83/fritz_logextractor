import pytest

from fritzlogextractor import __version__
from fritzlogextractor.__main__ import main


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == __version__


def test_version_comes_from_the_installed_distribution():
    from importlib.metadata import version

    assert __version__ == version("fritz-logextractor")


def test_bad_config_exits_1(monkeypatch):
    monkeypatch.delenv("FRITZ_USERNAME", raising=False)
    monkeypatch.delenv("FRITZ_PASSWORD", raising=False)
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 1


def test_valid_config_reports_not_implemented(caplog):
    with pytest.raises(SystemExit) as exc:
        main(["--config", "tests/conffiles/validconfig.yaml"])
    assert exc.value.code == 2
    assert "Configured 2 device(s), polling every 30s" in caplog.text
