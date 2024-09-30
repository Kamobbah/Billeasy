class SystemSettings:

    system_settings = {
        'name': 'Billeasy',
        'version': 'v1.3'
    }

    files_manager_settings = {
        'autofill_file': 'logs/autofill.json',
        'session_file': False,
        'session_directory': 'logs/sessions/',
        'ui_directory': 'core/packages/app/gui/'
    }
    
    session_settings = {
        'statut': True,
        'session_id': '',
        'stats_success': 0,
        'stats_total': 0,

        ##
        ## Demo mode
        ##
        # Create a real time simulation of the session
        # Demo : True | False
        'mode_demo': True,

        #####
        ##
        ## Timer
        ##
        # Set a timer to the session
        # [Default: False]
        'timer': False
    }

    app_settings = {
        'url_img': 'core/packages/app/img/'
    }

    user_settings = {
        'username': None,
        'password': None,
        'telegram': None,

        #####
        ##
        ## Wallet
        ##
        # Current wallet in your account
        # can be inferior to the original wallet
        # to not empty the wallet
        # [Default: 100] 
        'wallet': 100
    }

    frank_settings = {
        'side_human': {
            #####
            ##
            ## Brain
            ##
            # Activate brain of the game
            # brain : big | standard
            # [Default: big]
            'brain': 'big',

            ##
            ## Big Money mode increase the Set by 10 
            ## when reaching a certain point (15x the wallet)
            ##
            # BigMoney : True | False
            'mode_big_money': False,

            #####
            ##
            ## Self-confidence
            ##
            # keep trying to bet even when you are supposed to stop
            # [Default: 1]
            'self_confidence': 1,

            #####
            ##
            ## Quick start
            ##
            # start betting when the first result appear
            # quickStart : True | False
            # [Default: False]
            'quick_start': False
        },

        'side_bet': {
            #####
            ##
            ## set
            ##
            # Bet to set everytime
            # [Default: 100]
            'set': 100,

            #####
            ##
            ## stop 
            ##
            # When stopping the bet
            # [Default: 1.10]
            'stop': 1.10,

            #####
            ##
            ## Attempts Max
            ##
            # How much successive attempts when bet match
            # [Default: 3] [Minimum: 1]
            'attempts_max': 3,

            #####
            ##
            ## Attempts Min
            ##
            # Minimum for the range of attempts
            # Inferior to 1, possibility to not bet when there is an occasion
            # [Default: 0]
            'attempts_min': 0,

            #####
            ##
            ## Mins
            ##
            # Minimums for the balance to cash out
            # Multiples minimum lead multiples step before cashing out
            # for exemples [200, 500] will secure 200 and if 500 reached
            # 500 will be the new save
            # [Default: 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]
            'mins': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300],

            #####
            ##
            ## Max
            ##
            # Maximum for the balance to cash out
            # [Default: False]
            'max': False,
            
            #####
            ##
            ## Condition 
            ##
            # Minimum of the lastest result we want for making a bet
            # [Default: 3.0]
            'condition': 3.0,

            #####
            ##
            ## Safety
            ##
            # If it's risky, we check for safety point safe to bet
            # The safety is a lower Condition
            # [Default: 1.5]
            'safety': 1.5
        }
    }