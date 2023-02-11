from datetime import *
import os
from discord import *

from assets.not_allowed import no_invites, no_pings
from config import db

class Appeal():
    def __init__(self, appeal_id:int):
        self.user=user
        self.appeal_id=appeal_id
    
    def check_appeal(self):
        data=db.execute("SELECT * FROM warnData WHERE appeal_id = ?", (self.appeal_id,)).fetchone()
        if data==None:
            return None
        else:
            return data
    
    def remove_warn(self, member_id:int):
        db.execute("DELETE FROM warnData WHERE appeal_id = ?", (self.appeal_id,))
        db.execute("UPDATE warnDATA_v2 SET warn_point = warn_point - ? where user_id = ?", (1, member_id,))
        db.commit()


class Warn():
    def __init__(self, user: Member, moderator:Member, warn_id: int=None) -> None:
        self.user = user
        self.moderator=moderator
        self.warn_id = warn_id

    def check_warn(self):
        data=db.execute("SELECT * FROM warnDATA WHERE user_id = ? AND warn_id = ?", (self.user.id, self.warn_id,)).fetchone()
        db.commit()

        if data == None:
            return None

        else:
            data=db.execute("SELECT * FROM warnDATA WHERE user_id = ?", (self.user.id,))
            db.commit()
            return data


    def give_adwarn_auto(self, channel: TextChannel, appeal_id: int):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ?", (self.user.id,)).fetchone()
        data2 = db.execute(
            "SELECT * FROM warnData_v2 WHERE user_id= ?", (self.user.id,)).fetchone()
        db.commit()
        current_time = datetime.now()
        next_warn = current_time + timedelta(hours=1)

        reason = f"Incorrectly advertising in {channel.mention}"
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (self.user.id, self.moderator.id, reason, self.warn_id, appeal_id,))

            db.execute("INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                    (self.user.id, 1, round(next_warn.timestamp())),)
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute("UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?",
                    (1, round(next_warn.timestamp()), self.user.id,))
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False


    def give_adwarn(self, channel: TextChannel, reason: str, appeal_id: int):
        data = db.execute(
            "SELECT * FROM warnData WHERE user_id = ?", (member,)).fetchone()
        data2 = db.execute(
            "SELECT * FROM warnData_v2 WHERE user_id= ?", (member,)).fetchone()
        db.commit()
        current_time = datetime.now()
        next_warn = current_time + timedelta(hours=1)
        if data == None:
            db.execute(
                "INSERT OR IGNORE INTO warnData (user_id, moderator_id, reason, warn_id, appeal_id) VALUES (?,?,?,?,?)",
                (self.user.id, self.moderator.id, '{} - {}'.format(channel.mention, reason), self.warn_id, appeal_id,))

            db.execute("INSERT OR IGNORE INTO warnData_v2 (user_id, warn_point, time) VALUES (?,?,?)",
                    (member, 1, round(next_warn.timestamp())))
            db.commit()

        elif int(data2[2]) < round(current_time.timestamp()):
            db.execute("UPDATE warnDatav2 SET warn_point = warn_point + ? AND time = ? WHERE user_id= ?",
                    (1, round(next_warn.timestamp()), self.user.id,))
            db.commit()

        elif int(data2[2]) > round(current_time.timestamp()):
            return False


    def get_warn_points(self) -> int:
        try:
            warnpointdata = db.execute(
                "SELECT warn_point FROM warnData_v2 WHERE user_id = ?", (self.user.id,)).fetchone()
            db.commit()
            return warnpointdata[0]
        except:
            return 1


    def get_warn_id(self):
        data = db.execute(
            "SELECT warn_id FROM warnData WHERE user_id = ?", (self.user.id,)).fetchone()
        return data[0]
          

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
            return True
        else:
            return False




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

class Partner():
    def __init__(self, user:Member, server:Guild):
        self.user=user
        self.server=server

    def check(self):
        if self.server.id == 740584420645535775:
            path="/partnerships/orleans/{}.txt".format(self.user.id)
            check=os.path.exists(path)
            if check == True:
                return True
            else:
                return None    
        
        elif self.server.id == 925790259160166460:
            path = "/partnerships/hazeads/{}.txt".format(self.user.id)
            check = os.path.exists(path)
            if check == True:
                return True
            else:
                return None

    def approve(self):
        with open("partnerships/orleans/{}.txt".format(self.user.id), 'r') as f:
            content = "".join(f.readlines())
        os.remove("partnerships/orleans/{}.txt".format(self.user.id))
        return content

    def deny(self):
        with open("partnerships/orleans/{}.txt".format(self.user.id), 'r') as f:
            content = "".join(f.readlines())
        os.remove("partnerships/orleans/{}.txt".format(self.user.id))
        return content
    
    

def add_verification_request(user:int):
    db.execute("INSERT OR IGNORE INTO verificationData (user) VALUES (?)", (user,))
    db.commit()

def check_verification_request(user:int):
    a=db.execute("SELECT user FROM verificatioData WHERE user=?", (user,)).fetchone()
    db.commit()
    if a==None:
        return False
    else:
        return a[0]

def check_loa_breaks():
    data = db.execute(
        "SELECT * FROM breakData WHERE accepted = ?", (1,)).fetchall()
    db.commit()
    return data

def remove_loa_break(member:Member):
    db.execute("DELETE FROM breakData WHERE user_id = ?", (member.id,))
    db.commit()

def check_plans(server:int):
    data = db.execute(
            "SELECT * FROM planData where server_id = ?", (server,)).fetchall()
    db.commit()
    return data

def remove_plan(plan_id:int, server:int):
    db.execute(
        'DELETE FROM planData WHERE plan_id= ? AND server_id= ?', (plan_id, server,))
    db.commit()

def add_break_request(user:User, server:int, break_id:int, duration:str, reason:str, accepted:int, start:int, ends:int):
    db.execute("INSERT OR IGNORE INTO breakData (user_id, guild_id, break_id, duration, reason, accepted, start, ends) VALUES (?,?,?,?,?,?,?,?)", (user.id, server, break_id, duration, reason, accepted, start, ends,))
    db.commit()

def fetch_break_id(break_id:int, server:int):
    data = db.execute("SELECT * FROM breakData WHERE break_id = ? AND guild_id = ?",
                      (break_id, server,)).fetchone()
    if data == None:
        return None
    else:
        return data

def approve_break(member:User, server:int, start:int, ends:int):
        db.execute("UPDATE breakData SET accepted = ? WHERE user_id = ? and guild_id = ?",
                           (1, member.id, server,))
        db.execute("UPDATE breakData SET start = ? WHERE user_id = ? and guild_id = ?",
                           (start, member.id, server,))
        db.execute("UPDATE breakData SET ends = ? WHERE user_id = ? and guild_id = ?",
                           (ends, member.id, server,))
        db.commit()

def deny_break(break_id:int, server:int):
    db.execute("DELETE FROM breakData WHERE break_id = ? and guild_id = ?", (break_id, server,))
    db.commit()

def end_break(member:User, server:int):
    db.execute("DELETE FROM breakData WHERE user_id = ? and guild_id = ?", (member.id, server,))
    db.commit()

def resign_apply(user:User):
    db.execute(
            "INSERT OR IGNORE INTO resignData (user_id, accepted) VALUES (?, ?)", (user.id, 0))
    db.commit()

def check_resign(member:User):
    data = db.execute(
        "SELECT * FROM resignData WHERE user_id = ?", (member.id,)).fetchone()
    db.commit()
    
    if data==None:
        return None
    else:
        return data

def approve_resign(member:User):
    db.execute("UPDATE resignData SET accepted = ? WHERE user_id = ?", (1, member.id,))
    db.commit()


def deny_resign(member: User):
    db.execute(
        "DELETE FROM resignData WHERE WHERE user_id = ?", (member.id,))
    db.commit()


def add_plan(user:User, until:int, plan:str, claimee:User, plan_id, server:int):
    db.execute(
        "INSERT OR IGNORE INTO planData (user_id, started, until, plans, set_by, plan_id, server_id) VALUES (?,?,?,?,?,?,?)",
        (user.id, round(datetime.now().timestamp()), until, plan, claimee.id, plan_id, server,))
    db.commit()

def get_plan(plan_id:int, server:int):
    data = db.execute(
        "SELECT * FROM planData WHERE plan_id = ? AND server_id = ?", (plan_id, server,)).fetchone()
    
    if data == None:
        return None
    else:
        return data

    
