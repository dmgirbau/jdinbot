# jdinbot

**jdinbot** is an open-source **banking** bot built using `python-telegram-bot`. It provides users with **account management, referral rewards, JDIN transactions, cashu integration, and an interactive gambling feature**.

## 📣 Latest Updates (March 2025)

- **✅ Improved Database Connection Management**: Implemented async connection pool for better reliability
- **🛠️ Fixed `/tax` Command**: Ensured proper balance deduction when using the tax command
- **📝 Better Documentation**: Added comprehensive docstrings to all database functions
- **🪵 Enhanced Logging**: Added detailed logging for better debugging and monitoring

## 🚀 Features

### 🎟️ Account & Referral System
- Users receive a unique referral code upon registration.
- Optional referral input during signup to earn a **configurable JDIN bonus**.
- Referral rewards are credited to both the user and the referrer.

### 💰 JDIN Transactions
- Users can transfer JDIN tokens to others using their **unique referral codes** or their **Telegram username**.
- Transaction history is stored securely in an SQLite database.
- `/tax` command allows users to voluntarily donate JDIN to the system.

### 🎲 Gambling: "Ofrenda al Lojdin"
- Users can bet JDIN and roll a **6-sided die**, a form of voluntary taxation.
- Consecutive rolls of **6** multiply rewards exponentially.
- Full transaction logs with betting history.

### 🔗 Cashu Integration


### 📊 Admin & Analytics
- View **gambling results history** and **total JDIN in circulation**.
- Statistics.
- Full **transaction and gambling history logs**.

## 🛠️ Installation

### 1️⃣ Prerequisites
- Python 3.11
- python-Telegram-bot 22.0+
- aiosqlite 0.17.0+
- dotenv 0.9.9
- Telegram Bot API Key (Create via [BotFather](https://t.me/botfather))

### 2️⃣ Clone the Repository
```sh
git clone https://github.com/dmgirbau/jdinbot.git
cd jdinbot
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure the Bot

Create a `.env` file in the root directory and add:

```ini
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_API_KEY
ADMIN_CHAT=YOUR_TELEGRAM_ID
```

### 5️⃣ Run the Bot

```sh
python -m src.main
```

## 🗄️Database Schema

SQLite is used for storage. Key tables:

- **users**: Stores account data and referral codes.
- **transactions**: Logs JDIN transfers.
- **lojdin_statistics**: Stores gambling outcomes and statistics.

## 🧑‍💻 Development

### Database Connection Management

The bot uses an async connection pool to manage SQLite connections efficiently:

```python
async with connection() as conn:
    cursor = await conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = await cursor.fetchone()
```

## 🛠️ Development & Contribution

We welcome **pull requests and issues**! Follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Added feature X"`).
4. Push to GitHub (`git push origin feature-name`).
5. Create a pull request.

## 📜 License

This project is licensed under the **GPL-3.0 License**.

## 🌟 Support & Contact

- **Contribute:** [GitHub Issues](https://github.com/dmgirbau/jdinbot/issues)
- **Telegram Channel:** https://t.me/lojdin