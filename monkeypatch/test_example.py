# from unittest import mock
import pytest
import example as foo

def test_caller_to_power(monkeypatch):
    def mock_power(a, b):
        return 999
    monkeypatch.setattr(foo, "power", mock_power)
    result = foo.caller_to_power(2, 8)
    assert result == "Result: 999"

def test_class_response(monkeypatch):
    def mock_time(self, url):
        return 111
    monkeypatch.setattr(foo.FooBarBaz, "get_elapsed_time", mock_time)
    asdf = foo.FooBarBaz()
    durtime = asdf.get_elapsed_time("http://localhost")
    assert durtime == 111