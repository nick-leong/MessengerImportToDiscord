# MessengerImportToDiscord
Takes JSON data from Facebook Messenger and roughly inserts it into a Discord Channel.

## Requirements

Python 3+ (This was written with a 3.8 environment)

Discord API by Rapptz:

  https://github.com/Rapptz/discord.py
  
  https://discordpy.readthedocs.io/en/latest/index.html

## How to run
Create constant.py file with following format:
```
TOKEN=<YOUR_TOKEN_HERE>
json_dir=<LOCATION_OF_MESSENGER_JSONS_HERE>
mapping_location='MAPPING_OF_USERS_CSV_FILE'
channel_id=<ID_OF_INSERT_TO_TEXT_CHANNEL>
```
#### Note: The mapping location key is referring to a csv of the following format:
```
Name, ID
<Person's Name as it appears in Messenger Data>, <Associated Discord_ID>
```
#### Any person without a Discord_ID should have the ID field contain Undefined, or just not be included in the mapping.

### Command to run:
```python app.py```

## Explanation of what this does and why I did it
So what I did was I took raw exported messenger data requested from Facebook, and just loaded them in one at a time, in descending naming order, because the lowest numbered file had the earliest data, which means I had to iterate through the files in that order. EG) 3,2,1. Then in each file, I reversed the list that contained all the message sub-JSON objects. This is because Facebook must have delivered the data going from most recent to latest when it extracted and served you the data files.

For each sub-JSON object, I grabbed the sender's name and cross referenced it with a map of the Name(key) -> Discord UserID(value). If the person had a defined Discord UserID, I incorporated that into the message that would be sent. Then I took the timestamp that the message was sent, and manipulated it. I needed to change the format because it was stored in Unix epoch time. I took a epoch time converter and fed in the long value to get a strftime format. I took that format and made a string based on time stamp formatter.

Once I had the details about the who sent, and when it was sent, I took the content and fed it through a regex to identify any weird byte code characters. I encoded those parts into utf8 so we can get emojis and random characters in the message. After this, I checked if the length of the total content was greater than 2000 characters. The insertion is limited to 2000 characters per post, so I had to chunk them up into multiple parts and insert them individually as a continued post.

I added all the data to a list and kept adding to that list until the total character would exceed 2000 characters. Right before it reaches this 2000 character limit, I tell the Discord bot client to post the message. Any lingering messages that occur in my list after the last message in the file is added, is then added at the end of it's file iteration.

Anything that is a gif, photo, sticker, video is disregarded because the data was not there.

That's pretty much it
