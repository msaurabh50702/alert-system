import requests
import urllib3
from bs4 import BeautifulSoup


fo = open('urls.txt','w+')

urllib3.disable_warnings()

first_name=last_name=email=unm_telegram = None
send_url = "http://alert-system-2gud.herokuapp.com/"

while True:
    first_name = input("Enter Your First Name : ")
    if first_name != "" and first_name is not None:
        break

while True:
    last_name = input('Enter Your Last Name : ')
    if last_name != "" and last_name is not None:
        break
while True:
    email = input('Enter your Email ID : ')
    if email != "" and email is not None:
        break
unm_telegram = input('Enter your Telegram Username (optional) : ')

cnt = 1

dict_db = {'first_name':first_name,'last_name':last_name,'email':email,'telegram':unm_telegram}
product_db_list = []

print("+-------------------------------------------------+ Add Product's +-------------------------------------------------+")
while True:
    product_url = None
    prod_nm = None
    product_name = input("Enter Product Name : ")
    product_list_url = "https://www.2gud.com/search?q="+ product_name.replace(" ",'%20').lower() +"&otracker=search&otracker1=search&marketplace=EMERALD&as-show=off&as=off"

    product_list_page = requests.post(product_list_url,verify=False)
    soup = BeautifulSoup(product_list_page.content, 'html.parser')
    try:
        print("++++++++++++++++++++++++ Product Found ++++++++++++++++++++++++")
        prod_nm = str(soup.find(class_ = '_2cLu-l').text)
        print(prod_nm)
        print(soup.find(class_="_1rcHFq").text)
        print("Quality :- ",soup.find(class_ = 'sc-bZQynM nlXJc').text,"\n")
        cnf = input("Confirm Product (y/n) :")
        if cnf in ['n','N']:
            ch = input("Press.1 to enter Product URL (any key to confinue) : ")
            if ch != '1':
                continue
            elif ch == '1':
                usr_url = input("Enter URL of Product : ")
                try:
                    usr_product = requests.post(usr_url,verify=False)
                    usr_product_soup = BeautifulSoup(usr_product.content, 'html.parser')
                    prod_nm = usr_product_soup.find(class_ = '_35KyD6').text
                    print("Product Found : ", prod_nm)
                    product_url = usr_url
                except Exception as e:
                    print("Error : ",e)
        else:
            product_url = "2gud.com" + soup.find(class_ = '_2cLu-l').get('href').replace(" ",'')


    except Exception as e:
        if soup.find(class_ = 'DUFPUZ').text == 'Sorry, no results found!':
            print('\nSorry, no results found!')
            print('Try another product\n')
            usr_url_ch = input('if you have url of product PRESS.1 to Enter URL :')
            if usr_url_ch == '1':
                usr_url = input('Enter URL : ')
                try:
                    usr_product = requests.post(usr_url,verify=False)
                    usr_product_soup = BeautifulSoup(usr_product.content, 'html.parser')
                    prod_nm = usr_product_soup.find(class_ = '_35KyD6').text
                    print("Product Found : ", prod_nm)
                    product_url = usr_url
                except Exception as e:
                    print("Error : ",e)
        #print("Error : ",e)

    if product_url is not None:
        fo.write(product_url+"\n")
        dict_db["purl"]=product_url
        dict_db['product_name'] = prod_nm
        res = requests.post(send_url+"insert/",dict_db)
        product_db_list.append(res.json())
        cnt += 1
        nm = ""

        if cnt-1 == 1:
            nm = 'Product'
        else:
            nm = "Product's"
        print("+-------------------------------------------------+ "+str(cnt-1)+" "+str(nm)+" Added +-------------------------------------------------+")
    add_more_products = input("Do you want to add more products to search (y/n): ")
    print()
    if add_more_products in ['n','N']:
        fo.close()
        print("Request ID \t\t\t Product Name")
        for id in product_db_list:
            res = requests.get(send_url+"disp/"+id)
            print(id +"\t"+(res.json()[0])['product_name'])
        print("\n+-------------------------------------------------+ End +-------------------------------------------------+")
        break


