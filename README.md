# Server Utilities

Server Utilities is a custom Discord bot for Orleans and Varien's Homework
Folder. It provides message moderation, reaction roles, a starboard, bot status
commands, and an experimental verification workflow.

## Setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and set `DISCORD_TOKEN`.
5. Enable the **Server Members Intent** and **Message Content Intent** for the bot
   in the Discord Developer Portal.
6. Run the bot:

   ```powershell
   python server_utilities.py
   ```

The SQLite database and its required tables are created automatically on first
run. Server, role, and channel IDs are currently configured in the Python
modules.

## Checks

The offline checks do not connect to Discord or require a token:

```powershell
python -m unittest discover -v
python -m compileall -q .
```

## License

This project is licensed under the MIT License with the Commons Clause License
Condition. See [LICENSE](LICENSE) and [COMMON CLAUSE](COMMON%20CLAUSE).
