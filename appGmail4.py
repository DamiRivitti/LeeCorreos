import imaplib
import email
import smtplib
import mysql.connector
import re


# Declaro variables que almacenan los datos del usuario
username = 'xxxxx@gmail.com'
password = 'xxxxx'
# Gmai necesita un protoclo seguro IMAP4_SSL
mail = imaplib.IMAP4_SSL("imap.gmail.com")

# Le paso las variables a la funcion de login
mail.login(username, password)
# Selecciono la casilla de entrada
mail.select("inbox")
mail.list()
# Verifico los ids de los correos, que serían items
result, data = mail.uid('search', None, "ALL")
# coloco los items dentro de una lista, para poder accederlos por separado luego
inbox_item_list = data[0].split()
    # Por ejemplo accedo al ultimo id recibido , por eso -1
    most_recent = inbox_item_list[-1]
    # o Por ejemplo accedo al id más viejo
    # oldest = inbox_item_list[0]
    result2, email_data = mail.uid('fetch', most_recent, '(RFC822)')
    # Los datos estan en bytes, los cambio a string. Se hace con raw. Lo hago en este caso con el primer id
    raw_email = email_data[0][1].decode("utf-8")
    # ahora cambio este mensaje a un objeto de correo de python
    email_message = email.message_from_string(raw_email)
    # Ahora puedo imprimir distintos atributos del objeto, es decir del correo
    print(dir(email_message))
    email_message['To']
    email_message['From']
    email_message['Subject']
    email_message['date']
    email_message['message-id']
    # Para acceder al contenido necesito el payload, pero este mismo esta dividido en 2 partes, puede ser una lista o texto plano
    email_message.get_payload()
    print(email_message.get_payload(1))
    email_message = email.message_from_string(raw_email)

    # Busco la palabra DevOps en el payload
     x= email_message.get_payload(1)
     x = email_data[0][1].decode("utf-8")
     # Expresion regular para buscar
     y = re.search('DevOps',x)
     # y = re.findall('DevOps',x)
     # Si hay match es decir que encuentra la palabra hago lo siguiente
     if y:
         print(y.group())
        # Guardo la fecha del mail en una variable
        fecha = email_message['date']
        # Guardo quien envia el correo en una variable
        de = email_message['From']
        # Guardo asunto del correo en una variable
        asunto = email_message['Subject']

        id = email_message['message-id']
        # Conexion a MySQL
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="scarparo10",
        database="correos")
        mycursor = mydb.cursor()

        # Defino el query
        sql = "INSERT INTO devops_emails (Fecha, De, Asunto) VALUES (%s, %s, %s)"
        # Le paso el contenido de las variables
        val = (fecha, de, asunto)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
