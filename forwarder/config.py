from forwarder.sample_config import Config

class Development(Config):
    API_KEY = "5505684344:AAE98Odd40aqZiIAi8CtmtDUcfjdqxaompk"  # Your bot API key
    OWNER_ID = 2111357106  # Your user id
    # Make sure to include the '-' sign in group and channel ids.
    FROM_CHATS = [-741539747]  # List of chat id's to forward messages from.
    TO_CHATS = [-743101910]  # List of chat id's to forward messages to.

    REMOVE_TAG = True
    WORKERS = 4
