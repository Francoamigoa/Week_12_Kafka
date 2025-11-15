import json
import psycopg2
from kafka import KafkaConsumer


def run_consumer():
    """Consumes patient events from Kafka and inserts them into PostgreSQL."""
    print("[Consumer] Connecting to Kafka at localhost:9092...")
    consumer = KafkaConsumer(
        "patient_events",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",  # puedes cambiar a "latest" si quieres ignorar mensajes viejos
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        group_id="patient-events-consumer-group",
    )
    print("[Consumer] ✓ Connected to Kafka")

    print("[Consumer] Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        dbname="kafka_db",
        user="kafka_user",
        password="kafka_password",
        host="localhost",
        port="5433",
    )
    conn.autocommit = True
    cur = conn.cursor()
    print("[Consumer] ✓ Connected to PostgreSQL")

    # Tabla con nombres "médicos"
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patient_events (
            event_id VARCHAR(50) PRIMARY KEY,
            status VARCHAR(50),
            specialty VARCHAR(50),
            waiting_time NUMERIC(10,2),
            timestamp TIMESTAMP,
            hospital_name VARCHAR(100),
            insurance VARCHAR(50),
            triage_level INTEGER
        );
        """
    )
    print("[Consumer] ✓ Table 'patient_events' ready.")
    print("[Consumer] 🎧 Listening for patient events...\n")

    message_count = 0
    for message in consumer:
        try:
            event = message.value

            # Compatibilidad con mensajes antiguos (category/value/city/payment_method/discount)
            specialty = event.get("specialty", event.get("category", "Unknown"))
            waiting_time = event.get("waiting_time", event.get("value", 0.0))
            hospital_name = event.get(
                "hospital_name", event.get("city", "General Hospital")
            )
            insurance = event.get("insurance", event.get("payment_method", "Unknown"))
            triage_level = event.get("triage_level", event.get("discount", 0))

            insert_query = """
                INSERT INTO patient_events 
                (event_id, status, specialty, waiting_time, timestamp, hospital_name, insurance, triage_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING;
            """
            cur.execute(
                insert_query,
                (
                    event["event_id"],
                    event["status"],
                    specialty,
                    waiting_time,
                    event["timestamp"],
                    hospital_name,
                    insurance,
                    int(triage_level),
                ),
            )
            message_count += 1
            print(
                f"[Consumer] ✓ #{message_count} Inserted event {event['event_id']} | "
                f"{specialty} | status={event['status']} | triage={triage_level}"
            )

        except Exception as e:
            print(
                f"[Consumer ERROR] Failed to process event: {e} | raw event={message.value}"
            )
            continue


if __name__ == "__main__":
    run_consumer()
