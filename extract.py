from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import urllib.request
import mysql.connector
import uuid
import sys
import re
import os
# from dotenv import load_dotenv 

# load_dotenv()

# input credencials login
# instausername = os.getenv("MYIGUSERNAME")
# instapassword = os.getenv("MYIGPASSWORD")
instausername = "topcimentelis"
instapassword = "topciment1234"

# Chrome options
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-features=AmbientLightSensor')
path_to_chromedriver = './chromedriver.exe'
service = Service(path_to_chromedriver)

#Navegador
browser = webdriver.Chrome(service = service)

# selected option from node (hashtag)
# selected_value = sys.argv[1]
selected_value = "microcement"


url = 'https://www.instagram.com/'
url_pag = url + '/explore/tags/' + selected_value

# bbdd
mycon = mysql.connector.connect(
    host = "151.80.13.213",
    user = "apptopciment_captacion_leads",
    password = "nXnGy8QvN6",
    database = "apptopciment_captacion_leads"
)

mycursor = mycon.cursor()
mycursor.execute("SET SESSION WAIT_TIMEOUT=960")
mycon.commit()
mycursor.close()



# Login con Selenium
def ig_html(url):
    browser.get(url)
    time.sleep(2)
    try:
        browser.find_element(By.XPATH, '//button[contains(text(), "Permitir todas las cookies")]').click()
    except Exception as e:
        try: 
            browser.find_element(By.XPATH, '//button[contains(text(), "Allow all cookies")]').click()
        except Exception as e:
            print(e)
    time.sleep(2)
    try:
        #ig mobile site login steps
        browser.find_element(By.XPATH, '//input[@name="username"]').send_keys(instausername)

        browser.find_element(By.XPATH, '//input[@type="password"]').send_keys(instapassword)
        browser.find_element(By.XPATH, '//button[@type="submit"]').send_keys(Keys.RETURN)
    except NoSuchElementException:
        try:
            browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(instausername)
            browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(instapassword)
            browser.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').send_keys(Keys.RETURN)
        except Exception as e:
            print(e)

    html = browser.page_source
    return html


# Scroll
def scroller(browser):
    #define initial page height for 'while' loop
    lastHeight = browser.execute_script("return document.body.scrollHeight")
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #define how many seconds to wait while dynamic page content loads
        time.sleep(2)
        newHeight = browser.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        else:
            lastHeight = newHeight
    return browser



db_users = []
user_list = []

db_posts = []
post_list = []

phone_number = None
email = None
contact_page = None

phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|(?:\d{3}|\(\d{3}\))[ -.]?\d{3}[ -.]?\d{4}|(?:\+\d{2}[-. ]?)?\d{3,}[.-]?\d{3,}[.-]?\d{3,}|(?:(?:\+|00)\d{2}[-. ]?)?(?:\d{2,3}[-. ]?)?\d{6,}|(?:\+?9\d{1,2}[-. ]?)?[2-9]\d{6,7}|\+\d{11}|00\d{11}|\(\d{3}\) \d{8}|\d{2}-\d{4}-\d{4}|\+\d{3}-\d{1}-\d{6}|\d{3} \d{2} \d{2} \d{2}|\d{3} \d{3} \d{2} \d{2}'

def extract():

    # sacacmos los ususarios que ya estan en la bbdd
    mycursor = mycon.cursor()
    mycursor.execute("SELECT * FROM posts")
    myposts = mycursor.fetchall()
    mycon.commit()

    for col in myposts:
        user_link = col[2]
        db_users.append(user_link)

        post_link = col[1]
        db_posts.append(post_link)
    print("users in db:", len(db_users), "\nposts in db", len(db_posts))





