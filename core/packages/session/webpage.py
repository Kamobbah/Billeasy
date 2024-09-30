import os
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.common.by import By

from core.system.settings import SystemSettings
from core.system.filesmanager import FilesManager
from .system import Session

class SessionWebPage:
    
    logged = False
    urls = {
        False: 'https://stake.com/casino/home',
        True: 'https://stake.com/casino/games/crash'
        }

    def __init__ (self):

        self.session = Session()
        options = webdriver.ChromeOptions()
        options.add_argument("--allow-file-access-from-files")
        options.add_argument("--disable-web-security")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_service = ChromeService('chromedriver')
        chrome_service.creationflags = CREATE_NO_WINDOW
        
        self.driver = webdriver.Chrome("chromedriver.exe", options = options, service=chrome_service)
    
    ##
    # Open window
    async def window_open (self):

        await self.session.start()
        self.url = self.urls.get(SystemSettings.session_settings['mode_demo'])

        session_file = 'file:///' + os.getcwd() + '/' + SystemSettings.files_manager_settings['session_file'] + 'session.html'
        self.driver.get(session_file)
        self.driver.execute_script(f'window.open("{self.url}")')
        asyncio.create_task(self.tab_close())

        async def switch_tab ():

            self.driver.switch_to.window(self.driver.window_handles[1])

        await switch_tab()
        await self.cookies()

        print('Setup...')

    ##
    # Close window
    async def tab_close (self): 

        await asyncio.sleep(3)

        while SystemSettings.session_settings['statut']:
            await asyncio.sleep(1)

        asyncio.create_task(FilesManager.session_new_activity())
        self.driver.close()

    ##
    # Close cookies panel
    async def cookies (self):

        while (len(self.driver.find_elements(By.CLASS_NAME, 'cookie-banner')) == 0):
            await asyncio.sleep(0.5)
        
        cookies_content = self.driver.find_element(By.CLASS_NAME, 'cookie-banner')
        cookies_content.find_element(By.TAG_NAME, 'button').click()
    
    ##
    # Login account to game
    async def login (self):

        path_modal = '//div[ @data-test="modal-auth" ]'
        self.driver.find_element(By.XPATH, '//button[ @data-test="login-link" ]').click()
        
        await asyncio.sleep(2)
        
        input_email = self.driver.find_element(By.XPATH, path_modal + '//input[ @data-test="login-name" ]')
        input_password = self.driver.find_element(By.XPATH, path_modal + '//input[ @data-test="login-password" ]')

        input_email.send_keys(await self.session.user.user_username())
        input_password.send_keys(await self.session.user.user_password())
        
        print('Wainting for connection...')

        while self.driver.current_url != self.url:
            await asyncio.sleep(1)

        print("Connected.")

        await self.setup()

    ##
    # Set up interface
    async def setup (self):

        # Convet to €
        self.driver.find_element(By.CLASS_NAME, 'coin-toggle').click()
        await asyncio.sleep(1)

        self.driver.find_element(By.XPATH, '//div[ contains(@class, "fiat-toggle") ]/label').click()
        await asyncio.sleep(1)
        
        path_content = '//div[ contains(@data-test, "modal-fiatTerms") ]//div[ contains(@class, "modal-content") ]//'
        self.driver.find_element(By.XPATH, path_content + 'div[ contains(@class, "center") ]/div/div[2]/label').click()
        await asyncio.sleep(1)
        self.driver.find_element(By.XPATH, path_content + 'div[ contains(@class, "button-wrap") ]/button').click()

        # Go to game
        self.driver.find_element(By.XPATH, '//a[ contains(@href, "/casino/games/crash") ]').click()
        
        await asyncio.sleep(3)

    ##
    # Launching betting system
    async def launch (self):

        past_bets = self.driver.find_element(By.CLASS_NAME, 'past-bets')

        while len(past_bets.find_elements(By.TAG_NAME, 'button')) == 0:
            await asyncio.sleep(1)
    
        print("Session started.")

        asyncio.create_task(self.results_handler())
        
        while SystemSettings.session_settings['statut']:
            await asyncio.sleep(1)

    ##
    # Checking for the results
    async def results_handler (self):
        
        async def btn_bet_activated ():

            while self.driver.find_element(By.XPATH, '//div[ contains(@class, "game-sidebar") ]//button/span/span').text.lower() \
                != 'pari':
                await asyncio.sleep(1)

        await btn_bet_activated()
        container = self.driver.find_element(By.CLASS_NAME, 'past-bets')
        
        async def verification ():

            await results()
            wallet_verification = await self.session.verification()

            if wallet_verification \
                and SystemSettings.session_settings['mode_demo'] == False:
                asyncio.create_task(self.make_a_bet())

            await asyncio.sleep(1)
            
            if SystemSettings.session_settings['statut']:
                 asyncio.create_task(verification())

        async def results ():

            async def to_float (str):

                extract = str.split('×')[0]

                if ' ' in extract: extract = extract.replace(' ', '')

                extract = '.'.join(extract.split(','))

                return float(extract)
            
            async def changes ():
                
                all = container.find_elements(By.TAG_NAME, 'button')
                res1 = await to_float(all[0].text)
                last_results = [res1]

                if (len(all) > 1):
                    res2 = await to_float(all[1].text)
                    last_results.append(res2)

                return await self.session.lastests_set(last_results)

            while await changes() == False:
                await asyncio.sleep(1)

        await verification()

    ##
    # Start a new bet
    async def make_a_bet (self):

        input_bet = self.input_bet = self.driver.find_element(By.XPATH, '//div[ contains(@class, "game-sidebar") ]//input[ @data-test="input-game-amount" ]')
        input_stop = self.input_stop = self.driver.find_element(By.XPATH, '//div[ contains(@class, "game-sidebar") ]//label[ contains(@class, "stacked") ][2]//input')

        input_bet.send_keys(self.session.settings_bet['set'])
        input_stop.send_keys(self.session.settings_bet['stop'])
        self.driver.find_element(By.XPATH, '//div[ contains(@class, "game-sidebar") ]//button[@data-test="bet-button"]').click()