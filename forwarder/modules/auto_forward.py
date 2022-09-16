from typing import Union

from telegram import Message, MessageId
from telegram.ext import CallbackContext, Filters, MessageHandler
from telegram.error import ChatMigrated
from telegram.update import Update

from forwarder import FROM_CHATS, LOGGER, REMOVE_TAG, TO_CHATS, dispatcher
import sqlite3


def send_message(message: Message, chat_id: int, reply_to=None) -> Union[MessageId, Message]:
    return message.copy(chat_id=chat_id, reply_to_message_id=reply_to)


def forward(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat

    if not message or not chat:
        return
    from_chat_name = chat.title or chat.first_name

    for chat in TO_CHATS:
        to_chat_name = (

                context.bot.get_chat(chat).title or context.bot.get_chat(chat).first_name
        )

        try:
            connection = sqlite3.connect("replyForwardId.db")
            cursor = connection.cursor()

            source_id = message.chat.id
            destination_id = chat
            source_reply_id = message.message_id
            reply_message_id_from_des = None
            try:
                reply_message_id_from_source = message.reply_to_message.message_id
            except:
                reply_message_id_from_source = None

            if reply_message_id_from_source:
                cursor.execute(
                    "Select des_message_id from replyId where source_id= ? and des_id=? and source_message_id =?",
                    (source_id, destination_id, reply_message_id_from_source))
                reply_message_id_from_des = cursor.fetchone()

                if reply_message_id_from_des:
                    destination_rely_id = send_message(message, chat, reply_message_id_from_des[0]).message_id
                else:
                    destination_rely_id = send_message(message, chat).message_id
            else:
                destination_rely_id = send_message(message, chat).message_id

            cursor.execute(
                "insert into replyId (source_id, des_id, source_message_id, des_message_id) values (?,?,?,?)",
                (source_id, destination_id, source_reply_id, destination_rely_id))

            cursor.execute("Select count(0) from replyId")

            if cursor.fetchone()[0] > 1000:
                cursor.execute("delete from replyId where id in (SELECT id FROM replyId ORDER BY id ASC LIMIT 500)")

            connection.commit()

            connection.close()


        except ChatMigrated as err:
            send_message(message, err.new_chat_id)
            LOGGER.warning(f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!")
        except:
            LOGGER.exception(
                'Error while forwarding message from chat "{}" to chat "{}".'.format(
                    from_chat_name, to_chat_name
                )
            )


# create table
connection = sqlite3.connect("replyForwardId.db")
cursor = connection.cursor()
cursor.execute(
    "create table if not exists replyId (id integer primary key,source_id integer, des_id integer, source_message_id integer, des_message_id integer)")

connection.close()

try:
    FORWARD_HANDLER = MessageHandler(
        Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
        forward,
        run_async=True,
    )

    dispatcher.add_handler(FORWARD_HANDLER)
    # dispatcher.add_handler(FORWARD_HANDLER_2)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")
