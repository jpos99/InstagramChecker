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
        print(perfil)
        print(type(perfil))

        try:
            postagen = driver1.find_element_by_partial_link_text(perfil)
            print(postagen)

        except:
            relatorio.write(perfil + '\n')
        #sleep(intervalo)
    lista_posts = driver1.find_elements_by_xpath('// div[ @ class = "C4VMK"]')
    for post in lista_posts:

        post = post.text.split('\n')
        nome_perfil = post[0]
        print(nome_perfil)
        size_text_post = len(post[1].split(' '))
        print(post[1])
        print(size_text_post)
        print('\n')
        if size_text_post < 4:
            relatorio.write(nome_perfil + 'post pequeno\n')

    #sleep(intervalo)



def open_page(url_list):
    driver1 = driver.Chrome("/Users/joao/PycharmProjects/InstagramChecker/chromedriver")

    for url in url_list:
        url = url.replace('\n', '')
        driver1.get(url)
        sleep(2)
        relatorio.write(url)
        find_posts(driver1)
        relatorio.write('\n\n')
    relatorio.close()
    return driver1


driver1 = open_page(url_list)


