Cómo ejecutar y probar el proyecto:

Cambiar los valores de
broker_props = {
    "solace.messaging.transport.host": "wss://mr-connection-yf1llfk6z2n.messaging.solace.cloud:443",
    "solace.messaging.service.vpn-name": "global_proyect",
    "solace.messaging.authentication.scheme.basic.username": "solace-cloud-client",
    "solace.messaging.authentication.scheme.basic.password": "XD"
}
por tus datos propios de Solace. 

Para el Proyecto se tendra que realizar lo siguiente:

## Instrucciones de Instalación y Ejecución

1. **Crear el entorno virtual:**
   ```bash
   python -m venv venv
Activar el entorno virtual:

En Windows: .\venv\Scripts\activate

En Mac/Linux: source venv/bin/activate

Instalar dependencias:

Bash
pip install -r requirements.txt
Ejecutar el proyecto:
Para simular el sistema en tiempo real, abre 3 terminales distintas. Asegúrate de activar el entorno virtual en las tres y ejecuta los scripts en este orden:

Terminal 1: python carrier_dashboard.py

Terminal 2: python client_dashboard.py

Terminal 3: python dispatcher.py (Este enviará el payload de prueba a las colas).

Observa cómo al ejecutar el dispatcher, los mensajes se rutean instantáneamente a las consolas correspondientes dependiendo de las fechas que configures en el JSON de prueba.