def extract_insert_user(url_pag):

    # entramos al browser
    browser.get(url_pag)
    time.sleep(2)
    scroller(browser)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")


    # scrapeamos la feed de instagram
    feed = soup.find_all('div', class_="_aabd _aa8k _al3l")

    for post in feed:

    # links de los posts
        for p in post:
            post_href = p['href']

            if post_href not in db_posts and post_href not in post_list:
                post_list.append(post_href)

    print('post list nuevo:', len(post_list))


    for new_post in post_list:

        # scrapeamos cada publicacion
        browser.get('https://www.instagram.com/' + str(new_post))
        time.sleep(4)
        page = browser.page_source
        bsoup = BeautifulSoup(page, "html.parser")


        user = bsoup.find('a', attrs={"class":"x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1i0vuye xwhw2v2 xl56j7k x17ydfre x1f6kntn x2b8uid xlyipyv x87ps6o x14atkfc x1d5wrs8 x972fbf xcfux6l x1qhh985 xm0m39n xm3z3ea x1x8b98j x131883w x16mih1h xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 xjbqb8w x1n5bzlp xqnirrm xj34u2y x568u83"})
        if user:
            user_href = user['href']
            print(user_href)


        if user_href not in db_users and user_href not in user_list:
            user_list.append(user_href)
            print("user list nuevo:", len(user_list))
            
    # scrapeamos los usuarios encontrados que no estan en nuestra bbdd
    for user in user_list:
        try:
            browser.get('https://www.instagram.com/' + str(user))
            time.sleep(4)
            page = browser.page_source
            bs = BeautifulSoup(page, "html.parser")
            # bs_text = bs.get_text()
            time.sleep(2)

            # user's name
            span = bs.find('span', attrs={"class":"_aacl _aaco _aacw _aacx _aad7 _aade"})
            if span:
                name = span.get_text()
            else:
                name = ' - '
            print('Name:', name.encode())

            # account's type
            type_account = bs.find('div', attrs={"class":"_aacl _aaco _aacu _aacy _aad6 _aade"})
            if type_account:
                account = type_account.get_text()
            else:
                account = ' - '
            print('account:', account.encode())

            # user's description
            h1 = bs.find('h1', attrs={"class":"_aacl _aaco _aacu _aacx _aad6 _aade"})
            if h1:
                description = h1.get_text(" ")  

                # check for email in description
                email_in_description = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', description)
                if email_in_description:
                    email = email_in_description[0]
                else:
                    email = None
                # check for phone in description
                phone_in_description = re.findall(phone_pattern, description)
                if phone_in_description:
                    phone_number = phone_in_description[0]
                else:
                    phone_number = None

            else:
                description = ' - '
                
            print('desciption:', description.encode())

            # user's website
            link = bs.find('a', attrs={"target":"_blank"})
            if link['href'] != 'https://about.meta.com/' and link['href'] != '':
                website_link = link['href']
            else:
                website_link = ' - '

            website_name = bs.find('div', attrs={"class":"_aacl _aaco _aacw _aacz _aada _aade"})
            if website_name:
                website = website_name.get_text()
                if '+' in website:
                    browser.find_element(By.CLASS_NAME, "_acan _acao _acas _aj1-").click()
                    links_dialog = browser.page_source
                    links_dialog_bs = BeautifulSoup(links_dialog, 'html.parser')
                    website_btn = links_dialog_bs.find('button', class_="_a9-- _a9_1")
                    website_url = website_btn.find_next('a', attrs={"target":"_blank"})
                    website_link = website_url['href']
            else:
                website = ' - '
            print('website_name:', website)
            print('website_link:', website_link)


            if r'youtube' or r'facebook' in website:
                pass

            # Check if the URL is a WhatsApp link
            # a class "_9vcv _advm _9scb"
            if 'wa.me' in website or 'wa.link' in website or 'whatsapp' in website or 'walink' in website or 'bit' in website:
                wa_btn = bs.find('a', attrs={"class":"_9vcv _advm _9scb"})
                wa_href = wa_btn['href']
                print('whatsapp href:', wa_href)
                phone_match = re.search(r'phone=(\d+)|\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|(?:\d{3}|\(\d{3}\))[ -.]?\d{3}[ -.]?\d{4}|(?:\+\d{2}[-. ]?)?\d{3,}[.-]?\d{3,}[.-]?\d{3,}|(?:(?:\+|00)\d{2}[-. ]?)?(?:\d{2,3}[-. ]?)?\d{6,}|(?:\+?9\d{1,2}[-. ]?)?[2-9]\d{6,7}|\+\d{11}|00\d{11}|\(\d{3}\) \d{8}|\d{2}-\d{4}-\d{4}', wa_href)
                if phone_match:
                    phone_number = phone_match[0]

                else:    
                    wa_href_parts = wa_href.split("&")
                    for part in wa_href_parts:
                        if 'phone=' in part:
                            print('splitted parts:', part)
                    phone_number = part


            # If it's a linktr.ee link
            if 'linktr.ee' in website or 'linkin' in website or 'taplink' in website:
                browser.get(website_link)
                html = browser.page_source
                btflsoup = BeautifulSoup(html, "html.parser")
                text = btflsoup.get_text()
                mail_matches = btflsoup.find_all(href=re.compile('mailto:'))
                
                if mail_matches:
                    email = mail_matches[0]

                else:
                    p_web = re.findall(r'web[site]?|sit[e]?|page|pagina|www', text)
                    if p_web:
                        print(p_web)
                        
                        site_url = btflsoup.find('a', href=re.compile(r'https?://[\w\-\.]+\.[a-zA-Z]{2,20}'))
                        print(site_url)
                        if site_url:
                            site_href = site_url['href']
                            browser.get(site_href)
                            site_page = browser.page_source
                            soup = BeautifulSoup(site_page, 'html.parser')
                            page_html = soup.get_text()

                            site_mail_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', page_html)
                            if site_mail_matches:
                                print(site_mail_matches)
                                email = site_mail_matches[0]
                    else:

                        sites = btflsoup.find_all('a', href=re.compile(r'https?://[\w\-\.]+\.[a-zA-Z]{2,20}'))
                        if sites:
                            browser.get(sites[0])
                            page = soup.get_text()

                            found_mails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', page)
                            if found_mails:
                                print(found_mails[0])
                                email = found_mails[0]



            if website_link != ' - ' and 'wa.link' not in website and 'walink' not in website and 'whatsapp' not in website and 'wa.me' not in website and 'linktr' not in website:
                # Extract email and phone numbers from page
                browser.get(website_link)
                html = browser.page_source
                btflsoup = BeautifulSoup(html, "html.parser")
                text = btflsoup.get_text()
                email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
                phone_matches = re.findall(phone_pattern, text)

                # Choose the first email and phone number if they exist
                if email_matches:
                    email = email_matches[0]

                if phone_matches:
                    phone_number = phone_matches[0]
                
                if email == None and phone_number == None:
                    contact_links = btflsoup.find_all('a', string=re.compile('contact[0]?|kontakt|contato|contatto|контакт[и]?|kapcsolat', re.IGNORECASE))
                    print('CONTACT LINKS ENCONTRADO:', contact_links)
                    if contact_links:
                        contact_page = contact_links[0]['href']
                        print('CONTACT PAGE:', contact_page)
                        if r'http[s]?' in contact_page:
                            browser.get(contact_page)
                            contact_page_html = browser.page_source
                            contact_page_html_bs = BeautifulSoup(contact_page_html, 'html.parser')
                            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', contact_page_html_bs.get_text())
                            if emails:
                                email = emails[0]
                        
                        # if 'mailo:' in contact_page:
                        if 'mailto:' in contact_page:
                            email = contact_page[7:]
                            print('MAIL FROM MAILTO:', email)

                        # if 'http[s]?' not in contact_page:
                        if r'http[s]' not in contact_page:
                            contact_page = website + contact_page
                            print('CONTACT PAGE IF HREF DOES NOT HAVE HTTP:', contact_page) 
                        

                            browser.get(contact_page)
                            contact_html = browser.page_source
                            contact_html_soup = BeautifulSoup(contact_html, 'html.parser')

                            mailtos = contact_html_soup.select('a[href^=mailto]')
                            if mailtos:
                                email = mailtos[0]['href'][7:]

                            phone_numbers = re.findall(phone_pattern, contact_html_soup.get_text())
                            if phone_numbers:
                                phone_number = phone_numbers[0]
                        




            print(f'Email: {email}\nPhone Number: {phone_number}\n')


            # insertamos usuarios a la bbdd
            mycursor = mycon.cursor()
            sql = "INSERT INTO users (post_link, user_link, name, account, description, website_link, website_name, email, phone, hashtag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (new_post, user, name, account, description, website_link, website, email, phone_number, selected_value, )
            mycursor.execute(sql, val)
            mycon.commit()


        except Exception as e:
            print(e)


