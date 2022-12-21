import asyncio
from telethon.sync import TelegramClient
from telethon.types import InputMediaDice
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, GetHistoryRequest
from json import loads, dumps


def load_sessions():
    with open("active_sessions.json") as file:
        data = loads(file.read())
        return data


def join_public_channel(client, invite_link):
    channel = client.get_entity(invite_link)
    client(JoinChannelRequest(channel))


def join_private_channel(client, invite_link):
    client(ImportChatInviteRequest(invite_link.split("+")[1]))


def leave_public_channel(client, invite_link):
    channel = client.get_entity(invite_link)
    client(LeaveChannelRequest(channel))


def leave_private_channel(client, invite_link):
    channel = client.get_entity(invite_link)
    client.delete_dialog(channel)


def join_and_comment_post(client, post_link, message):
    channel = client.get_entity(post_link.split("/")[3])
    message_id = int(post_link.split("/")[4])
    client(JoinChannelRequest(channel))
    posts = client(GetHistoryRequest(
        peer=channel,
        limit=999999,
        offset_date=None,
        offset_id=0,
        max_id=message_id + 1,
        min_id=message_id - 1,
        add_offset=0,
        hash=0))
    post = posts.messages[0]
    client.send_message(entity=channel, message=message, comment_to=post)


def add_account(api_id, api_hash, done_template):
    with TelegramClient(StringSession(), api_id, api_hash) as client:
        string_session = client.session.save()
        client_data = client.get_me()
        username = "@" + client_data.username
        data_dict = {"USERNAME": username,
                     "API_ID": api_id,
                     "API_HASH": api_hash,
                     "ID_SESSION": string_session,
                     "isActive": True,
                     "doneTemplate": done_template}
        with open("active_sessions.json", "r") as file:
            data_loaded = loads(file.read())
            data_loaded.append(data_dict)
        with open("active_sessions.json", "w") as file:
            file.write(dumps(data_loaded, sort_keys=True, indent=4))


def delete_account(string_session):
    with open("active_sessions.json", "r") as file:
        data_loaded = loads(file.read())
    for session in data_loaded:
        if session["ID_SESSION"] == string_session:
            data_loaded.remove(session)
    with open("active_sessions.json", "w") as file:
        file.write(dumps(data_loaded, sort_keys=True, indent=4))


async def join_and_send_sticker(client, post_link, sticker, stickers_count, interval):
    await client.connect()
    channel = await client.get_entity(post_link.split("/")[3])
    message_id = int(post_link.split("/")[4])
    await client(JoinChannelRequest(channel))
    posts = await client(GetHistoryRequest(
        peer=channel,
        limit=999999,
        offset_date=None,
        offset_id=0,
        max_id=message_id + 1,
        min_id=message_id - 1,
        add_offset=0,
        hash=0))
    post = posts.messages[0]
    for i in range(stickers_count):
        await client.send_file(entity=channel, file=InputMediaDice(sticker), comment_to=post)
        await asyncio.sleep(interval)


async def join_and_comment_post_async(client, post_link, message):
    await client.connect()
    channel = await client.get_entity(post_link.split("/")[3])
    message_id = int(post_link.split("/")[4])
    await client(JoinChannelRequest(channel))
    posts = await client(GetHistoryRequest(
        peer=channel,
        limit=999999,
        offset_date=None,
        offset_id=0,
        max_id=message_id + 1,
        min_id=message_id - 1,
        add_offset=0,
        hash=0))
    post = posts.messages[0]
    await client.send_message(entity=channel, message=message, comment_to=post)


async def gather_loop(tasks):
    await asyncio.gather(*tasks)
