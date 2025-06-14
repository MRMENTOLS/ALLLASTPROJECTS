from models.ticket import Ticket, SessionLocal

def save_ticket(user_id, full_name, question, department):
    session = SessionLocal()
    new_ticket = Ticket(
        user_id=user_id,
        full_name=full_name,
        question=question,
        department=department
    )
    session.add(new_ticket)
    session.commit()
    session.close()