from models import db, Therapist
from app import app
import random

therapists_data = [
    {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "specialization": "Terapia Poznawczo-Behawioralna",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Specjalizuje się w leczeniu lęków i depresji.",
        "contact_email": "jan.kowalski@example.com",
        "time_slots": [
            "9:15 - 10:00",
            "10:00 - 11:00",
            "11:15 - 12:00",
            "13:00 - 14:00",
            "14:15 - 15:00",
        ],
    },
    {
        "first_name": "Anna",
        "last_name": "Nowak",
        "specialization": "Terapia Rodzinna",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Pomaga rodzinom w rozwiązywaniu konfliktów i budowaniu relacji.",
        "contact_email": "anna.nowak@example.com",
        "time_slots": [
            "10:00 - 10:30",
            "11:00 - 11:30",
            "12:00 - 12:30",
            "14:00 - 14:30",
        ],
    },
    {
        "first_name": "Piotr",
        "last_name": "Zieliński",
        "specialization": "Terapia Dzieci i Młodzieży",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Wspiera dzieci i młodzież w radzeniu sobie z trudnościami emocjonalnymi.",
        "contact_email": "piotr.zielinski@example.com",
        "time_slots": [
            "9:15 - 10:00",
            "13:30 - 14:15",
            "14:15 - 15:00",
            "15:30 - 16:15",
        ],
    },
    {
        "first_name": "Maria",
        "last_name": "Wiśniewska",
        "specialization": "Terapia Traum",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Specjalizuje się w pracy z osobami doświadczającymi PTSD.",
        "contact_email": "maria.wisniewska@example.com",
        "time_slots": [
            "10:00 - 10:30",
            "11:00 - 11:30",
            "12:00 - 12:30",
            "14:00 - 14:30",
        ],
    },
    {
        "first_name": "Krzysztof",
        "last_name": "Jabłoński",
        "specialization": "Terapia Par",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Pomaga parom w rozwiązywaniu konfliktów i poprawie komunikacji.",
        "contact_email": "krzysztof.jablonski@example.com",
        "time_slots": [
            "9:00 - 10:00",
            "10:00 - 11:00",
            "12:00 - 13:00",
            "14:00 - 15:00",
        ],
    },
    {
        "first_name": "Ewa",
        "last_name": "Lewandowska",
        "specialization": "Terapia Kryzysowa",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Wspiera osoby w sytuacjach kryzysowych.",
        "contact_email": "ewa.lewandowska@example.com",
        "time_slots": [
            "9:00 - 9:45",
            "11:00 - 12:45",
            "13:00 - 14:45",
            "16:00 - 16:45",
        ],
    },
    {
        "first_name": "Tomasz",
        "last_name": "Kaczmarek",
        "specialization": "Terapia Uzależnień",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Pomaga w walce z uzależnieniami i wspiera proces zdrowienia.",
        "contact_email": "tomasz.kaczmarek@example.com",
        "time_slots": [
            "9:00 - 10:00",
            "10:00 - 11:00",
            "12:00 - 13:00",
            "14:00 - 15:00",
        ],
    },
    {
        "first_name": "Magdalena",
        "last_name": "Piotrowska",
        "specialization": "Terapia Indywidualna",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Specjalizuje się w indywidualnym podejściu do problemów emocjonalnych.",
        "contact_email": "magdalena.piotrowska@example.com",
        "time_slots": [
            "8:00 - 9:00",
            "9:00 - 10:00",
            "13:15 - 14:00",
            "15:15 - 16:00",
        ],
    },
    {
        "first_name": "Robert",
        "last_name": "Wójcik",
        "specialization": "Terapia Grupowa",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Organizuje i prowadzi terapie grupowe dla osób z podobnymi problemami.",
        "contact_email": "robert.wojcik@example.com",
        "time_slots": [
            "10:20 - 11:00",
            "11:20 - 12:00",
            "13:20 - 14:00",
            "14:20 - 15:00",
        ],
    },
    {
        "first_name": "Agnieszka",
        "last_name": "Szymańska",
        "specialization": "Terapia Psychodynamiczna",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "biography": "Wspiera pacjentów w głębokim zrozumieniu ich emocji i zachowań.",
        "contact_email": "agnieszka.szymanska@example.com",
        "time_slots": [
            "9:00 - 10:00",
            "11:00 - 12:00",
            "12:00 - 13:00",
            "14:00 - 15:00",
        ],
    },
]

def seed_therapists():
    with app.app_context():
        for therapist in therapists_data:
            new_therapist = Therapist(
                first_name=therapist["first_name"],
                last_name=therapist["last_name"],
                specialization=therapist["specialization"],
                rating=therapist["rating"],
                biography=therapist["biography"],
                contact_email=therapist["contact_email"],
                time_slots=therapist["time_slots"],
            )
            db.session.add(new_therapist)
        db.session.commit()
        print("Therapists table has been seeded successfully!")

if __name__ == "__main__":
    seed_therapists()
