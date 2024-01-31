import pytest
import multiprocessing
import time

def server_process():
    from guidance import models, Server

    mistral = models.Mock()

    server = Server(mistral, api_key="SDFSDF")
    server.run(port=8392)

@pytest.fixture
def running_server():
    p = multiprocessing.Process(target=server_process)
    p.start()
    time.sleep(10)
    yield p
    p.terminate()

def test_remote_mock_gen(running_server):
    from guidance import models, gen

    m = models.Mock("http://localhost:8392", api_key="SDFSDF")
    m2 = m + "A story." + gen("test", max_tokens=20)
    assert len(str(m2)) > 20, "The model didn't generate enough data"