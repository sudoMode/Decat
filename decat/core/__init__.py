from decat.core.model import Decat


client = Decat()


def decat(string):
    client.decat(string)
    return client.out


if __name__ == '__main__':
    i = 'dummy.email1234@gmail.com'
    o = decat(i)
    print(f'In: {i}\nOut: {o}')
