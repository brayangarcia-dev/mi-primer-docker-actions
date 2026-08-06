import os
from flask import Flask
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def conectar_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def inicio():
    try:
        conn = conectar_db()
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS visitas (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

        cur.execute("INSERT INTO visitas DEFAULT VALUES;")
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM visitas;")
        total_visitas = cur.fetchone()[0]

        cur.close()
        conn.close()

        return f"<h1>¡Hola DevOps!</h1><p>Esta página se conecta a PostgreSQL.</p><p>Total de visitas registradas en la base de datos: <b>{total_visitas[0]}</b></p>"
    except Exception as e:
        return f"<h1>Error de conexión</h1><p>{str(e)}</p>"

if __name__== '__main__':
    app.run(host='0.0.0.0', port=5000)
