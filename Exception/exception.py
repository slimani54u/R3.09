def divEntier(x: int, y: int) -> int:
    try:
        if x<0 or y<0:
            raise ValueError("veuillez entre un nombre positif")
        if y==0:
            raise ValueError("le diviseurt ne peux etre egale a 0")
        if x < y:
            return 0
        else:
            x = x - y
    except:
        print("")
    return divEntier(x, y )+1





if __name__ == '__main__':
    print(divEntier(18,0))