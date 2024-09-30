import os
import asyncio
import json
from .system import System
from .settings import SystemSettings

class FilesManager:

    ##
    # Open JSON file
    @classmethod
    def json_open_file (cls, filename):

        with open(filename, 'r+') as file:
            datas = json.load(file)
        
        return datas
    
    ##
    # Save JSON file
    @classmethod
    def json_save_file (cls, filename, datas):

        with open(filename, 'w+') as file:
            json.dump(datas, file, indent=None)

    ##
    # Is autofill on ?
    @classmethod
    def autofill_get_state (cls):
        
        return cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )['autofill']

    ##
    # Get saved login
    @classmethod
    def autofill_get_login (cls):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )['login']

        SystemSettings.user_settings['username'] = datas['username']
        SystemSettings.user_settings['password'] = datas['password']
        SystemSettings.user_settings['telegram'] = datas['telegram']

    ##
    # Change autofill state
    @classmethod
    def autofill_save_state (cls, state):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )
        datas['autofill'] = state
        cls.json_save_file( SystemSettings.files_manager_settings['autofill_file'], datas )

    ##
    # Change autofill login
    @classmethod
    def autofill_save_login (cls):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )
        
        if datas['autofill']:
            datas['login']['username'] = SystemSettings.user_settings['username']
            datas['login']['password'] = SystemSettings.user_settings['password']
            datas['login']['telegram'] = SystemSettings.user_settings['telegram']
        
        else:
            datas['login']['username'] = None
            datas['login']['password'] = None
            datas['login']['telegram'] = None
        
        cls.json_save_file( SystemSettings.files_manager_settings['autofill_file'], datas )

    ##
    # Set Settings
    @classmethod
    def autofill_set_settings (cls):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )

        SystemSettings.frank_settings['side_human']['brain']            = datas['frank']['brain']
        SystemSettings.frank_settings['side_human']['self_confidence']  = datas['frank']['self_confidence']
        SystemSettings.frank_settings['side_human']['mode_big_money']   = datas['frank']['mode_big_money']
        SystemSettings.frank_settings['side_human']['quick_start']      = datas['frank']['quick_start']
        
        SystemSettings.frank_settings['side_bet']['set']                = datas['bets']['set']
        SystemSettings.frank_settings['side_bet']['stop']               = datas['bets']['stop']
        SystemSettings.frank_settings['side_bet']['attempts_max']       = datas['bets']['attempts_max']
        SystemSettings.frank_settings['side_bet']['attempts_min']        = datas['bets']['attempts_min']
        SystemSettings.frank_settings['side_bet']['mins']               = datas['bets']['mins']
        SystemSettings.frank_settings['side_bet']['max']                = datas['bets']['max']
        SystemSettings.frank_settings['side_bet']['condition']          = datas['bets']['condition']
        SystemSettings.frank_settings['side_bet']['safety']             = datas['bets']['safety']
        
        SystemSettings.session_settings['timer']                        = datas['session']['timer']
    
    ##
    # Update Settings
    @classmethod
    def autofill_update_settings (cls, settings):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )

        datas['frank']['brain']             = settings['frank']['brain']
        datas['frank']['self_confidence']   = settings['frank']['self_confidence']
        datas['frank']['quick_start']       = settings['frank']['quick_start']
        
        datas['bets']['set']                = settings['bets']['set']
        datas['bets']['stop']               = settings['bets']['stop']
        datas['bets']['attempts_max']       = settings['bets']['attempts_max']
        datas['bets']['attempts_min']        = settings['bets']['attempts_min']
        datas['bets']['mins']               = settings['bets']['mins']
        datas['bets']['max']                = settings['bets']['max']
        datas['bets']['condition']          = settings['bets']['condition']
        datas['bets']['safety']             = settings['bets']['safety']
        
        datas['session']['timer']           = settings['session']['timer']

        cls.json_save_file( SystemSettings.files_manager_settings['autofill_file'], datas )

    ##
    # Get Settings
    @classmethod
    def autofill_get_settings (cls):

        datas = cls.json_open_file( SystemSettings.files_manager_settings['autofill_file'] )

        settings = {
            'frank': datas['frank'],
            'bets': datas['bets'], 
            'session': datas['session']
            }

        return settings

    ##
    # Set new session file
    @classmethod
    async def session_new (cls):

        SystemSettings.files_manager_settings['session_file'] = SystemSettings.files_manager_settings['session_directory']
        SystemSettings.files_manager_settings['session_file'] += 'demo/' if SystemSettings.session_settings['mode_demo'] else 'real/'
        SystemSettings.files_manager_settings['session_file'] += SystemSettings.session_settings['session_id'] + '/'
        cls.filename_session = SystemSettings.files_manager_settings['session_file']

        os.mkdir(cls.filename_session)
        await cls.session_init()

    ##
    # Initialization of session file content
    @classmethod
    async def session_init (cls):

        html = f"""
            <!DOCTYPE html>
            <html lang="FR">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <link rel="icon" href="../../../html/img/logo.svg" type="image/svg+xml">
                
                <title>{SystemSettings.system_settings['name']}</title>
                <link rel="stylesheet" href="../../../html/css/style.css" />
                <link rel="stylesheet" href="../../../html/css/session.css" />
            </head>

            <body>
                <div id="root" data-session="{SystemSettings.session_settings['session_id']}"></div>
                
                <script src="../../../html/js/main.js"></script>
                <script src="../../../html/js/session.js"></script>
            </body>
            </html>
        """

        # create html file
        with open(cls.filename_session + 'session.html', 'w+') as file:
            file.write(html)
        
        #create datas file
        cls.filename_session += 'datas.json'

        mins = SystemSettings.frank_settings['side_bet']['mins']
        mins = ' | '.join(str(e) for e in mins) if mins != False else mins

        timer = SystemSettings.session_settings['timer']

        if timer != False:
            timer_day = '/'.join((str(e) if e >= 10 else '0' + str(e)) for e in timer['day'])
            timer_time = ':'.join((str(e) if e >= 10 else '0' + str(e)) for e in timer['time'])
            timer = timer_day+ ' ' +timer_time
        
        datas = {
            'name': SystemSettings.system_settings['name'],
            'session_id': SystemSettings.session_settings['session_id'],
            'user': {
                'username': SystemSettings.user_settings['username'],
                'wallet_start': SystemSettings.user_settings['wallet'],
                'wallet_record': SystemSettings.user_settings['wallet'],
                'wallet_final': SystemSettings.user_settings['wallet'],
                'mins': mins,
                'max': SystemSettings.frank_settings['side_bet']['max']
            },
            'frank': {
                'brain': SystemSettings.frank_settings['side_human']['brain'],
                'self_confidence': SystemSettings.frank_settings['side_human']['self_confidence'],
                'mode_big_money': SystemSettings.frank_settings['side_human']['mode_big_money'],
                'attempts_max': SystemSettings.frank_settings['side_bet']['attempts_max'],
                'attempts_min': SystemSettings.frank_settings['side_bet']['attempts_min']
            },
            'bet': {
                'stats': '0/0',
                'set': SystemSettings.frank_settings['side_bet']['set'],
                'condition': SystemSettings.frank_settings['side_bet']['condition'],
                'stop': SystemSettings.frank_settings['side_bet']['stop'],
                'safety': SystemSettings.frank_settings['side_bet']['safety'],
            },
            'session': {
                'statut': SystemSettings.session_settings['statut'],
                'date_start': await System.date_full(),
                'date_end': await System.date_full(),
                'mode_demo': SystemSettings.session_settings['mode_demo'],
                'timer': timer
            },
            'activities': []
        }

        cls.json_save_file(cls.filename_session, datas)

    ##
    # Update session balances
    @classmethod
    async def session_balance_update (cls, amount, record = False):

        datas = cls.json_open_file(cls.filename_session)

        if record:
            datas['user']['wallet_record'] = amount

        else:
            datas['user']['wallet_final'] = amount

        cls.json_save_file(cls.filename_session, datas)

    ##
    # Set new session activity
    @classmethod
    async def session_new_activity (cls, activity = {}):

        datas = cls.json_open_file(cls.filename_session)

        if activity:
            if activity['balance'] is not None:
                SystemSettings.session_settings['stats_total'] += 1
                if activity['result_bet'] == 'WIN': SystemSettings.session_settings['stats_success'] += 1

            activity = {
                'result_last': activity['result_last'],
                'result_bet': activity['result_bet'],
                'action': activity['action'],
                'balance': activity['balance']
            }

            datas['activities'].append(activity)
            datas['bet']['stats'] = f"{ SystemSettings.session_settings['stats_success'] }/{ SystemSettings.session_settings['stats_total'] }"

        datas['session']['date_end'] = await System.date_full()

        if SystemSettings.session_settings['statut'] == False: datas['session']['statut'] = False
        
        cls.json_save_file(cls.filename_session, datas)