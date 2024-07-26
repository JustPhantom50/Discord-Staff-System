# Discord Staff System V1
Requirement:
- Mongo
- Discord.py
- A brain

To set this code up, you will need some technical skills

## First: 
Setup Mongo and import Motor (asynchronous Mongo library). add this collection name: "staff_system"

## Second: 
Put this code into your on_ready function, all this does is create a cached variable of the staff members for the bot to use:
```
self.bot.staff_members = []

async for record in db.staff_system.find({"user_id": {"$exists": True}}):
    member_doc = {
        'user_id': record['user_id'],
        'role': record['role'],
        'logged_in': record['logged_in']
    }
    self.bot.staff_members.append(member_doc)
```

## Third:
Import the file on this git hub repo, it's a cog file. Please replace "from utils.constants import db" with the proper path for the db connection. If you put it in the file, you do not have to import it. 

## Commands:
- staff_create @user role - Creates a staff member with a corresponding role (is owner only)
- staff_remove @user - Removes a staff member from the system (is owner only)
- staff_force_logout @user - Forces a user logout to prevent abuse (is owner only)
- staff_login - login to the staff system (you will have to be added)

## functions:
- @is_staff() - its a command check so @ it right after the command call. will check to see if you are a staff member
- is_admin(ctx) - just a function, that will check to see if you are an admin
- is_mod(ctx) - just a function, that will check to see if you are a mod
- is_support(ctx) - just a function, that will check to see if you are a support member

### roles types are as follows but can be changed:
- admin - admin, owner, core_team
- mod - mod, moderator
- support - support

## Config:
By default when you log in, you have 10 minutes to do what you need to do then it forces a logout. you can change that by going to line 54 and replacing "600" with your desired amount of seconds. If you do not want that function, comment out lines 48-63 and line 46
