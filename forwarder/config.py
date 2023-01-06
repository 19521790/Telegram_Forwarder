from forwarder.sample_config import Config

class Development(Config):
    API_KEY = "5727416332:AAFY-yxFtLf1T0jGUyt4aLHfVUVqF0BizDQ"  # Your bot API key
    OWNER_ID = 2111357106  # Your user id
 
    FROM_CHATS = [-1001473494312]  # List of chat id's to forward messages from.
    TO_CHATS = [-1001735866288]  # List of chat id's to forward messages to.

    REMOVE_TAG = True
    WORKERS = 4
