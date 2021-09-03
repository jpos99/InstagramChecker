from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import date
from random import randint, shuffle
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os.path import exists

import SendEmail
import CsvRecorder
from GetUserConfiguration import UserConfigurations
import os


class InstaBot:
    def __init__(self, credentials):
        options = Options()
        options.add_argument("incognito")
        #options.headless = True
        self.driver = webdriver.Chrome(credentials['path_to_chromedriver'], options=options)
        #self.driver = webdriver.Safari()
        self.driver.implicitly_wait(10)
        self.url = credentials['url']
        self.username = credentials['user_name']
        self.password = credentials['password']
        self.login()

    def login(self):
        self.driver.get(self.url)
        sleep(randint(2, 5))
        input_username = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        input_username.send_keys(self.username)
        sleep(randint(2, 5))
        input_password = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        input_password.send_keys(self.password)
        sleep(randint(2, 5))
        log_in_btn = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')
        log_in_btn.click()
        sleep(randint(2, 5))
        not_now = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button')
        not_now.click()
        sleep(randint(2, 5))
        not_now_again = self.driver.find_elements_by_class_name("aOOlW")[1]
        not_now_again.click()
        print('login')
        sleep(randint(2, 5))

    def get_comments_of_post(self, url):
        print('get post')
        self.driver.get(url)
        sleep(randint(3, 7))
        InstaBot.load_all_comments(self)
        lista_posts = self.driver.find_elements_by_xpath('// div[ @ class = "C4VMK"]')
        return lista_posts

    def load_all_comments(self):
        try:
            btn_more_posts = self.driver.find_element_by_class_name("dCJp8")
            sleep(randint(2, 5))
            while btn_more_posts:
                btn_more_posts.click()
                sleep(randint(2, 5))
                btn_more_posts = self.driver.find_element_by_class_name("dCJp8")
        except:
            pass

    def close_session(self):
        self.driver.close()
        self.driver.quit()






def prepara_lista_perfis(lista_perfis):
    lista_nomes_perfis = []
    for linha in lista_perfis:
        if '@' not in linha:
            continue
        linha = linha.replace('\n','').strip()
        linha = linha.replace('@@','@')
        if linha[-1] == '.':
            linha = linha[:-1]
        linha = linha.split('@')
        if linha[-1] == '':
            continue
        lista_nomes_perfis.append(linha[-1].strip())
    return lista_nomes_perfis




def verify_who_comment_in_posts(list_of_posts, perfil_name_list):
    perfil_who_posted = {}
    print(perfil_name_list)
    delet_from_perfil_who_posted = []
    for post in list_of_posts:
        #sleep(randint(1, 3))
        post = post.text.split('\n')
        perfil_name = post[0]
        text_of_post = post[1].split(' ')
        for word in post[1:len(post)-2]:
            word = word.split(' ')
            for w in word:
                text_of_post.append(w)

        size_post_text = len(text_of_post)

        if perfil_name not in perfil_who_posted.keys():
            perfil_who_posted[perfil_name] = size_post_text

        if perfil_name in perfil_who_posted.keys():
            if perfil_who_posted[perfil_name] < size_post_text:
                perfil_who_posted[perfil_name] = size_post_text
        #print(perfil_who_posted.keys())

    for key in perfil_who_posted:
        if key not in perfil_name_list:
            delet_from_perfil_who_posted.append(key)

    print(len(perfil_who_posted))
    for nome in delet_from_perfil_who_posted:
        perfil_who_posted.pop(nome)
    #print(deletar_do_dict)
    #print(perfil_who_posted)

    print(len(perfil_who_posted))
    print(len(perfil_name_list))
    for iten in perfil_who_posted:
        if perfil_who_posted[iten] < 4:
            record_report.record_csv(f'{iten};post pequeno\n')
    for perfil in perfil_name_list:
        if perfil not in perfil_who_posted.keys():
            record_report.record_csv(f'{perfil};não postou\n')
    record_report.record_csv('\n')



def sanitiza_urls(url_list):
    for index in range(len(url_list)):
        #url_list[index] = url_list[index].replace('?utm_source=ig_web_copy_link', '')
        url_list[index] = url_list[index].replace('\n', '')
    return url_list
#path_to_configuration_file = 'Config/UserConfigurations.json'
#configuration = UserConfigurations(path_to_configuration_file)
#email_configuration = configuration.email_configuration()
#instagram_login_configuration = configuration.instagram_login_configuration()
day = date.today().day
print(day)
path_to_filename = os.path.join('Relatorio', f'relatorio_{str(day)}.csv')
record_report = CsvRecorder.RecordCsv(path_to_filename)

url_list = open('ListasDeConferencia/conferencia -27agosto.txt').readlines()
sanitized_url_list = sanitiza_urls(url_list)

lista_perfis = open('ListasDeConferencia/lista-27agosto.txt').readlines()
perfil_name_list = prepara_lista_perfis(lista_perfis)

my_bot = InstaBot(credentials)

for url in sanitized_url_list:
    list_of_posts = my_bot.get_comments_of_post(url)
    print(url + "\n")
    record_report.record_csv('\n' + url + '\n')
    verify_who_comment_in_posts(list_of_posts, perfil_name_list)
my_bot.close_session()



send_email = SendEmail.EmailWithAtachment(email)
message_to_send = send_email.build_message()
send_email.send_the_message(message_to_send)


