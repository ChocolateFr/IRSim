from pyrogram import Client, filters, types
from watchdict import WatchDict
import re
wd = WatchDict('conf.json')


bot = Client('bot', wd['api_id'], wd['api_hash'], bot_token=wd['api_token'], proxy=proxy)
admins = filters.user(wd['admins'])
banned = filters.user(wd['banned'])
channels = {i:[] for i in wd['channels']}
channels_reverse = {}
nicknames ={}
for i in wd['nicknames']:
    nicknames[int(i)] = wd['nicknames'][i]
msg_partition = {}
stop = False

def get_user(nick):
    return(

            [*nicknames.keys()][
                [*nicknames.values()].index(nick)
            ]
        
    )

def set_msg(msg:types.Message):
    if msg.text:
        msg_partition[msg.text] = {}
        key = msg.text
    else:
        media = getattr(msg,msg.media.name.lower())
        if media:
            media = media.file_unique_id
        
        msg_partition[f'{media}'] = {}
        key = f"{media}"
    return key

def get_id(rep_msg, user):

    if rep_msg.text:
        return msg_partition[rep_msg.text].get(user, None)
    else:
        media = getattr(rep_msg,rep_msg.media.name.lower())
        if media:
            media = media.file_unique_id
        return msg_partition[f'{media}'].get(user, None)

def stop_filter(x,y,z):
    return stop


@bot.on_message(~admins&filters.create(stop_filter))
async def stop_handler(cl, msg):
    return

@bot.on_message(~admins&filters.command('start'))
async def start(cl, msg):
    await msg.reply('Hello! welcome to irc robot. join a channel via /join channel_name or see channels /channels')

@bot.on_message(admins&filters.regex('^/'))
async def admins_setup(cl, msg):
    global stop
    t = msg.text
    if t == '/status':
        txt = f'''🎈| bot status
🧑|- Users: {len(wd['users'])}
🔝|- Admins: {len(wd['admins'])}
🩹|- Banned: {len(wd['banned'])}
📢|- Channels: {len(wd['channels'])}
{','.join([i for i in wd['channels']])}
'''
        await msg.reply(txt)
    elif t.startswith('/admin '):
        nick = t.replace('/admin ', '')
        nick = get_user(nick)
        
        if nick not in admins:
            admins.add(nick)
            wd['admins'].append(nick)
            await msg.reply(f'User {nick} added to admin list.')
            await bot.send_message(nick,f'You promoted to admin.')
    elif t.startswith('/dem '):
        nick = t.replace('/dem ', '')
        nick = get_user(nick)
        if nick in admins:
            admins.add(nick)
            wd['admins'].remove(nick)
            await msg.reply(f'User {nick} removed from admin list.')
            await bot.send_message(nick,f'You demoted to member.')

    elif t == '/backup':
        await bot.send_document(msg.from_user.id, 'conf.json')
    
    elif t.startswith('/ban '):
        try:
            t = t.replace('/ban ', '')
            t = get_user(t)
            if t not in wd['users']:
                return await msg.reply(f'User {t} is not a bot user.')
            wd['banned'].append(t)
            await msg.reply(f'User {t} added to ban list.')
            await bot.send_message(t,f'Sorry, admin banned you from the robot.')
        except ValueError:
            await msg.reply(f'User id {t} is incorrect.')
    
    elif t.startswith('/unban '):
        try:
            t = t.replace('/unban ', '')
            t = get_user(t)
            if t not in wd['banned']:
                return await msg.reply(f'User {t} is not a banned user.')
            wd['banned'].remove(t)
            banned.remove(t)
            await bot.send_message(t,f'Yay, admin unbanned you!')
        except ValueError:
            await msg.reply(f'User id {t} is incorrect.')
    
    elif t.startswith('/add '):
        t = t.replace('/add ', '')
        if t in wd['channels']:
            return await msg.reply(f'Channel {t} is already added.')
        
        wd['channels'].append(t)
        await msg.reply(f'Channel {t} added successfully.')
    
    elif t.startswith('/del '):
        t = t.replace('/del ', '')
        if t not in wd['channels']:
            return await msg.reply(f'{t} is not a channel')
        
        wd['channels'].remove(t)
        await msg.reply(f'Channel {t} removed successfully.')
        for user in channels[t]:
            try:
                await bot.send_message(user, f'channel {t} is removed by admin.')
            except:
                pass
    elif t == '/stop':
        stop = not stop
        await msg.reply(f'Bot stopped: {stop}')
    elif t.startswith('/join '):
        t = t.replace('/join ', '')
        if t in wd['channels']:
            
            channels[t].append(msg.from_user.id)
            channels_reverse[msg.from_user.id] = t
            return await msg.reply(f'Listening to channel {t}')
        await msg.reply(f'Channel {t} doesn\'t exists.')

    elif t.startswith('/nick '):
        t = t.replace('/nick ', '')
        if not re.match('^[a-zA-Z0-9]+$', t):
            await msg.reply( f'Nickname should only contain a-z and numbers.')
        elif t.lower() == 'admin':
            await msg.reply( f'Fuck off you\'re not admin.')
        elif t in nicknames.values():
            await msg.reply( f'This nickname already exists.')
        else:
            nicknames[msg.from_user.id] = t
            wd['nicknames'] = nicknames
            await msg.reply(f'Now you\'re {t}')

