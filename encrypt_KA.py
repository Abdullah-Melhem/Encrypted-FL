from charm.toolbox.integergroup import IntegerGroup
import hashlib
import random

# this function convert the float to integer
def float_to_int_fnc(number,accuracy=6):
    if isinstance(number,float):
        return int(10**accuracy * number)
    if isinstance(number,int):
        return number

# This function converts an integer back to a float
def int_to_float_fnc(number, accuracy=6):
    if isinstance(number, int):
        return number / (10**accuracy)
    if isinstance(number, float):
        return number



# Initialize the group
group = IntegerGroup()
# select the length of p (number of bit)
group.paramgen(6)

# Group parameters
p = int(group.p)  # Prime modulus
q = int(group.q)  # Group order
g = int(group.randomGen())  # Generator

# Number of participants
N = 10

# Generate random secret keys (s_i)
# weights (w_i), and model parameters (p_i^t[m]), i: participant number, t: FL round

# this list will contain (Si, Wi, Pi_t) for each participant
participants = []

# this loop defines the parameters randomly
for i in range(N):
    # Wi = int(group.random() % q)  # Weight strictly greater than 0
    w = random.random()
    Wi = float_to_int_fnc(w)
    # this loop to ensure Wi is not zero
    while Wi == 0:
        # Wi = int(group.random() %q)
        Wi = float_to_int_fnc(random.random())

    Si = int(group.random() % q)  # Secret key
    # Pi = int(group.random() % p)  # Parameter mod p
    Pi = float_to_int_fnc(random.random())
    participants.append((Si, Wi, Pi))


# Round identifier (ℓt) and its hash (Uℓt)
ℓt = int(group.random() % p)  # Round identifier
Uℓt = int(hashlib.sha256(str(ℓt).encode()).hexdigest(), 16) % q  # Uℓt = H(ℓt) mod q
# Uℓt = int(group.random()) % q  # Uℓt = H(ℓt) mod q

# Formula 1: Compute the Ciphertext (Ci[p[m]]) for each participant
ciphertexts = []
for Si, Wi, Pi in participants:
    power_G = (Si * Uℓt) % q  # Compute (si * Uℓt) mod q
    Ci_m = (pow(g, power_G + Pi, p)) % p  # Compute Ci[p[m]] = g^^(si * Uℓt + Pi_t) mod p
    ciphertexts.append(Ci_m)

# Compute Aggregator Key (AKas)=g^(Σ Si * Wi) mod p

weighted_sum = sum(si * wi for si, wi, _ in participants) % q  # Σ si * wi mod q
AKas = pow(g, weighted_sum, p)  # g^(Σ si * wi) mod p

# Compute the product ∏ (C[p[m]])^wi (top of the division)
top = 1
for Ci_m, (_, Wi, _) in zip(ciphertexts, participants):
    top = (top * pow(Ci_m, Wi, p)) % p  # Top is the product of (Ci[p[m]])^w_i mod p

# Compute (AKas)^(uℓt) mod p (Bottom of the division)
bottom = pow(AKas, Uℓt, p)  # (AKas)^(uℓt) mod p

# Final result Y (computed by the AS)
Y = (top * pow(bottom, p - 2, p)) % p  # Multiply by modular inverse of bottom


# Compute g^(Σ (p[m] * w)) mod p
direct_exp = sum(pi * wi for _, wi, pi in participants)  # Σ p_t^i[m] * w_i mod q
expected_Y = pow(g, direct_exp, p)  # g^(Σ p[m] * wi) mod p

# Debugging Output
print(f"Group Prime Modulus (p): {p}")
print(f"Group Order (q): {q}")
print(f"Generator (g): {g}")

print(f"\nRound Identifier (ℓt): {ℓt}")
print(f"u^ℓ_t (H(ℓt)): {Uℓt}")
print("\nParticipants:")
for i, (Si, Wi, Pi) in enumerate(participants, 1):
    print(f"Participant {i}: si = {Si}, wi = {Wi}, p[m] = {Pi}")
print("\n")
for i,ci in enumerate(ciphertexts,1):
    print(f" participant {i}: cipher: {ci}")

print(f"\nAggregator Key (AKas): {AKas}")
print(f"Top (Product of (∏ C[p[m]])^wi): {top}")
print(f"Bottom (AKas^(uℓt)): {bottom}")
print(f"\nAggregation (Formula Result, Y): {Y}")
print(f"Direct Computation (Expected Y): {expected_Y}")
print(f"\nAggregation Correct: {Y == expected_Y}")
