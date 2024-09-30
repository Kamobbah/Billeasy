import os
import asyncio
import datetime
from .settings import SystemSettings

class System:

    ##
    # Get date section
    @classmethod
    def date_strip (cls, value = 'year'):

        strip = {
            'YEAR': datetime.date.today().year,
            'MONTH': datetime.date.today().month,
            'DAY': datetime.date.today().day,
            'HOUR': datetime.datetime.now().hour,
            'MINUTE': datetime.datetime.now().minute,
            'SECONDS': datetime.datetime.now().second
        }
        res = strip.get(value.upper())

        if res < 10:
            res = '0' + str(strip.get(value.upper()))
        
        elif res == 0:
            res = '00'

        return res

    ##
    # Set a new session id
    @classmethod
    def session_set (cls):

        session_id = '{}_{}_{}_{}{}{}'.format(
            System.date_strip('day'),
            System.date_strip('month'),
            System.date_strip('year'),
            System.date_strip('hour'),
            System.date_strip('minute'),
            System.date_strip('seconds')
        )
        SystemSettings.session_settings['session_id'] = session_id
    
    ##
    # Get full date
    @classmethod
    async def date_full (cls):

        date = '{}/{}/{}'.format(
            System.date_strip('day'),
            System.date_strip('month'),
            System.date_strip('year')
        )

        time = '{}:{}:{}'.format(
            System.date_strip('hour'),
            System.date_strip('minute'),
            System.date_strip('seconds')
        )

        return f'{date} {time}'

    ##
    # Is two array the same ?
    @classmethod
    async def is_matching (cls, arr1, arr2):

        if arr1 == arr2:
            return True

        return False