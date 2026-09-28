Cómo ejecutar y probar el proyecto:

Cambiar los valores de
broker_props = {
    "solace.messaging.transport.host": "wss://mr-connection-yf1llfk6z2n.messaging.solace.cloud:443",
    "solace.messaging.service.vpn-name": "global_proyect",
    "solace.messaging.authentication.scheme.basic.username": "solace-cloud-client",
    "solace.messaging.authentication.scheme.basic.password": "XD"
}

por tus datos propios de Solace. 

Abre tres terminales independientes.

En la primera, ejecuta python carrier_dashboard.py.

En la segunda, ejecuta python client_dashboard.py.

En la tercera, ejecuta python dispatcher.py.

Observa cómo al ejecutar el dispatcher, los mensajes se rutean instantáneamente a las consolas correspondientes dependiendo de las fechas que configures en el JSON de prueba.
