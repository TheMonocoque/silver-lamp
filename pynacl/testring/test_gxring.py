""" Testing Sandbox """
import pytest
import gxring

#//////////////////////////////////////////////////////////////////////////////
# Setups and Teardowns
#------------------------------------------------------------------------------
def setup():
    pass

def teardown():
    print("Closing time")

def setup_method():
    pass

def teardown_method():
    pass
#//////////////////////////////////////////////////////////////////////////////
# Fixtures
#------------------------------------------------------------------------------

#//////////////////////////////////////////////////////////////////////////////
# Tests
#------------------------------------------------------------------------------
def test_basic(mocker):
    """ Test out mocking an imported library function """
    mocker.patch(
        'gxring.keyz.produce',
        return_value="hello there"
    )
    result = gxring.basic_test()
    assert result == "hello thereaaa"

#@pytest.mark.timeout(10) # need to install pytest-timeout to use this
@pytest.mark.fast # custom markers need to be added to project pytest.ini
#@pytest.mark.xfail(reason='Well not really') # mark things that are expected to fail until fixed
#@pytest.mark.skip(reason="No infra resource") # skip because it is not implemented yet
@pytest.mark.parametrize('test_value, test_files',
                         [('hello there', ['tmux3']),
                          ('1234', ['tmux3']),
                          ('x66', ['tmux32', 'tmux3'])
                          ])
def test_arg_run(mocker, caplog, test_value, test_files):
    """ test arg run mock """
    mocker.patch(
        'gxring.keyz.produce',
        return_value="hello there"
    )
    mocker.patch(
        'nacl.encoding.Base64Encoder.encode',
        return_value=b'Gasldjfoiawerlkadsjf123412')
    caplog.set_level(gxring.logging.INFO)
    mocker.patch('os.listdir').return_value = test_files
    result, key = gxring.arg_run(test_value)
    assert result == 'Gasldjfoiawerlkadsjf123412'
    assert key == 'hello there'
    assert "Running gxring" in caplog.text

def test_dvide_by_zero():
    """ Quick Exception pytest example """
    with pytest.raises(ZeroDivisionError) as excinfo:
        gxring.divide(7,0)
    assert str(excinfo.value) == "No dividing by zero!"

def test_arg_run_max_limit_exception(mocker,caplog):
    mocker.patch(
        'gxring.keyz.produce',
        return_value="hello there"
    )
    mocker.patch(
        'nacl.encoding.Base64Encoder.encode',
        return_value=b'Zasldjfoiawerlkadsjf123412')
    caplog.set_level(gxring.logging.INFO)
    mocker.patch('os.listdir').return_value = ['one', 'two']
    with pytest.raises(RuntimeError) as excpinfo:
        result, key = gxring.arg_run('test_value')
    assert "Running gxring" in caplog.text
    assert str(excpinfo.value) == "Out of luck with retries"