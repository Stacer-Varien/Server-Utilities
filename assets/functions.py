from datetime import *
import os
from nextcord import Embed, Member, TextChannel

from assets.not_allowed import no_invites, no_pings
from config import db


def check_illegal_invites(message, channel: int):
    if 'discord.gg' in message:
        if channel in no_invites:
            return True
        else:
            return False

def check_illegal_mentions(message, channel: int):
    pings = ['@everyone', '@here']
    if any(word in message for word in pings):
        if channel in no_pings:
            return (True)
        else:
            return (False)

def give_adwarn_auto(channel:TextChannel, member: int, moderator: int, warn_id: int, appeal_id:int):
    data = db.execute("SELECT * FROM bankData WHERE user_id = ?", (member,)).fetchone()
    current_time = datetime.now()
    next_warn = current_time + timedelta(hours=1)

    reason = f"Incorrectly advertising in {channel.mention}"
    if data == None:
        db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (member, moderator, reason, warn_id, appeal_id,))

        db.execute("INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                       (member, 1, round(next_warn.timestamp())))
        return True

    elif data[2] < round(current_time.timestamp()):
        db.execute("UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?", (1, round(next_warn.timestamp()), member,))
        db.commit()
        return True
    else:
        return False


def give_adwarn(channel, member: int, moderator: int, reason: str, warn_id:int, appeal_id:int):
    data = db.execute("SELECT * FROM bankData WHERE user_id = ?", (member,)).fetchone()
    current_time = datetime.now()
    next_warn = current_time + timedelta(hours=1)
    if data == None:
        db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (member, moderator, '{} - {}'.format(channel, reason), warn_id, appeal_id,))

        db.execute("INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                       (member, 1, next_warn))
        return True

    elif data[2] < round(current_time.timestamp()):
        db.execute("UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?", (1, round(next_warn.timestamp()), member,))
        db.commit()
        return True
    else:
        return False
                


def get_warn_points(member: int) -> int:
    try:
        warnpointdata = db.execute(
            "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member,)).fetchone()
        db.commit()
        return warnpointdata[0]
    except:
        return 1


def get_warn_id(member: int):
    data = db.execute("SELECT warn_id FROM warnData WHERE user_id = ?", (member,)).fetchone()
    return data[0]


def set_results(member: int):
    warn_point = get_warn_points(member)

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


def send_adwarn(member: Member, reason: str):
    warnpointdata = db.execute("SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (member.id,))
    warn_point = int(warnpointdata.fetchone()[0])

    warn_id = get_warn_id(member.id)

    result = set_results(member.id)

    embed = Embed(
        title="You have been warned", color=0xFF0000)
    embed.add_field(
        name="Reason of warn", value=reason, inline=True)
    embed.add_field(name="Warn ID", value=warn_id, inline=True)
    embed.add_field(name="Warn Points", value=warn_point, inline=True)
    embed.add_field(name="Result", value=result, inline=False)
    embed.set_footer(text="If you feel this warn was a mistake, please use `/appeal WARN_ID`")
    embed.set_thumbnail(url=member.display_avatar)


def strike_staff(department: str, member: int, strike_id: int, appeal_id: int):
    db.execute("INSERT OR IGNORE INTO strikeData (department, user_id, strike_id, appeal_id) VALUES (?,?,?,?)",
               (department, member, strike_id, appeal_id,))
    db.commit()


def get_strikes(department: str, member: int):
    data = db.execute("SELECT * FROM strikeData WHERE department = ? AND user_id = ?", (department, member,))

    try:
        return data.fetchall()
    except:
        return 0


def check_strike_id(strike_id: int, department: str):
    data = db.execute("SELECT * FROM strikeData WHERE strike_id = ? AND department = ?",
                      (strike_id, department,)).fetchone()

    if data == None:
        return None
    else:
        return data


def revoke_strike(department: str, strike_id: int):
    db.execute("DELETE FROM strikeData WHERE strike_id = ? AND department = ?", (strike_id, department))
    db.commit()


def get_appeal_id(strike_id: int, department: str):
    data = db.execute("SELECT appeal_id FROM strikeData WHERE strike_id = ? AND department = ?",
                      (strike_id, department)).fetchone()
    db.commit()
    return data[0]


def fetch_striked_staff(appeal_id: int, department: str):
    data = db.execute("SELECT * FROM strikeData WHERE appeal_id = ? AND department = ?",
                      (appeal_id, department,)).fetchone()
    db.commit()

    if data == None:
        return None
    else:
        return data


def add_partnership_request(user: int, server: int):
    db.execute("INSERT OR IGNORE INTO partnerData (user_id, guild_id) VALUES (?,?)",
               (user, server,))
    db.commit()


def get_partnership_request(user: int, server: int):
    data = db.execute("SELECT * FROM partnerData WHERE user_id = ? and guild_id = ?", (user, server,)).fetchone()
    db.commit()
    return data


def remove_partnership_request(user: int, server: int):
    db.execute("DELETE FROM partnerData WHERE WHERE user_id = ? and guild_id = ?", (user, server,))
    db.commit()

def check_partnership(server:int, user:int)->bool:
    if server == 740584420645535775:
        path="/partnerships/orleans/{}.txt".format(user)
        check=os.path.exists(path)
    
    elif server == 925790259160166460:
        path = "/partnerships/hazeads/{}.txt".format(user)
        check = os.path.exists(path)
    
    return check

def add_verification_request(user:int):
    db.execute("INSERT OR IGNORE INTO verificationData (user) VALUES (?)", (user,))
    db.commit()

def check_verification_request(user:int) -> (int|None):
    a=db.execute("SELECT user FROM verificatioData WHERE user=?", (user,)).fetchone()
    db.commit()
    if a==None:
        return None
    else:
        return a[0]
