import logging
from src.db.dbconfiguration import connection


async def updatebalance(winnings, userid, mod="+"):
    """
    Update a user's balance by adding or subtracting a specified amount.
    
    This function handles both adding winnings and deducting taxes from a user's balance
    depending on the 'mod' parameter.
    
    Args:
        winnings (float): The amount to add or subtract from the user's balance
        userid (int): The Telegram user ID
        mod (str, optional): The operation to perform. '+' to add, '-' to subtract. Defaults to '+'
        
    Returns:
        bool: True if the update was successful, False otherwise
    """
    logging.info(f"Updating balance for user {userid} with {mod}{winnings}")
    try:
        async with connection() as conn:
            query = f"UPDATE users SET jdin_balance = jdin_balance {mod} ? WHERE user_id = ?"
            logging.info(f"Executing SQL: {query} with params: ({winnings}, {userid})")
            cursor = await conn.execute(query, (winnings, userid))
            logging.info(f"Rows affected: {cursor.rowcount}")
            await conn.commit()
            logging.info("Transaction committed successfully")
            return True
    except Exception as e:
        logging.error(f"Error updating balance: {e}")
        return False


async def gambling_session(userid, bet_amount, multiplier, winnings, streak):
    """
    Log a gambling session in the lojdin_statistics table.
    
    This function records the details of a gambling session, including the bet amount,
    outcome, and number of rolls (streak).
    
    Args:
        userid (int): The Telegram user ID
        bet_amount (float): The amount that was bet
        multiplier (float): The multiplier applied to the bet amount
        winnings (float): The total winnings (can be negative)
        streak (int): The number of successful rolls
        
    Returns:
        bool: True if the logging was successful, False otherwise
    """
    logging.info(f"Logging gambling session for user {userid}")
    try:
        async with connection() as conn:
            await conn.execute("""INSERT INTO lojdin_statistics (user_id, bet_amount, outcome, rolls, timestamp) 
                            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)""", 
                           (userid, bet_amount, winnings, streak))
            await conn.commit()
            logging.info("Gambling session logged successfully")
            return True
    except Exception as e:
        logging.error(f"Error logging gambling session: {e}")
        return False


async def winingstatus():
    """
    Get statistics about gambling winnings across all users.
    
    Returns:
        tuple or None: A tuple containing (count, total_winnings) or None if error
    """
    async with connection() as conn:
        cursor = await conn.execute("SELECT COUNT(*), SUM(outcome) FROM lojdin_statistics")
        result = await cursor.fetchone()
        await cursor.close()
        return result


async def maxmultiplier():
    """
    Get the maximum multiplier achieved in gambling sessions.
    
    Returns:
        float or None: The maximum multiplier value or None if no sessions exist
    """
    async with connection() as conn:
        cursor = await conn.execute("SELECT MAX(outcome/bet_amount) FROM lojdin_statistics WHERE bet_amount > 0")
        result = await cursor.fetchone()
        await cursor.close()
        return result