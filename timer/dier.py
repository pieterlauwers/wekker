class Dier:
    def __init__(self,name):
        self.name = name

if __name__ == '__main__':
    dierenriem = []
    k = Dier('kat')
    dierenriem.append(k)
    h = Dier('hond')
    dierenriem.append(h)
    h.name = 'boxer'
    k.name = 'minoes'
