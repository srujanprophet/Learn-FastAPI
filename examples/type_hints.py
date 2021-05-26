""" Example script for python 'type hints' """


def get_full_name(first_name: str, last_name: str):
    """ Return full name given first and last name"""
    full_name = first_name.title() + " " + last_name.title()
    return full_name


print(get_full_name("zack", "hemsey"))
