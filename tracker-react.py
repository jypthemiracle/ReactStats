# Bot to track reactions in a discord server 
# Counts only reacts in the channel it is triggered in
# Displays a user leaderboard of top 10 users to receive that reaction
# Works with Python 3.5.4
import discord
import json
from collections import OrderedDict


TOKEN = 'OTU0NjA0MTU1NTMwNTM0OTg0.YjViZg.bF6xlKWyflqj1c0nYPiHx9DadP4'

client = discord.Client()

async def get_logs(channel):
    print("Getting logs from "+ str(channel.name))
    msg_list = await channel.history(limit=100000).flatten()
    
    print( "Read " + str(len(msg_list)) + " messages")
    return msg_list

async def count_reacts(emoji, msg_list):
    new_dict = {}
    for m in msg_list:
         if (not m.author.bot):
             for react in m.reactions:
                if(react.emoji == emoji):
                    if (m.author.id in new_dict.keys()):
                        if(react.count>0 and (emoji=='💊' or emoji == '😭' or emoji=='✍' or emoji=='💯' or emoji=='w' or emoji=='💉')):
                           new_dict[m.author.id]["count"] = new_dict[m.author.id]["count"] + (react.count - 1)
                        else:
                            new_dict[m.author.id]["count"] = new_dict[m.author.id]["count"] + react.count
                    else:
                        new_dict[m.author.id] = { 
                            "member" : m.author,
                            "count" : react.count
                        }
    return new_dict

async def get_leaders(emoji, member_dict, channel, member_list):
    mem_count = 1
    s = "These are the top 10 users with " + emoji + " reacts on #" + str(channel) + '\n'

    sorted_d = sorted(member_dict.keys(), key = lambda x:(member_dict[x]['count']), reverse=True)
    for key in sorted_d:
        s = s + str(mem_count) + ". " + str(member_dict[key]["member"]) + " : " + str(member_dict[key]["count"]) + '\n'
        mem_count = mem_count + 1
        if (mem_count>=11):
            break
    s = s + "========================================== \n"
    return s

async def hello(author):
    return "Hello " + author.mention

async def help(author): # Modify based on commands added

    return """
    This bot helps track the top 10 users with specific emoji reacts on their posts in this channel.

    Usage - !stats <command>,<command2>,<command3>,...

    valid commands - win, loss, joy, syringe, pensive, 100, ok, help, hello, star
    """

@client.event
async def on_message(message):
    print("message: ", message.content)
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return
    if (message.content.startswith('!stats ')):
        print("YES, we are in.")
        val = message.content[7:] #get command name from message
            
        if(val == 'help' or val =='hello'):
            msg = await globals()[val](message.author)  
        else:
            flag = 0
            emoji_dict = {
                "win" : "🇼",
                "loss" : "🇱",
                "syringe" : "💉" ,
                "pensive" : "😔",
                "joy" : "😂",
                "100" : "💯",
                "ok" : "👌",
                "eggplant" : "🍆",
                "peach" : "🍑",
                "write": "✍",
                "sob" : "😭",
                "tomato" : "🍅",
                "star" : "⭐",
                "pill": "💊"
            }

            try:
                val_list = val.split(",")
            except: 
                flag = 1

            if not("pill" in emoji_dict.keys()):
                flag = 1
            
            if (flag == 0):
                member_list = message.channel.guild.members
                msg = ""
                channel = client.get_guild(927446583337951332).get_channel(940208552285442108)
                print("channel", channel)
                msg_list = await get_logs(channel) #replace with channel you want to track 

                member_dict = await count_reacts(emoji_dict['pill'], msg_list)

                if (len(member_dict.keys())):
                    msg = msg + await get_leaders(emoji_dict['pill'], member_dict, channel, member_list)
                else:
                    msg = 'no stats'
            else:
                msg = "Invalid Command List. Try again."
                    
        
        if not(msg is None):
            print("SUCCESS")
            await message.channel.send(msg)
            
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)

