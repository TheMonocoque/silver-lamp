""" Testing Sandbox """
import gxring

#//////////////////////////////////////////////////////////////////////////////
def setup():
    pass

def teardown():
    print("Closing time")

def setup_method():
    pass

def teardown_method():
    pass
#//////////////////////////////////////////////////////////////////////////////

def test_basic(mocker):
    """ Test out mocking an imported library function """
    mocker.patch(
        'gxring.keyz.produce',
        return_value="hello there"
    )
    result = gxring.basic_test()
    assert result == "hello thereaaa"

def test_arg_run(mocker, caplog):
    """ test arg run mock """
    mocker.patch(
        'gxring.keyz.produce',
        return_value="hello there"
    )
    mocker.patch(
        'nacl.encoding.Base64Encoder.encode',
        return_value=b'Gasldjfoiawerlkadsjf123412')
    caplog.set_level(gxring.logging.INFO)
    result, key = gxring.arg_run('hello there')
    assert result == 'Gasldjfoiawerlkadsjf123412'
    assert key == 'hello there'
    assert "Running gxring" in caplog.text
