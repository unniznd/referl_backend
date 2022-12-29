from django.utils import timezone
import uuid

def mark_expired(query_set):
    for query in query_set:
        if query.current_status == 1:
            if((timezone.now() - query.updated_at).days>query.validity):
                query.current_status = 2
                query.save()

def get_referalcode():
    return str(uuid.uuid4())[:6]