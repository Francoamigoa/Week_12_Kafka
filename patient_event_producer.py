import time
import json
import uuid
import random
from datetime import datetime
from kafka import KafkaProducer


def generate_patient_event():
    """
    Generates synthetic patient visit data for a single hospital.
    """

    # Especialidades del hospital
    specialties = [
        "Emergency",
        "Cardiology",
        "Trauma",
        "Pediatrics",
        "Neurology",
        "Oncology",
        "Internal Medicine",
    ]

    # Estado del paciente en el flujo asistencial
    patient_statuses = [
        "Waiting",
        "In Treatment",
        "Discharged",
        "Left Without Being Seen",
    ]

    # Tipo de seguro
    insurance_types = [
        "Medicare",
        "Medicaid",
        "Private Insurance",
        "Self-pay",
        "Charity Care",
    ]

    specialty = random.choice(specialties)
    status = random.choice(patient_statuses)
    insurance = random.choice(insurance_types)

    # Tiempo de espera en minutos, razonable
    waiting_time = round(random.uniform(5, 180), 2)

    # Nivel de triage ESI 1 a 5
    triage_level = random.randint(1, 5)

    event = {
        "event_id": str(uuid.uuid4())[:8],
        "status": status,
        "specialty": specialty,
        "waiting_time": waiting_time,
        "timestamp": datetime.now().isoformat(),
        "hospital_name": "General Hospital",
        "insurance": insurance,
        "triage_level": triage_level,
    }

    return event


def run_producer():
    """Sends synthetic patient events to the 'patient_events' Kafka topic."""
    try:
        print("[Producer] Connecting to Kafka at localhost:9092...")
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            request_timeout_ms=30000,
            max_block_ms=60000,
            retries=5,
        )
        print("[Producer] ✓ Connected to Kafka successfully!")

        count = 0
        while True:
            event = generate_patient_event()
            print(f"[Producer] Sending patient event #{count}: {event}")

            producer.send("patient_events", value=event)
            producer.flush()
            count += 1

            time.sleep(random.uniform(0.5, 1.5))

    except Exception as e:
        print(f"[Producer ERROR] {e}")
        import traceback

        traceback.print_exc()
        raise


if __name__ == "__main__":
    run_producer()
