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

class ClientMessageHandler(MessageHandler):
    def on_message(self, message):
        payload = message.get_payload_as_string()
        data = json.loads(payload)
        status = data.get('status')
        
        print("\n" + "-"*40)
        print(f"🔔 ACTUALIZACIÓN DE ESTADO - Orden: {data.get('shipperOrderId')}")
        if status == "Accepted":
            print(f"✅ ESTADO: {status}")
        else:
            print(f"❌ ESTADO: {status}")
        print(f"📝 NOTA: {data.get('notes')}")
        print("-"*40 + "\n")

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
        
    messaging_service.connect()
    
    topic = TopicSubscription.of("Q/clientes/respuestas")
    receiver = messaging_service.create_direct_message_receiver_builder().with_subscriptions([topic]).build()
    
    receiver.start()
    print("Dashboard de Clientes iniciado. Esperando actualizaciones de solicitudes...")
    
    receiver.receive_async(ClientMessageHandler())
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cerrando dashboard...")
        receiver.terminate()
        messaging_service.disconnect()

if __name__ == "__main__":
    main()