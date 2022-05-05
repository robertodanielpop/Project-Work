
from django import template

register = template.Library()



@register.filter

#filter created to deal with any bus delays
def real(a, seconds):

    #splits time in hours, minutes and seconds
    a = a.split(":")

    #seconds to be added to the actual time(a)
    seconds = int(seconds)

    #Converts everything to seconds
    second_all = seconds + (int(a[0]) * 3600) + (int(a[1]) * 60) + int(a[2])

    #Convert seconds to hours, minutes and seconds
    actual_hours = int(((second_all / 60) / 60) % 24)
    actual_minutes = int((second_all / 60) % 60)
    actual_seconds = int(second_all % 60)

    #Convert to 00:00:00 system
    if len(str(actual_hours)) == 1:
        actual_hours = str(0) + str(actual_hours)

    if len(str(actual_minutes)) == 1:
        actual_minutes = str(0) + str(actual_minutes)

    if len(str(actual_seconds)) == 1:
        actual_seconds = str(0) + str(actual_seconds)

    #Putting it all together
    actual = str(actual_hours) + ":" + str(actual_minutes) + ":" + str(actual_seconds)

    return actual

@register.filter

def integer(digit):
    return int(digit)

@register.filter

def string(word):
    return str(word.strip())