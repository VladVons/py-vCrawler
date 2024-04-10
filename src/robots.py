#https://tamethebots.com/tools/robotstxt-checker

def Test1():
    q1 = Robots.can_fetch('/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC', '*')
    q2 = Robots.can_fetch('http://oster.com.ua/c600240/c637000/c663700/p685662.html?sort=p.price&order=ASC', '*')
    q3 = Robots.can_fetch('http://oster.com.ua/index.php/?route=account/login', '*')
    q4 = Robots.can_fetch('http://oster.com.ua/index.php?route=account1/login&key=1', '*')


def Test2():
    import json
    from Inc.Util.Obj import GetTree

    with open('kts.json', 'r') as F:
        ParsedData = json.load(F)


    print(ParsedData)
Test2()
