from src.db.dbconfiguration import connection


async def updatebalance(winnings,userid,mod="+"):
    return await connection().execute(f"UPDATE users SET jdin_balance = jdin_balance {mod} ? WHERE user_id = ?", (winnings, userid)).commit()
async def gambling_session(userid,bet_amount,multiplier,winnings,streak):
    return await connection().execute("""INSERT INTO gambling_logs (user_id, bet_amount, multiplier, winnings, streak) VALUES (?, ?, ?, ?, ?)""", (userid, bet_amount, multiplier, winnings, streak)).commit()
async  def winingstatus():
    return await connection().execute("SELECT COUNT(*), SUM(winnings) FROM gambling_logs")
async def maxmultiplier():
    return await connection().execute("SELECT MAX(multiplier) FROM gambling_logs")