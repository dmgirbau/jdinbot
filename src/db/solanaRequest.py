from datetime import datetime

from src.db.dbconfiguration import connection


async def verifysolanaacount(userid: int):
    """
    Verify if a user has a Solana account registered in the database.
    
    Args:
        userid (int): The Telegram user ID to check
        
    Returns:
        tuple or None: A tuple containing the Solana account information if found, None otherwise
    """
    async with connection() as conn:
        cursor = await conn.execute("SELECT * FROM solana_accounts WHERE user_id = ?", (userid,))
        result = await cursor.fetchone()
        await cursor.close()
        return result


async def balance(userid: int):
    """
    Get the current JDIN token balance for a user.
    
    Args:
        userid (int): The Telegram user ID to check
        
    Returns:
        tuple or None: A tuple containing the user's balance if found, None if the user doesn't exist
    """
    async with connection() as conn:  
        cursor = await conn.execute("SELECT jdin_balance FROM users WHERE user_id = ?", (userid,))
        result = await cursor.fetchone()  
        await cursor.close()  
        # Return result as is (it's a tuple) or None if user doesn't exist
        return result


async def descountfee(fee, userid):
    """
    Deduct a fee from a user's JDIN balance.
    
    Args:
        fee (float): The amount to deduct
        userid (int): The Telegram user ID
        
    Returns:
        None
    """
    async with connection() as conn:
        await conn.execute("UPDATE users SET jdin_balance = jdin_balance - ? WHERE user_id = ?", (fee, userid))
        await conn.commit()


async def solanarequest(userid, adress, requestype, fee):
    """
    Create a new Solana request in the database.
    
    Args:
        userid (int): The Telegram user ID
        adress (str): The Solana wallet address
        requestype (str): The type of request ('existing' or 'new')
        fee (float): The fee associated with this request
        
    Returns:
        None
    """
    async with connection() as conn:
        await conn.execute("""
            INSERT INTO solana_requests (user_id, solana_address, type, fee)
            VALUES (?, ?, ?, ?)
        """, (userid, adress, requestype, fee))
        await conn.commit()


async def transactioStatus(userid):
    """
    Check the status of pending Solana transactions for a user.
    
    Args:
        userid (int): The Telegram user ID
        
    Returns:
        tuple or None: Information about the pending transaction if found, None otherwise
    """
    async with connection() as conn:
        cursor = await conn.execute("SELECT * FROM solana_requests WHERE user_id = ? AND status = 'pending'", (userid,))
        result = await cursor.fetchone()
        await cursor.close()
        return result


async def transactionUpdateSatus(userid):
    """
    Update a Solana transaction's status to 'approved'.
    
    Args:
        userid (int): The Telegram user ID whose transaction should be updated
        
    Returns:
        None
    """
    async with connection() as conn:
        await conn.execute(f"UPDATE solana_requests SET status = 'approved', approved_at = ? WHERE user_id = ?", (datetime.now(), userid))
        await conn.commit()


async def insertransaction(userid, solanaadress):
    """
    Insert a new Solana account for a user.
    
    Args:
        userid (int): The Telegram user ID
        solanaadress (str): The Solana wallet address to add
        
    Returns:
        None
    """
    async with connection() as conn:
        await conn.execute("INSERT INTO solana_accounts (user_id, solana_address) VALUES (?, ?)", (userid, solanaadress))
        await conn.commit()