@bot.on_message(filters.regex('^/'))
async def user_command(cl, msg):
    nickname = nicknames.get(msg.from_user.id)
    channel = channels_reverse.get(msg.from_user.id, 'main')
    
    if msg.from_user.id not in wd['users']:
        wd['users'].append(msg.from_user.id)
    t = msg.text
    if t == '/users':
        await msg.reply(f'There is {len(channels[channel])} people in channel {channel}.')
    elif t == '/me':
        await msg.reply(f'You are {nickname} and you\'re in channel {channel}.')
    elif t.startswith('/join '):
        if not nickname:
            await msg.reply('You should set your nickname first by using /nick nickname')
            return
        t = t.replace('/join ', '')
        if t in wd['channels']:
            channels[t].append(msg.from_user.id)
            channels_reverse[msg.from_user.id] = t
            await msg.reply(f'Listening to channel {t}')
            
            for i in channels[t]:
                if i != msg.from_user.id:
                    await bot.send_message(i, f'__User {nickname} joined the channel.__')
        else:
            await msg.reply(f'Channel {t} doesn\'t exists.')
    elif t.startswith('/nick '):
        t = t.replace('/nick ', '')
        if not re.match('^[a-zA-Z0-9]+$', t):
            await msg.reply( f'Nickname should only contain a-z and numbers.')
        elif t.lower() == 'admin':
            await msg.reply( f'Fuck off you\'re not admin.')
        elif t in nicknames.values():
            await msg.reply( f'This nickname already exists.')
        else:
            nicknames[msg.from_user.id] = t
            wd['nicknames'] = nicknames
            await msg.reply(f'Now you\'re {t}')
    
    elif t == '/channels':
        await msg.reply('\n'.join([f'{i} ({len(channels[i])} users)' for i in wd['channels']]))



@bot.on_message()
async def users(cl, msg:types.Message):
    if msg.from_user.id in wd['banned']:
        return
    channel = channels_reverse.get(msg.from_user.id, 'main')
    if msg.text and len(msg.text) > 500:
        await msg.reply_text('You can\t send message bigger than 500 chars.')
    elif msg.caption and len(msg.caption) > 500:
        await msg.reply_text('You can\t send message bigger than 500 chars.')

    if msg.from_user.id in nicknames:
        if msg.text:
            msg.text = nicknames[msg.from_user.id]+' says:\n'+msg.text
        else:
            msg.caption = f"{nicknames[msg.from_user.id]} says:\n{msg.caption if msg.caption else ''}"
    if msg.from_user.id not in nicknames:
        await msg.reply('You should set your nickname first by using /nick nickname')
        return
    key = set_msg(msg)
    for i in channels[channel]:
        if i != msg.from_user.id and i not in wd['admins']:
            rep = None
            if msg.reply_to_message_id:
                rep = get_id(msg.reply_to_message, i)
            
   
            new_m = await msg.copy(i, reply_to_message_id=rep)
            msg_partition[key][i] = new_m.id
        elif i == msg.from_user.id:
            msg_partition[key][i] = msg.id

    for i in wd['admins']:
        channel1 = channels_reverse.get(i, 'main')
        if channel == channel1:
            if i != msg.from_user.id:
                new_m = await msg.copy(i)
                msg_partition[key][i] = new_m.id
            else:
                msg_partition[key][i] = msg.id
        else:
            if msg.text:
                msg.text = f'in channel {channel}\n'+msg.text
            else:
                msg.caption = f'in channel {channel}\n'+msg.caption
            if i != msg.from_user.id:
                new_m = await msg.copy(i)
                msg_partition[key][i] = new_m.id
            else:
                msg_partition[key][i] = msg.id

        


            




    
    
    



bot.run()
