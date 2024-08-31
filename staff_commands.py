import discord
from discord.ext import commands, tasks
import time
from utils.constants import staff_system

def is_staff():
    async def predicate(ctx: commands.Context):
        members = ctx.bot.staff_members
        for member in members:
            if member['user_id'] == ctx.author.id:
                return True
            
        return False
    return commands.check(predicate)

async def is_staff_admin(ctx: commands.Context):
    members = ctx.bot.staff_members
    admin_roles = ['owner', 'admin', 'core_team']
    for member in members:
        if ctx.author.id == member['user_id']:
            if member['role'].lower() in admin_roles and member['logged_in']:
                return True

    return False

async def is_staff_mod(ctx: commands.Context):
    members = ctx.bot.staff_members
    mod_roles = ['mod', 'moderator', 'owner', 'admin', 'core_team']
    for member in members:
        if ctx.author.id == member['user_id']:
            if member['role'].lower() in mod_roles and member['logged_in']:
                return True

    return False

async def is_staff_support(ctx: commands.Context):
    members = ctx.bot.staff_members
    support_roles = ['support', 'owner', 'admin', 'core_team']
    for member in members:
        if ctx.author.id == member['user_id']:
            if member['role'].lower() in support_roles and member['logged_in']:
                return True

    return False

class staff_system_file(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_staff_logins.start()

    @tasks.loop(minutes=1)
    async def check_staff_logins(self):
        current_time = round(time.time())
        users = staff_system.find()
        admin_roles = ['owner', 'admin', 'core_team']

        async for user in users:
            if user['logged_in'] and int(current_time) - int(user['logged_in_time']) >= 600:
                if user['role'] in admin_roles:
                    pass
                
                await staff_system.update_one({'user_id': user['user_id']}, {'$set': {'logged_in': False, 'logged_in_time': None}})

                for member_doc in self.bot.staff_members:
                    if member_doc['user_id'] == user['user_id']:
                        member_doc['logged_in'] = False
                        member_doc['logged_in_time'] = None
                        break

                member = await self.bot.fetch_user(user['user_id'])
                await member.send('You are now signed out!')

    
    @commands.command(description="This command you will be able to create a login (is owner only)")
    @commands.is_owner()
    async def staff_create(self, ctx: commands.Context, member: discord.User, role: str):
        user = await staff_system.find_one({'user_id': member.id})

        if user:
            return await ctx.send(f"**{member.name}** is already added as a staff member")
        
        staff_doc = {
            'user_id': member.id,
            'role': role,
            'logged_in': False,
            'logged_in_time': None,
        }
        await staff_system.insert_one(staff_doc)

        member_doc = {
                'user_id': member.id,
                'role': role,
                'logged_in': False
            }
        self.bot.staff_members.append(member_doc)
        await ctx.send(f'**{member.name}** has been successfully created!')


    @commands.command(description="This command will remove a login (is owner only)")
    @commands.is_owner()
    async def staff_remove(self, ctx: commands.Context, member: discord.User):
        user = await staff_system.find_one({'user_id': member.id})

        if not user:
            return await ctx.send(f"I cannot find any records with the username: **{member.name}**")
        
        await staff_system.delete_one({'user_id': member.id})
        self.bot.staff_members.remove(member.id)
        await ctx.send(f'**{member.name}** has been successfully removed!')

    @commands.command(description="This command will force the user to log out (is owner only)")
    @commands.is_owner()
    async def staff_force_logout(self, ctx: commands.Context, member: discord.User):
        user = await staff_system.find_one({'user_id': member.id})
        if not user:
            return await ctx.send(f"I cannot find any records with the username: **{member.name}**")
        elif not user['logged_in']:
            return await ctx.send(f'**{member.name}** is currently not logged in!')
        
        await staff_system.update_one({'user_id': member.id}, {'$set': {'logged_in': False, 'logged_in_time': None}})
        
        for member_doc in self.bot.staff_members:
            if member_doc['user_id'] == member.id:
                member_doc['logged_in'] = False
                break
        
        member = await self.bot.fetch_user(user['user_id'])
        await ctx.send(f'**{member.name}** is now logged out!')
        await member.send(f'You have forced logged out of your session!')


    @commands.command(description="This command will allow users to login to the system")
    @is_staff()
    async def staff_login(self, ctx: commands.Context):
        user = await staff_system.find_one({'user_id': ctx.author.id})
        if not user:
            return False
        elif user['logged_in']:
            return await ctx.send(f'**{ctx.author.name}** is already currently logged in!')
        await staff_system.update_one({'user_id': ctx.author.id}, {'$set': {'logged_in': True, 'logged_in_time': int(round(time.time()))}})
        for member_doc in self.bot.staff_members:
            if member_doc['user_id'] == ctx.author.id:
                member_doc['logged_in'] = True
                break
        await ctx.author.send('You are now logged in!')


async def setup(bot):
    await bot.add_cog(staff_system_file(bot))
