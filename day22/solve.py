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

print("first part:")
print(sum_next_secrets('day22/sample', 10))
print(sum_next_secrets('day22/input', 2000))