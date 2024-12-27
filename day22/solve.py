class Buyer:
    prices: dict[str, int]
    reverse_prices: dict[int, list[str]]
    
    def __init__(self, prices: dict[str, int]):
        self.prices = prices
        self.reverse_prices = dict()
        for k in prices:
            key = prices[k]
            if key in self.reverse_prices:
                self.reverse_prices[key].append(k)
            else:
                self.reverse_prices[key] = [k]
                
    def get_changes_from(self, value) -> list[str]:
        return self.reverse_prices[value]
    
    def get_changes(self):
        return self.prices.keys()
    
    def get_distinct_prices(self):
        distinct = [p for p in self.reverse_prices.keys()]
        distinct.sort(reverse=True)
        return distinct

def load(filename: str) -> list[int]:
    secrets = []
    with open(filename, 'r') as filedata:
        for line in filedata.readlines():
            secrets.append(int(line.strip()))
    return secrets

def next_secret(secret: int) -> int:
    result = secret * 64
    secret = (result ^ secret) % 16777216
    result = int(secret / 32)
    secret = (result ^ secret) % 16777216
    result = secret * 2048
    secret = (result ^ secret) % 16777216
    return secret

def sum_next_secrets(filename: str, nb_generations: int) -> int:
    secrets = load(filename)
    
    total = 0
    for secret in secrets:
        new_secret = secret
        for _ in range(0, nb_generations):
            new_secret = next_secret(new_secret)
        total += new_secret
    return total

def get_buyer(secret: int, nb_generations) -> Buyer:
    prices = dict()
    
    old_secret = secret
    change = []
    for _ in range(0, nb_generations):
        new_secret = next_secret(old_secret)
        if len(change) < 4:
            change.append((new_secret % 10) - (old_secret % 10))
            if len(change) == 4:
                key = ','.join([str(c) for c in change])
                prices[key] = new_secret % 10
        else:
            change = change[1:]
            change.append((new_secret % 10) - (old_secret % 10))
            key = ','.join([str(c) for c in change])
            if key not in prices:
                prices[key] = new_secret % 10
        old_secret = new_secret
        
    return Buyer(prices)
    

def max_bananas(filename: str, nb_generations: int) -> int:
    secrets = load(filename)
    
    buyers: list[Buyer] = []
    for secret in secrets:
        buyers.append(get_buyer(secret, nb_generations))

    changes = []
    for buyer in buyers:
        changes.extend(buyer.prices.keys())
        
    bananas = 0
    best_change = ''
    for change in set(changes):
        nb = 0
        for buyer in buyers:
            if change in buyer.prices:
                nb += buyer.prices[change]
        if nb > bananas:
            bananas = nb
            best_change = change
    
    return best_change, bananas

print("first part:")
print(sum_next_secrets('day22/sample', 10))
print(sum_next_secrets('day22/input', 2000))

print("second part:")
print(max_bananas('day22/sample2', 2000))
print(max_bananas('day22/input', 2000))