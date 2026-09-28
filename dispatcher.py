import os
import certifi
import json
from datetime import datetime, date
from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic import Topic
from solace.messaging.config.transport_security_strategy import TLS

broker_props = {
    "solace.messaging.transport.host": "wss://mr-connection-yf1llfk6z2n.messaging.solace.cloud:443",
    "solace.messaging.service.vpn-name": "global_proyect",
    "solace.messaging.authentication.scheme.basic.username": "solace-cloud-client",
    "solace.messaging.authentication.scheme.basic.password": "XD"
}

def validate_payload(payload):
    try:
        pickup_date = datetime.strptime(payload['pickupDate'], '%Y-%m-%d').date()
        delivery_date = datetime.strptime(payload['deliveryDate'], '%Y-%m-%d').date()
        today = date.today()
        now = datetime.now()

        if pickup_date < today:
            return False, "Pickup date cannot be earlier than the current date."
        if pickup_date == today and now.hour >= 15:
            return False, "Pickup cannot be scheduled today after 3:00 p.m."
        if delivery_date <= pickup_date:
            return False, "Delivery date must be at least one day after pickup date."
            
        return True, "Valid"
    except Exception as e:
        return False, f"Invalid date format: {str(e)}"

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
    publisher = messaging_service.create_direct_message_publisher_builder().build()
    publisher.start()

    topic_carriers = Topic.of("Q/pedidos/disponibles")
    topic_clients = Topic.of("Q/clientes/respuestas")

    payload_entrada = {
        "shipperOrderId": "6600111",
        "pickupDate": "2026-09-28", 
        "deliveryDate": "2026-09-29",
        "price": 900,
        "stops": [{"stopNumber": 1, "city": "Milford", "state": "MA", "postalCode": "01757"}],
        "vehicles": [{"year": "2010", "make": "Toyota", "model": "Corolla"}]
    }

    is_valid, msg_error = validate_payload(payload_entrada)

    if is_valid:
        outbound_msg_carrier = messaging_service.message_builder().build(json.dumps(payload_entrada))
        publisher.publish(destination=topic_carriers, message=outbound_msg_carrier)
        print("[+] Payload válido enviado a transportistas.")

        client_response = {
            "shipperOrderId": payload_entrada["shipperOrderId"],
            "status": "Accepted",
            "notes": "You will receive an email when a carrier accepts this dispatch request"
        }
    else:
        client_response = {
            "shipperOrderId": payload_entrada["shipperOrderId"],
            "status": "Cancelled",
            "notes": msg_error
        }
        print(f"[-] Payload inválido. Motivo: {msg_error}")

    outbound_msg_client = messaging_service.message_builder().build(json.dumps(client_response))
    publisher.publish(destination=topic_clients, message=outbound_msg_client)
    print("[+] Respuesta enviada al dashboard del cliente.")

    publisher.terminate()
    messaging_service.disconnect()

if __name__ == "__main__":
    main()