def extract_insert_post():
    # scrapear las paginas de cada publicacion que esta en nuestra lista y insertar los datos a la bbdd
    try:
        for post in post_list:

            browser.get('https://www.instagram.com/' + str(post))
            time.sleep(5)
            page = browser.page_source
            bsoup = BeautifulSoup(page, "html.parser")

            # user's link
            user_div = bsoup.find('div', attrs={"class":"xt0psk2"}) # cant findthis element, i think
            for user in user_div:
                user = user.find('a', attrs={"role":"link"})
                user_link = user['href']
            # print('User link:', user_link)


            # image's link
            img_div = bsoup.find('div', attrs={"class":"_aagv"})
            for img in img_div:
                imagen_src = img['src']
            # print('IMG link:', imagen_src)


            # description
            post_caption = bsoup.find('h1', attrs={"class":"_aacl _aaco _aacu _aacx _aad7 _aade"})
            if post_caption:
                caption = post_caption.text.strip()
            else:
                caption = " - "
            # print('Description:', caption.encode())


            # name for saved image
            username = str(user_link).replace('/', '')
            filename = str(username) + '--' + uuid.uuid4().hex + '.jpg'
            linkToFile = imagen_src
            localDestination = "images/" + filename
            resultFilePath, responseHeaders = urllib.request.urlretrieve(linkToFile, localDestination)
            # print('Result File Path:', resultFilePath, '\nResponse Headers:', responseHeaders)

            # converting img to blob
            with open(localDestination, 'rb') as img_file:
                binaryData = img_file.read()


            # inserting data
            mycursor = mycon.cursor()
            sql = "INSERT INTO posts (post_link, user_link, img_b, description, img_name_location, hashtag) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (post, user_link, binaryData, caption, localDestination, selected_value, )
            mycursor.execute(sql, val)
            mycon.commit()


    except Exception as e:
        print(e)


    # actualizando el foreign key
    try:
        mycursor = mycon.cursor()
        mycursor.execute("UPDATE users, posts SET posts.user_id = users.id WHERE posts.user_link = users.user_link")
        mycon.commit()
    except Exception as e:
        print(e)





#Empezar Ejecución

if __name__ == "__main__":


    ig_html(url)
    time.sleep(5)

    extract()

    extract_insert_user(url_pag)

    extract_insert_post()

    browser.quit()


