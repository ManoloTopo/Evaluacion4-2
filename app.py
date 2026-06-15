from flask import Flask, render_template
import socket

app = Flask(__name__)
HOST = "192.168.101.5"  ## Ip del servidor TCP
PORT = 12345           ## Puerto del servidor TCP

def leer_sensor():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0) 
            s.connect((HOST, PORT))
            data = s.recv(1024).decode().strip()
            print("RECIBIDO TCP:", data)
            
            ejeX, ejeY = data.split(',')
            ejeX = float(ejeX.replace('X:', '').strip())
            ejeY = float(ejeY.replace('Y:', '').strip())
            
            # --- CORRECCIÓN DE INVERSIÓN ---
            # Multiplicamos por -1 para dar vuelta el sentido del eje X
            ejeX = ejeX * -1 
            # -------------------------------
            
            return ejeX, ejeY

    except socket.timeout:
        print("ERROR: El dispositivo sensor no respondió a tiempo (Timeout).")
        return 0.0, 0.0
    except Exception as e:
        print("ERROR:", e)
        return 0.0, 0.0

# 1. RUTA PRINCIPAL: Envía datos a la Matriz 4x4 (EjeXY.html)
@app.route('/')
def index():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'EjeXY.html',
        ejeX=ejeX,
        ejeY=ejeY
    )

# 2. RUTA EJE X: Envía datos a la barra horizontal 4x1 (EjeX.html)
@app.route('/eje_x')
def vista_eje_x():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'EjeX.html',
        ejeX=ejeX,
        ejeY=ejeY
    )

# 3. RUTA EJE Y: Envía datos a la columna vertical 1x4 (EjeY.html)
@app.route('/eje_y')
def vista_eje_y():
    ejeX, ejeY = leer_sensor()
    return render_template(
        'EjeY.html',
        ejeX=ejeX,
        ejeY=ejeY
    )

if __name__ == '__main__':
    # El servidor corre en el puerto 5000 de Flask de forma local
    app.run(host='0.0.0.0', port=5000, debug=True)
