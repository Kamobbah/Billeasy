import asyncio
from core.system.settings import SystemSettings
from core.system.system import System
from core.system.filesmanager import FilesManager
from ..accounts.frank import Frank

class Session (Frank):

    # Lastests bets
    lastests_results = []

    def __init__ (self):
        super().__init__()

    async def start (self):
        # await System.session_set()
        await FilesManager.session_new()

    ##
    # Refresh lastests bets if changes
    async def lastests_set (self, results):

        same_results = await System.is_matching(self.lastests_results, results)

        if same_results == True:
            return False

        self.lastests_results = []
        self.lastests_results.extend(results)
        
        return True

    ##
    # Get the lastests bets
    async def lastests_get (self):
        return self.lastests_results
        
    ##
    # Get the amount of winning
    async def bet_amount_win (self):
        return self.settings_bet['set'] * self.settings_bet['stop'] - self.settings_bet['set']

    ##
    # Get the amount of loss
    async def bet_amount_lose (self):
        return self.settings_bet['set']

    ##
    # Wallet verification
    async def verification (self):
        
        lastests = await self.lastests_get()

        if self.betting:
            await self.bet_result(lastests[0])

        wallet = await self.user.wallet_total()

        if wallet >= self.settings_bet['set']:
            return await self.calculating(lastests)

        else:
            SystemSettings.session_settings['statut'] = False
            asyncio.create_task( self.activity_new({ 'action': 'Not enough money' }) )
            
            print('Session end.')

        return False
        
    ##
    # Get results of the bet
    async def bet_result (self, last):

        await self.bet_action_set()

        async def acitivities (win):

            wallet = await self.user.wallet_total()
            
            if win:
                asyncio.create_task(
                    self.activity_new({
                    'result_bet': 'WIN',
                    'balance': wallet
                    }))
                
                balance_new_record = await self.user.balance_record()
                if balance_new_record:
                    asyncio.create_task( FilesManager.session_balance_update(wallet, True) )
            
            else:
                asyncio.create_task(
                    self.activity_new({
                    'result_bet': 'LOSE',
                    'balance': wallet
                    }))
                
            asyncio.create_task( FilesManager.session_balance_update(wallet) )

        if last >= self.settings_bet['stop']:
            self.settings_bet['last_win'] = True
            money = await self.bet_amount_win()
            await self.user.wallet_win(money)
            await acitivities(win=True)
        
        else:
            if self.settings_bet['cash_out_safety']:
                self.settings_bet['self_confidence_lost'] += 1

            self.settings_bet['cash_out_safety'] = True
            
            if self.settings_bet['last_win']:
                self.settings_bet['last_win'] = False

            money = await self.bet_amount_lose()
            await self.user.wallet_lose(money)
            await acitivities(win=False)