from .model import Decat


client = Decat()


def decat(string):
    client.decat(string)
    return client.out
