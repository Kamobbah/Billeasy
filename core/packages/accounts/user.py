import asyncio
from core.system.settings import SystemSettings

class User:

    settings = SystemSettings.user_settings
    balance_max = 0
    balance_max_new = False
    
    ##
    # Set new balance record
    async def balance_max_set (self, amount):
        self.balance_max = amount
        self.balance_max_new = True

    ##
    # Get the balance record
    async def balance_max_get (self):
        return self.balance_max
    
    ##
    # Do we have a new record ?
    async def balance_record (self):
        if self.balance_max_new:
            self.balance_max_new = False
            return True
        
        return False

    ##
    # Get username
    async def user_username (self):
        return self.settings['username']

    ##
    # Get password
    async def user_password (self):
        return self.settings['password']

    ##
    # Get current wallet sold
    async def wallet_total (self):
        return self.settings['wallet']

    ##
    # We've won !
    async def wallet_win (self, amount):
        self.settings['wallet'] = round(self.settings['wallet'] + amount, 2)

        max = await self.balance_max_get()
        wallet = await self.wallet_total()

        if max < wallet:
            await self.balance_max_set(wallet)

    ##
    # We've lost !
    async def wallet_lose (self, amount):
        self.settings['wallet'] = round(self.settings['wallet'] - amount, 2)