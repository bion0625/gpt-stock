portfolio = {}

while True:
    action = input("1. 종목 추가 2. 포트폴리오 보기 3. 종료 > ")

    if action == "1":
        name = input("종목명 입력: ")
        amount = int(input("보유 수량 입력: "))
        portfolio[name] = portfolio.get(name, 0) + amount
    elif action == "2":
        for name, amount in portfolio.items():
            print(f"{name}: {amount}주")
    elif action == "3":
        print("종료합니다.")
        break
    else:
        print("잘못된 입력입니다.")