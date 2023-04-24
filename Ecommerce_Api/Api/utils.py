import random
import string

class services:
    def generate_invitation_code(length=15):
        """Genera un codigo de invitacion aleatorio."""
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))