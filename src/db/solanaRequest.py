from datetime import datetime

from src.db.dbconfiguration import connection


async  def verifysolanaacount(userid:int):
    return  await connection().execute("SELECT * FROM solana_accounts WHERE user_id = ?", userid)


async def balance(userid:int):
    return await connection().execute("SELECT jdin_balance FROM users WHERE user_id = ?", userid)


async def descountfee(fee,userid):
    return await connection().execute("UPDATE users SET jdin_balance = jdin_balance - ? WHERE user_id = ?", (fee, userid))


async def solanarequest(userid,adress,requestype,fee):
    return  connection().execute("""
        INSERT INTO solana_requests (user_id, solana_address, type, fee)
        VALUES (?, ?, ?, ?)
    """, (userid, adress, requestype, fee)).commit()


async def transactioStatus(userid):
    return connection().execute("SELECT * FROM solana_requests WHERE user_id = ? AND status = 'pending'", (userid,)).fetchone()


async def transactionUpdateSatus(userid):
    return await connection().execute(f"UPDATE solana_requests SET status = 'approved', approved_at ={datetime.now()}  WHERE user_id = ?", (userid,))


async def insertransaction(userid,solanaadress):
    return await connection().execute("INSERT INTO solana_accounts (user_id, solana_address) VALUES (?, ?)", (userid, solanaadress)).commit()