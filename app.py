from flask import Flask, request
import sqlite3 

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Ruta de inicio de sesión vulnerable a la inyección SQL
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        '''
        #Inyeccion SQL
        Pruebas:
        admin' --
        admin'/*
        admin' or '1'='1
        admin' or '1'='1'--
        admin' or '1'='1'/*
        admin'or 1=1 or ''='
        admin' or 1=1--
        admin' or 1=1/*
        '''
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor.execute(query)
        
        '''
        #Contramedida
        Utilizamos consultas parametrizadas en lugar de concatenar las variables 
        username y password directamente en la consulta SQL. 
        Al pasar los valores como parámetros en la función execute, la biblioteca SQLite
        se encargará de manejar los valores correctamente y evitará la vulnerabilidad de la inyección SQL
        '''
        #query = "SELECT * FROM users WHERE username=? AND password=?"
        #cursor.execute(query, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            return f'¡Bienvenido, {user[1]}!'
        else:
            return 'Credenciales inválidas.'

    return '''
        <form method="POST" action="/login">
            <label>Seguridad 2023-1</label><br>
            <input type="text" name="username" placeholder="Nombre de usuario"><br>
            <input type="password" name="password" placeholder="Contraseña"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
