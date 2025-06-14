import re 
from Baseapp.models import Profile
import random
from rest_framework.response import Response
from rest_framework import status
def generate_profile_id():
    while True:
        profile_id = f'USRACC-{random.randint(1000, 999999)}'
        try:
            Profile.objects.get(profile_id=profile_id)
        except Profile.DoesNotExist:
            return profile_id
        
def checkpass(pwd):
    if len(pwd) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', pwd):
        return "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', pwd):
        return "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', pwd):
        return "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd):
        return "Password must contain at least one special character."
    return None

def check_field(request, *args):
    for field in args:
        if field not in request.data or not request.data.get(field):
            return Response({"error": f"{field} is required.", "status_code": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    return None  # Return only if all fields are present





