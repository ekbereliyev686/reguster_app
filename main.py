import sqlite3
import re
import bcrypt 
  

# # Python SQL vasitəsilə Register app qurun

# # Proqram soruşur:
   
# #     Daxil edin :
# #         username,first_name,last_name,email,password
# #         Daxil edilmiş məlumatlar databazaya otursun

# # Qeyd:

# # Password daxil edildikdə əlavə təsdiq passwordu soruşsun əgər 2 password bir-birinə uymursa error mesajı qaytarsın
# # Təkrar emailin databazaya oturmasının qarşısını alın
# # Bazada mövcud olan email təkrar daxil edildikdə error mesajı qaytarsın
# # Password və Email düzgün daxil edilmədikdə proqram sonlanmadan yenidən soruşsun
# # Password databazaya təhlükəsizliyə görə şifrələnmiş şəkildə düşsün
# # Hər şey qaydasındadırsa success mesajı qaytarsın və məlumatlar databazaya otursu

app=sqlite3.connect("data.db")
register=app.cursor()


def create_table():
    register.execute("CREATE TABLE IF NOT EXISTS register (username TEXT,first_name TEXT,last_name TEXT,email TEXT,password TEXT) ")
    app.commit()

create_table()



def check(email): 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'  
    email=re.fullmatch(regex, email)
    return email
 

def select_table():
    b=register.execute(F"SELECT * FROM register")
    return b.fetchall()
    
def select_email():
    select=register.execute("SELECT email FROM register ")
    select=''.join(map(str,select.fetchall()))
    return select



def insert_table(username, first_name, last_name, email, password):
    query = "INSERT INTO register(username, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)"
    user_data = (username, first_name, last_name, email, password)
    register.execute(query, user_data)
    app.commit()
    # if check(email):
    #     if password == password2:
    #         app.commit()
    #         print("Ugurlu")
    #     else:
    #         print("Parol eyni deyil")
    # else:
    #     print("email duzgun qeyd edin")


            



        
def secret(password):

    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hash = bcrypt.hashpw(bytes, salt) 
    secret_password=hash
    return secret_password



while True:
    username=input("Login daxil edin :")
    first_name=input("Adiniz axil edin :")
    last_name=input("Soyadiniz axil edin :")
    email=input("Email adresiniz daxil edin :")
    password=input("Sifrenizi daxil edin :")
    password2=input("Sifreni tesdiq ucun tekrar daxil edin: ")

    

    if len(select_table())==0:
        if check(email):
            if password == password2:
                secret_password=secret(password)
                insert_table(username,first_name,last_name,email,secret_password)
                print("Ugurlu")
                break
            else:
                print("Parol eyni deyil")
                
        else:
            print("email duzgun qeyd edin")
            
            

    else:
        
        if email not in select_email():
            if password == password2:
                secret_password=secret(password)
                insert_table(username,first_name,last_name,email,secret_password)
                print("Ugurlu")
                break
            else:
                print("Parol eyni deyil")
        else:
            print("Bele bir email movcuddur.")

    

app.close()





  
