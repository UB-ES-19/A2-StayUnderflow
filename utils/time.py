from urllib.request import urlopen
from django.utils import timezone

def get_time_online():
    # Get the time utc+0 via online request
    return urlopen('http://just-the-time.appspot.com/').read().strip().decode('utf-8')

def get_time_local():
    # Get the local time from the server clock
    return timezone.now