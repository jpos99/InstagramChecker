from selenium import webdriver as driver
from time import sleep
import random
from selenium.webdriver.chrome.options import Options

relatorio = open('Relatorio/relatorio.csv', 'w')
url_list = open('ListasDeConferencia/ListaDeUrls.txt').readlines()
lista_perfis = open('ListasDeConferencia/the_goodefellas_2.txt').readlines()


def prepara_lista_perfis(lista_perfis):
    lista_nomes_perfis = []
    for linha in lista_perfis:
        if '@' not in linha:
            continue
        linha = linha.replace('\n','').split('@')
        if linha[-1] == '':
            continue
        lista_nomes_perfis.append(linha[-1].strip())
    return lista_nomes_perfis


def find_posts(driver1):
    lista_nomes_perfis = prepara_lista_perfis(lista_perfis)

    for perfil in lista_nomes_perfis:

        #print(type(perfil))

        try:
            post = driver1.find_element_by_partial_link_text(perfil)

        except:
            print(perfil)
            relatorio.write(perfil + '\n')
        #sleep(intervalo)
    lista_posts = driver1.find_elements_by_xpath('// div[ @ class = "C4VMK"]')
    for post in lista_posts:
        print(post.text)
        post = post.text.split('\n')
        nome_perfil = post[0]

        text_of_post = post[1].split(' ')

        for word in post[1:len(post)-2]:
            word = word.split(' ')
            for w in word:
                text_of_post.append(w)

        size_text_post = len(text_of_post)

        if size_text_post < 4 and nome_perfil in lista_nomes_perfis:
            relatorio.write(nome_perfil + ';post pequeno\n')




def open_page(url_list):
    driver1 = driver.Chrome("/Users/joao/PycharmProjects/InstagramChecker/chromedriver")

    for url in url_list:
        url = url.replace('\n', '')
        driver1.get(url)
        there_are_btn_plus = True
        while there_are_btn_plus:
            try:
                btn_more_posts = driver1.find_element_by_xpath(
                    '// span[@class = "glyphsSpriteCircle_add__outline__24__grey_9 u-__7"] ')

                btn_more_posts.click()
                sleep(5)
            except:
                there_are_btn_plus = False
        relatorio.write(url)
        find_posts(driver1)
        relatorio.write('\n\n')
    relatorio.close()
    return driver1


driver1 = open_page(url_list)


