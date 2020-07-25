#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import json
import os
import re
import time
from constant import TOKEN
from constant import json_dir
from constant import mapping_location
from constant import channel_id

raw_list_jsons = [x for x in os.listdir(json_dir)]
json_files = sorted(raw_list_jsons, reverse=True)

names_map = {}

with open(mapping_location) as name_mapping_file:
    for line in name_mapping_file:
        curr_line = line.strip().split(",")
        if curr_line[1] != 'Undefined':
            names_map[curr_line[0]] = curr_line[1]

class InsertClient(discord.Client):

    async def send_msg(self, message):
        await self.get_channel(channel_id).send(message)
    
def chunk_message(message):
    pointer = 0
    messages = list(message[0+i:1950+i] for i in range(0, len(message), 1950))
    for i in range(0, len(messages)):
        if i == 0:
            messages[i] = messages[i]+"..."
        elif i == len(messages)-1:
            messages[i] = "..."+messages[i]
        else:
            messages[i] = "..."+messages[i]+"..."
    return messages


client = InsertClient()

@client.event
async def on_ready():
    for file in json_files:
        with open(json_dir+file, 'r') as json_file:
            j = json.load(json_file)
            messages = j["messages"][::-1]
            message_queue = []
            for item in messages:

                to_send = "**[{}] {} :**\n{}"
                to_send_content = ""
                if 'content' in item:
                    to_send_content = re.sub(r'[\xc2-\xf4][\x80-\xbf]+',lambda m: m.group(0).encode('latin1').decode('utf8'), item['content'])
                elif 'gifs' in item:
                    to_send_content = "```<GIF NOT FOUND>```"
                elif 'photos' in item:
                    to_send_content = "```<PHOTO NOT FOUND>```"
                elif 'sticker' in item:
                    to_send_content = "```<STICKER NOT FOUND>```"
                elif 'videos' in item:
                    to_send_content = "```<VIDEO NOT FOUND>```"
                else:
                    to_send_content = "```<CONTENT NOT AVAILABLE>```"

                sender = item["sender_name"]
                if item["sender_name"] in names_map:
                    sender = '<@' + names_map[item["sender_name"]] + '>' + ' aka __' + item["sender_name"] + '__'

                to_add = to_send.format(
                    time.strftime('%m/%d/%Y - %H:%M:%S',  time.gmtime(item["timestamp_ms"]/1000.)),
                    sender,
                    to_send_content)

                if len(to_add) > 2000:
                    for chunk in chunk_message(to_add):
                        await client.send_msg(chunk)
                    continue

                elif len("\n\n".join(message_queue)) + 4 + len(to_add) >= 2000:
                    await client.send_msg("\n\n".join(message_queue))
                    message_queue = []

                message_queue.append(
                    to_send.format(
                    time.strftime('%m/%d/%Y - %H:%M:%S',  time.gmtime(item["timestamp_ms"]/1000.)),
                    sender,
                    to_send_content))

            if len(message_queue) > 0:
                await client.send_msg("\n\n".join(message_queue))
                    
    await client.close()


client.run(TOKEN)
