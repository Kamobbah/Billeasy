import asyncio
import random
from core.system.system import System
from core.system.settings import SystemSettings
from core.system.filesmanager import FilesManager
from .user import User

class Frank:
    settings = None
    settings_bet = {
        # min reached
        'min_reached': -1,

        # safety mode of the bet cash out
        'cash_out_safety': False,

        # time lose despite the self confidence
        'self_confidence_lost': 0,
        
        # Amount of bet since last bet condition
        'attempts_actual': 0,

        # Amount of bet to do since last bet condition
        'attempts_to': 0,

        # Waiting times
        'time_waiting': 0,

        # Success condition times
        'time_match': 0,

        # Last result was a victory
        'last_win': True
    }
    betting = False

    def __init__ (self):

        self.user = User()
        self.settings = SystemSettings.frank_settings['side_human']
    
        bet_list = SystemSettings.frank_settings['side_bet']
        bet_list_keys = [*bet_list]
        bet_list_vals = [*bet_list.values()]

        for x in range(len(bet_list)):
            self.settings_bet[bet_list_keys[x]] = bet_list_vals[x]
    
    ##
    # New activity
    async def activity_new (self, datas):

        lastest = datas['result_last'] if 'result_last' in datas else None
        action = datas['action'] if 'action' in datas else None
        bet = datas['result_bet'] if 'result_bet' in datas else None
        balance = datas['balance'] if 'balance' in datas else None

        send = {
            'result_last': lastest,
            'result_bet': bet,
            'balance': balance,
            'action': action
        }

        await FilesManager.session_new_activity(send)

    ##
    # Action of betting or not
    async def bet_action_set (self, state = False):

        self.betting = state

    ##
    # To bet or not to bet ?
    async def calculating (self, lastests):

        betable = lastests[0] <= self.settings_bet['condition']
        
        if await self.calculating_cash_out():
            return False
        
        brains = {
            'BIG': self.brain_big,
            'STANDARD': self.brain_standard
        }
        
        call_brain = brains.get(self.settings['brain'].upper())

        return await call_brain(betable, lastests)

    ##
    # Check if we cash out
    async def calculating_cash_out (self):

        async def reset ():

            self.settings_bet['self_confidence_lost'] = 0
            self.settings_bet['cash_out_safety'] = False

        async def calculating ():

                # If there is a max wallet desired to stop
                # and we reached it, we stop
            if self.settings_bet['max'] != False \
                and wallet >= self.settings_bet['max']:
                return True
                
                # If the timer is activated
            if SystemSettings.session_settings['timer'] != False:
                    # If we reached the limit of time indicated,
                    # we stop
                    if timer_end:
                        return True

                # If we reached a new minimum, save it
                # and reset settings
                # and say that we're not ready to cash out
            if self.settings_bet['mins'] != False:
                if len(self.settings_bet['mins']) > 1 \
                    and len(self.settings_bet['mins']) != self.settings_bet['min_reached'] + 1:
                    if wallet >= self.settings_bet['mins'][self.settings_bet['min_reached'] + 1]:
                        self.settings_bet['min_reached'] += 1
                        await reset()
                        return False
                
                else:
                    if wallet >= self.settings_bet['mins'][0] \
                        and self.settings_bet['min_reached'] == -1:
                        self.settings_bet['min_reached'] += 1
                        await reset()
                        return False

                # Else, if we still have self-confidence, let's keep going
            if self.settings_bet['self_confidence_lost'] != self.settings['self_confidence']:
                return False

                # Else, if we haven't reached a minium, we keep going
            elif self.settings_bet['min_reached'] == -1:
                return False

                # Else, if the next bet is inferior or equal to the minimum
                # and the cash out safety is on
                # and the cash out security is activated
            elif final_wallet <= self.settings_bet['mins'][self.settings_bet['min_reached']] \
                and self.settings_bet['cash_out_safety']:
                return True
        
        async def timer ():
            
            if (SystemSettings.session_settings['timer']):
                timer_day = SystemSettings.session_settings['timer']['day']
                timer_time = SystemSettings.session_settings['timer']['time']
                day = System.date_strip('day')
                month = System.date_strip('month')
                year = System.date_strip('year')
                hour = System.date_strip('hour')
                minute = System.date_strip('minute')

                    # If date is passed, we stop
                if timer_day[0] < int(day) \
                    and timer_day[1] <= int(month) \
                    and timer_day[2] <= int(year):
                    return True

                    # If it's the correct day and the timer is reached,
                    # we stop
                elif timer_day[0] == int(day) \
                    and timer_day[1] == int(month) \
                    and timer_day[2] == int(year) \
                    and timer_time[0] <= int(hour) \
                    and timer_time[1] <= int(minute):
                    return True
            
            return False

        timer_end = await timer()
        wallet = await self.user.wallet_total()
        final_wallet = wallet - self.settings_bet['set']
        cash_out = await calculating()

        if cash_out or timer_end:
            asyncio.create_task( self.activity_new({ 'action': 'Cash out' }) )
            SystemSettings.session_settings['statut'] = False
            
            print('Cash out!')
        
        return cash_out

    ##
    # Simple state of mind
    async def brain_standard (self, betable, lastests):

        if betable:
            asyncio.create_task(self.bet_action_set(True))
            asyncio.create_task(
                self.activity_new({
                'result_last': lastests[0],
                'action': 'Bet'
                }))

            return True

        asyncio.create_task(
            self.activity_new({
            'result_last': lastests[0],
            'action': 'Waiting'
            }))

        return False

    ##
    # Big brain time
    async def brain_big (self, betable, lastests):

        # 3 for more safety 
        max_success = 3
        max_waiting = 2
        state = False
        is_safe = lastests[0] <= self.settings_bet['safety']

        async def reset ():
            self.settings_bet['attempts_to'] = 0
            self.settings_bet['attempts_actual'] = 0
            return False

        # Knowing the rates of results
        # and act in consequences
        async def attempts_results ():

            nonlocal state, is_safe, max_success, max_waiting

                # If we can bet, we bet
                # and memorize the fact that you bet this time
            if betable:
                state = True
                self.settings_bet['time_match'] += 1

                    # If the amount of successives matching betable
                    # are superior or equal to the max of safety successive betable
                    # and the last result was safe,
                    # reset the previous successives times waited
                if self.settings_bet['time_match'] >= max_success \
                    and is_safe:
                    self.settings_bet['time_waiting'] = 0

                    # Else, if the total of betable and waiting
                    # are superior or equal to the max safety of the both
                    # reset the previous successives times waited
                elif self.settings_bet['time_match'] + self.settings_bet['time_waiting'] \
                    >= max_success + max_waiting:
                    self.settings_bet['time_waiting'] = 0

                # Else memorize the fact that we waited this time
            else:
                self.settings_bet['time_waiting'] += 1

                    # If the amount of successives waiting
                    # are superior or equal to the max of safety successive waiting
                    # and the last result was inferior or equal to the bet condition,
                    # reset the previous successivs times beted
                if self.settings_bet['time_waiting'] >= max_waiting \
                    and lastests[0] <= self.settings_bet['condition']:
                    self.settings_bet['time_match'] = 0
                
                    # Else, if the total of betting and waiting
                    # are superior or equal to the max safety of the both
                    # reset the previous successives times beted
                elif self.settings_bet['time_match'] + self.settings_bet['time_waiting'] \
                    >= max_success + max_waiting:
                    self.settings_bet['time_match'] = 0

        # First stage of verifications
        async def checking1 ():

            nonlocal state

                # If we reached the max of betting session, we stop
            if self.settings_bet['attempts_to'] == self.settings_bet['attempts_actual']:
                self.settings_bet['attempts_to'] = 0
                self.settings_bet['attempts_actual'] = 0

                # Else, if we are in a betting session, we bet
            elif self.settings_bet['attempts_to'] != 0: state = True

        # Second stage of verifications
        async def checking2 ():

            nonlocal state, is_safe, max_success, max_waiting

                # If we want to bet, let's check some things
            if state:

                    # If successive waiting are superior or equal
                    # to the max of safety successive waiting
                    # and the betting session is superior to 2 attempts
                    # and it's not safe, we stop
                if self.settings_bet['time_waiting'] >= max_waiting \
                    and self.settings_bet['attempts_to'] > 2 \
                    and is_safe == False:
                    state = await reset()
                
                    # Else, if successive waiting are superior or equal
                    # to the max of safety successive waiting
                    # and we are not in a betting session
                    # and it's not safe, we stop
                elif self.settings_bet['time_waiting'] >= max_waiting \
                    and self.settings_bet['attempts_to'] <= 0 \
                    and is_safe == False:
                    state = await reset()
                    
                    # Else, if successive betable are superior
                    # to the max of safety successive betable
                    # and the betting session is equal
                    # to the maximum a betting session can have
                    # and it's not safe, we stop
                elif self.settings_bet['time_match'] > max_success \
                    and self.settings_bet['attempts_to'] == self.settings_bet['attempts_max'] \
                    and is_safe == False:
                    state = await reset()

                    # Else, if successive betable are superior
                    # to the max of safety successive betable
                    # and we are not in a betting session
                    # and it's not safe, we stop
                elif self.settings_bet['time_match'] > max_success \
                    and self.settings_bet['attempts_to'] <= 0 \
                    and is_safe == False:
                    state = await reset()

                    # Else, if we've lost last time
                    # and we are in a betting session, we stop
                elif self.settings_bet['last_win'] == False \
                    and self.settings_bet['attempts_actual'] != 0:
                    state = await reset()

        # Third stage of verifications
        async def checking3 ():

            nonlocal state

                # If we want to bet, let's check some things
            if state:

                    # Else, if le last result is superior or equal to 5
                    # and we are in a betting session
                    # where we betted more than once, we stop
                if lastests[0] >= 5 \
                    and self.settings_bet['attempts_actual'] > 1:
                    state = await reset()
                    
                    # If, we got less than two results
                    # and we don't want to quick start, we stop
                if len(lastests) < 2 \
                    and self.settings['quick_start'] == False:
                    state = await reset()

        # Fouth stage of verifications
        async def checking4 ():

            nonlocal state

                # If we still want to bet, let's check some things
            if state:

                    # If we are not in a betting session, we start a betting session
                if self.settings_bet['attempts_to'] <= 0:
                    self.settings_bet['attempts_to'] = random.randint(self.settings_bet['attempts_min'], self.settings_bet['attempts_max'])
                    self.settings_bet['attempts_actual'] = 0

                        # If the betting session is equal to 0 attempts, we don't bet
                    if self.settings_bet['attempts_to'] <= 0: state = False

                    # If we are in a betting session,
                    # we make a bet attempt
                if self.settings_bet['attempts_to'] > 0:
                    self.settings_bet['attempts_actual'] += 1

        await attempts_results()
        await checking1()
        await checking2()
        await checking3()
        await checking4()

        if state:
            asyncio.create_task(self.bet_action_set(True))
            asyncio.create_task(
                self.activity_new({
                'result_last': lastests[0],
                'action': f'Bet {self.settings_bet["attempts_actual"]}/{self.settings_bet["attempts_to"]}'
                }))
        else:
            asyncio.create_task(
                self.activity_new({
                'result_last': lastests[0],
                'action': 'Waiting'
                }))

        return state
