import os
import certifi
import json
import time
from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.receiver.message_receiver import MessageHandler
from solace.messaging.config.transport_security_strategy import TLS

broker_props = {
    "solace.messaging.transport.host": "wss://mr-connection-yf1llfk6z2n.messaging.solace.cloud:443",
    "solace.messaging.service.vpn-name": "global_proyect",
    "solace.messaging.authentication.scheme.basic.username": "solace-cloud-client",
    "solace.messaging.authentication.scheme.basic.password": "XD"
}

class CarrierMessageHandler(MessageHandler):
    def on_message(self, message):
        payload = message.get_payload_as_string()
        data = json.loads(payload)
        print("\n" + "="*50)
        print("🚛 NUEVA CARGA DISPONIBLE 🚛")
        print(f"ID Orden: {data.get('shipperOrderId')}")
        print(f"Pago: ${data.get('price')}")
        print(f"Recogida: {data.get('pickupDate')} | Entrega: {data.get('deliveryDate')}")
        print(f"Vehículos: {len(data.get('vehicles', []))} auto(s)")
        print("="*50 + "\n")

def main():
    cert_dir = os.path.dirname(certifi.where()).replace('\\', '/')
    
    transport_security = TLS.create().with_certificate_validation(
        False, 
        validate_server_name=False, 
        trust_store_file_path=cert_dir
    )

    messaging_service = MessagingService.builder().from_properties(broker_props) \
        .with_transport_security_strategy(transport_security) \
        .build()
        
    messaging_service.connect() # Esta es la famosa línea 43 que ahora conectará correctamente
    
    topic = TopicSubscription.of("Q/pedidos/disponibles")
    receiver = messaging_service.create_direct_message_receiver_builder().with_subscriptions([topic]).build()
    
    receiver.start()
    print("Dashboard de Transportistas iniciado. Esperando cargas...")
    
    receiver.receive_async(CarrierMessageHandler())
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cerrando dashboard...")
        receiver.terminate()
        messaging_service.disconnect()

if __name__ == "__main__":
    main() # Esta es la línea 62