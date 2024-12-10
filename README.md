# Discord Staff System V1
Requirements:
- Mongo
- Discord.py
- A brain

To set this code up, you will need some technical skills

## First: 
Setup Mongo and import Motor (asynchronous Mongo library). Add this collection name: "staff_system"

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
- staff_force_logout @user - Forces a user to logout to prevent abuse (is owner only)
- staff_login - login to the staff system (you will have to be added)

## functions:
- @is_staff() - This is a command check, add this below `@commands.command`, etc. This will check to see if they are a staff member but does not check anything else. 
- is_admin(ctx) - Just a function, it will check to see if the user is in the admin category (checks if the user is logged in)
- is_mod(ctx) - Just a function, it will check to see if the user is in the mod category (checks if the user is logged in)
- is_support(ctx) - Just a function, it will check to see if the user is in the support category (checks if the user is logged in)

### These are the default role types:
- admin - admin, owner, core_team
- mod - mod, moderator
- support - support

## Config:
By default when you log in, you have 10 minutes to do what you need to do than it forces a logout. You can change that by going to line 58 and replacing "600" with your desired amount of seconds. If you do not want that function, comment out lines 51-71 and line 49. By default this task allows all admins to be exempt from the force logout, this way admins can stay logged in. If you want to remove this please comment out lines 59 and 60.
