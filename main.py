''' @Kennedy Molina Q
    02/07/2022
'''

import pymysql # pip install pymysql

user_table="""
    CREATE TABLE users(
        id INT PRIMARY KEY autoincrement ,
        username VARCHAR(50),
        email   VARCHAR(50),
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""
def create_user(connect ,cursor):
    """A) Crear usuario"""
    username = input("Ingrese un username: ")
    email = input("Ingrese un email: ")

    query = "INSERT INTO users (username, email) VALUES (%s , %s)"
    valor=(username, email)

    cursor.execute(query, valor)
    connect.commit()

    print("Usuario creado correctamente")

def list_user(connect ,cursor):
    """B) Mostrar usuario"""
    query = "SELECT * FROM users"

    cursor.execute(query)

    for i in cursor.fetchall():
        print(i)
    print("Lista de usuarios correctamente")

def update_user(connect ,cursor):
    """C) Actualizar usuario"""
    # Validamos si el usuario existe
    id = input("Ingresar ID a actualizar: ")
    query = f"SELECT * FROM users WHERE id={id}"

    cursor.execute(query)
    user_exist = cursor.fetchone()
    print(user_exist)
    if user_exist:
        username = input("Ingrese nuevo username: ")
        email = input("Ingrese nuevo email: ")
        query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
        valor = (username, email, id)

        cursor.execute(query, valor)
        connect.commit()
        print("Actualización correcta")

    else:
        print("Usuario no existe")

   
    

def delete_user(connect ,cursor):
    """D) Borrar usuario"""
    # Validamos si el usuario existe
    id = input("Ingresar ID a borrar: ")
    query = f"SELECT * FROM users WHERE id={id}"

    cursor.execute(query)
    user_exist = cursor.fetchone()
    print(user_exist)
    if user_exist:

        query = "DELETE FROM users WHERE id = %s"
        Valor=(id)

        cursor.execute(query,Valor)
        connect.commit()
        print("Usuario eliminado correctamente")
    else:
        print("Usuario no exites")


def default(*args):
    print("""INGRESAR OPCION CORRECTA""")





if __name__=='__main__':

    options={
        'a': create_user,
        'b': list_user,
        'c': update_user,
        'd': delete_user
    }

    try:
        connect=pymysql.connect(host='localhost', 
                                user= 'root', 
                                passwd='123456', 
                                db='db_python'
        ) # Es una contraseña temporal, más despacio velocista
        
        
        cursor=connect.cursor()

        while True:
            # Recorremos las opciones y las imprimos desde las funciones
            for function in options.values():
                print(function.__doc__)
            
            print("quit para salir")
            # Usuario seleccionara un opcion y validando la salida
            option=input("Selecciona una funcion valida: ").lower()
            if option == 'quit' or option == 'q':
                break
            # Llamamos a la funcion que se escogio y validamos opciones no validas
            function = options.get(option, default())
            function(connect ,cursor)
            

    except pymysql.err.OperationalError as err:
        print("*****Error al conectar a la DB")
        print(err)

    finally:
        cursor.close()
        connect.close()
