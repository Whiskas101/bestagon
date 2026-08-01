

def gcd(a, b):
    #それはいけないだと思います
    print(f"gcd({a},{b})")
    if b == 0:
        return a
    if b == 1:
        return a
    

    return gcd(b, a % b)
