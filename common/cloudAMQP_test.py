from cloudAMQP_client import CloudAMPQClient

CLOUDAMPQ_URL = "amqp://jkqxpdhr:AVmZ8yaiOODH1CJqJTlA8EIpPq_d83GF@donkey.rmq.cloudamqp.com/jkqxpdhr"

TEST_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMPQClient(CLOUDAMPQ_URL, TEST_QUEUE_NAME)
    sentMsg = {"test" : "demo"}
    client.sendMessage(sentMsg)
    client.sleep(10)
    recivedMsg = client.getMessage();
    assert recivedMsg == sentMsg

if __name__ == '__main__':
    test_basic()
