# from unittest import mock
import pytest
import example as foo
import datetime

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

def test_fedex_two_day():
    start = datetime.date(2022,1,28) # Friday
    end = start + datetime.timedelta(days=5)   # Wednesday
    expected = 3 # 2 day ship not including itself
    result = foo.fc_shipment(start, end)
    assert result == expected

@pytest.mark.parametrize("start,end,expected",[
    (datetime.date(2022,1, 28), datetime.date(2022, 2, 2), 3),
    (datetime.date(2022,1, 29), datetime.date(2022, 2, 3), 3),
    (datetime.date(2022,1, 1), datetime.date(2022, 2, 28), 40)
])
def test_fc_shipment_delayed(start, end, expected):
    result = foo.fc_shipment(start, end)
    assert result == expected

# tmpfile and directories
CONTENT = "Example from pytest.org"
def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
#--------------------------------------------------------------------------------------------------
# @pytest.fixture(scope="session")
# def vmdk_obj(tmp_path_fact):
#     vmdk = foo.create_expensive_disk()
#     fn = tmp_path_fact.mktemp("data") / "core.vmdk"
#     vmdk.save(fn)
#     return fn
# def test_validate_vmdk(vmdk_obj):
#     disk = load_vmdk(vmdk_obj)
#     # test disk