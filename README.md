# Rahbot

Rahbot is a TF2 Discord bot for assigning division roles and running PUG utility commands.

Supported division/profile sources include ETF2L, RGL, AsiaFortress (`match.tf`), OzFortress, and FBTF.

Works with [pubobot](https://github.com/Leshaka/PUBobot2)

## How to setup and run the bot

### 1) Prerequisites

- Python 3.10+ (recommended)
- A Discord bot application + token
- A Discord server where the bot has role management permissions

### 2) Install dependencies

```cmd
pip install -r requirements.txt
```

### 3) Configure secrets

Rahbot reads keys from either environment variables or `config.ini`:

- `RAHBOT_KEY` (Discord bot token)
- `SERVERME_KEY` (Serveme API key)

Environment variables take priority over `config.ini`.

### 4) Run the bot

```cmd
python rahbot.py
```

If startup is successful, you should see logs like:

- `Starting up...`
- `Logged in!`

## Settings important to change

Most important runtime values are in `settings.py`:

- `COMMAND_PREFIX`
	- Prefix for legacy text commands (default `;`).
- `NOW_PLAYING`
	- Bot presence text (currently set to `/help`).
- `CHANNEL`
	- Channel names where prefixed commands are accepted.
- `TRACK`
	- Substring used for ready-up/game tracking channel matching.
- `ADMIN_COMMANDS`
	- Command names treated as admin-only in help/output filtering.

### Security note

Keep tokens/API keys private. Prefer environment variables in production.

If secrets have ever been committed to source control, rotate them immediately.

## How to setup the bot with roles and database tables

Rahbot supports both slash commands and legacy prefixed commands.

### Slash command setup (recommended)

- Setup division roles:
	- `/setup target:roles`
- Update/fill missing roles and role colors:
	- `/setup target:roles update:true`
- Setup database tables:
	- `/setup target:db`

### Legacy prefixed command setup

- Setup roles:
	- `;setup`
- Update roles:
	- `;setup update`
- Setup database tables:
	- `;setupdb`

### Required bot permissions for setup

The bot should have, at minimum:

- `Manage Roles`
- `Read Messages/View Channels`
- `Send Messages`

Role hierarchy must allow the bot to edit/create target roles.

