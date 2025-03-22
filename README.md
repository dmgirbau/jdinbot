# jdinbot

**jdinbot** is an open-source **token management and gambling** bot built using `python-telegram-bot`. It provides users with **account management, referral rewards, JDIN transactions, Solana wallet integration, and an interactive gambling feature**.

## 🚀 Features

### 🎟️ Account & Referral System
- Users receive a unique referral code upon registration.
- Optional referral input during signup to earn a **configurable JDIN bonus**.
- Referral rewards are credited to both the user and the referrer.

### 💰 JDIN Transactions
- Users can transfer JDIN tokens to others using their **unique referral codes** or their **Telegram username**.
- Transaction history is stored securely in an SQLite database.

### 🎲 Gambling: "Ofrenda al Lojdin"
- Users can bet JDIN and roll a **6-sided die**, a form of voluntary taxation.
- Consecutive rolls of **6** multiply rewards exponentially.
- Full transaction logs with betting history.

### 🔗 Solana Wallet Integration
- Users can request Solana account setup:
  - **Existing Address:** Direct deposit activation, with a minimal **configurable fee**.
  - **New Address:** Requires admin approval and JDIN payment.
- Only **one approved Solana wallet per user**.

### 📊 Admin & Analytics
- View **gambling results history** and **total JDIN in circulation**.
- Statistics.
- Admins can manually approve **Solana wallet** requests.
- Full **transaction and gambling history logs**.

## 🛠️ Installation

### 1️⃣ Prerequisites
- Python 3.11
- dotenv 0.9.9
- python-Telegram-bot 22.0+
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

python jdinbot.py
```

## 🗄️Database Schema

SQLite is used for storage. Key tables:

- **users**: Stores account data and referral codes.
- **transactions**: Logs JDIN transfers.
- **solana_requests**: Tracks wallet approval requests.
- **gambling_logs**: Stores gambling outcomes.

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