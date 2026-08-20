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

4. Copy `.env.example` to `.env` and set `DISCORD_TOKEN` and `DATABASE_URL`.
5. Enable the **Server Members Intent** and **Message Content Intent** for the bot
   in the Discord Developer Portal.
6. Run the bot:

   ```powershell
   python server_utilities.py
   ```

The bot stores its persistent data in Postgres. A Neon Postgres database is
recommended; keep its connection string in `DATABASE_URL`. Server, role, and
channel IDs are currently configured in the Python modules.

## Render deployment

This is a persistent Discord Gateway bot and must run as a continuously running
worker. It is not compatible with a Vercel Function as the primary bot process.

1. Create a Neon Postgres project and copy its connection string.
2. Create a Render Background Worker from this repository.
3. Use the included `render.yaml`, or set the build command to
   `pip install -r requirements.txt` and the start command to
   `python -m scripts.migrate_legacy && python server_utilities.py`.
4. Add `DISCORD_TOKEN` and `DATABASE_URL` as secret environment variables.

The legacy `message_ids.txt` entries are imported idempotently before the bot
starts. The file is no longer read by normal event handling.

## Importing the supplied SQLite database

`DATABASE_URL` is not a path to a local file. It is the Postgres connection
string supplied by Neon, for example:

```text
postgresql://user:password@host/database?sslmode=require
```

After creating the Neon database and setting `DATABASE_URL` in your local `.env`,
run this once from the repository:

```powershell
python -m scripts.migrate_legacy --sqlite-path "C:\Users\Stacer Varien\Documents\database.db"
```

The current blacklist, starboard, and verification data are imported into the
active tables. Older unused SQLite tables are retained in `legacy_sqlite_rows`
so their data is preserved without affecting the current bot.

## Checks

The offline checks do not connect to Discord or require a token:

```powershell
python -m unittest discover -v
python -m compileall -q .
```

## License

This project is licensed under the MIT License with the Commons Clause License
Condition. See [LICENSE](LICENSE) and [COMMON CLAUSE](COMMON%20CLAUSE).
