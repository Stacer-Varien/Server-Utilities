from random import randint
from assets.not_allowed import no_invites, no_pings
from config import db
from nextcord import Embed, Member


def check_illegal_invites(message, channel:int):
    if 'discord.gg' in message:
        if channel in no_invites:
            return(True)
        else:
            return(False)

def check_illegal_mentions(message, channel:int):
    pings=['@everyone', '@here']
    if any(word in message for word in pings):
        if channel in no_pings:
            return (True)
        else:
            return (False)


        
def give_adwarn(channel, member:int, moderator:int):
    warn_id = f"{randint(0,100000)}"
    appeal_id = f"{randint(0,100000)}"

    reason = f"Incorrectly advertising in {channel}"

    cursor1 = db.execute("INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)", (member, moderator, reason, warn_id, appeal_id,))

    cursor2 = db.execute("INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point) VALUES (?,?)", (member, 1))

    if cursor1.rowcount == 0:
        db.execute("UPDATE warnData SET moderator_id = ?, reason = ?, appeal_id = ? AND warn_id = ? WHERE user_id= ?", (moderator, reason, appeal_id, warn_id,))
    db.commit()

    if cursor2.rowcount == 0:
        db.execute("UPDATE warnData_v2 SET warn_point = warn_point + ? WHERE user_id = ?", (1, member,))
    db.commit()

def get_warn_points(member:int):
    warnpointdata = db.execute(
        "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member,)).fetchone()
    db.commit()
    return warnpointdata[0]

def get_warn_id(member:int):
    data=db.execute("SELECT warn_id FROM warnData WHERE user_id = ?", (member,)).fetchone()
    return data[0]

def set_results(member:int):
    warn_point=get_warn_points(member)

    if warn_point < 3:
        result = "No action taken yet"
        return result
    
    elif warn_point == 3:
        result = "Member has reached the 3 warn point punishment. A 2 hour mute punishment was applied"
        return result

    elif warn_point == 6:
        result = "Member has reached the 6 warn point punishment. A kick punishment was applied"
        return result
    elif warn_point == 10:
        result = "Member has reached the 10 warn point punishment. A ban punishment was applied"
        return result

       

def send_adwarn(member:Member, reason:str):
    warnpointdata = db.execute("SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member.id,))
    warn_point = int(warnpointdata.fetchone()[0])

    warn_id=get_warn_id(member.id)

    result=set_results(member.id)

    embed = Embed(
        title="You have been warned", color=0xFF0000)
    embed.add_field(
        name="Reason of warn", value=reason, inline=True)
    embed.add_field(name="Warn ID", value=warn_id, inline=True)
    embed.add_field(name="Warn Points", value=warn_point, inline=True)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_footer(text="If you feel this warn was a mistake, please use `/appeal WARN_ID`")
    embed.set_thumbnail(url=member.display_avatar)

def strike_staff(department:str, member:int, strike_id:int, appeal_id:int):
    
    db.execute("INSERT OR IGNORE INTO strikeData (department, user_id, strike_id, appeal_id) VALUES (?,?,?,?)", (department, member, strike_id, appeal_id,))
    db.commit()


def get_strikes(department: str, member: int):
    data=db.execute("SELECT * FROM strikeData WHERE department = ? AND user_id = ?", (department, member,))

    try:
        return data.fetchall()
    except:
        return 0

def check_strike_id(strike_id:int, department:str):
    data= db.execute("SELECT * FROM strikeData WHERE strike_id = ? AND department = ?", (strike_id, department,)).fetchone()

    if data == None:
        return None
    else:
        return data

def revoke_strike(department:str, strike_id:int):
    db.execute("DELETE FROM strikeData WHERE strike_id = ? AND department = ?", (strike_id, department))
    db.commit()

def get_appeal_id(strike_id:int, department:str):
    data = db.execute("SELECT appeal_id FROM strikeData WHERE strike_id = ? AND department = ?", (strike_id, department)).fetchone()
    db.commit()
    return data[0]

def fetch_striked_staff(appeal_id:int, department:str):
    data=db.execute("SELECT * FROM strikeData WHERE appeal_id = ? AND department = ?", (appeal_id, department,)).fetchone()
    db.commit()

    if data == None:
        return None
    else:
        return data

def add_partnership_request(user:int, ad, proof, server:int):
    db.execute("INSERT OR IGNORE INTO partnerData (user_id, ad, proof, guild_id) VALUES (?,?,?,?)", (user, ad, proof, server,))
    db.commit()

def get_partnership_request(user:int, server:int):
    data = db.execute("SELECT * FROM partnerData WHERE user_id = ? and guild_id = ?", (user, server,))
    db.commit()
    return data.fetchone()

def remove_partnership_request(user:int, server:int):
    db.execute("DELETE FROM partnerData WHERE WHERE user_id = ? and guild_id = ?", (user, server,))
    db.commit()









