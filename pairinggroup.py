from charm.toolbox.pairinggroup import PairingGroup,ZR,G1
import random
import numpy as np



# This function converts a float to an integer
def float_to_int_fnc(number, accuracy=6):
    if isinstance(number, (float, np.float32)):
        val = float(number) * (10 ** accuracy)
        # Explicitly ensure rounding preserves the sign
        return int(round(val)) if val >= 0 else int(-round(abs(val)))
    if isinstance(number, int):
        return int(number)
    else:
        raise ValueError(f"Input must be an int or float, got {type(number)}: {number}")


# This function converts an integer back to a float
def int_to_float_fnc(number, accuracy=6):
    if isinstance(number, (int, np.int64)):
        return float(number / (10 ** accuracy))
    if isinstance(number, float):
        return number


def init_group_fn(number_of_bits='MNT159'):
    # Initialize the group
    group = PairingGroup(number_of_bits,param_file=False,verbose=True)
    q = group.order()
    g = group.random(G1)

    return g,group ,q


def generate_random_Si(number_of_participants,group):
    # Generate random secret keys (si), weights (wi), and model parameters (Pi[m])
    participants = []

    # This loop defines the parameters randomly
    for i in range(number_of_participants):
        Si = group.random(ZR)  # Secret key (si ∈ Zq )
        participants.append(Si)
    return participants


def generate_Uℓt_fun(group):
    Uℓt = group.random(ZR)  # Uℓt = H(ℓt) mod q # H(ℓt ) ∈ Zq
    return Uℓt


def generate_AK_fun(si_wi,g):
    # Compute Aggregator Key (AKas) = g^(Σ Si * Wi) mod p
    weighted_sum = sum(si * wi for si, wi in si_wi)  # (Σ Si * Wi)
    AKas = g ** weighted_sum
    return AKas


def encrypt_param(pi, power_G, g):

    Pi = float_to_int_fnc(pi)

    Ci_m = g ** (power_G + Pi)  # Compute Ci[p[m]] = g^^(si * Uℓt + Pi_t) mod p

    return Ci_m


def encrypt_parameters_fun(Pi, Si, Uℓt,g):
    # Compute the Ciphertext (Ci[p[m]]) for each participant as a matrix:  g^[(si*uℓt) + pi [m]] ∈ G
    ciphertexts = []
    power_G = Si * Uℓt

    for item in Pi:
        if np.isscalar(item):  # Handle scalar values directly
            # Encrypt the scalar and store it in the same structure
            ciphertexts.append(encrypt_param(pi=item, power_G=power_G, g=g))
        else:
            # Handle arrays (1D, 2D, or higher dimensions)
            Ci_m_array = []
            for row in np.atleast_2d(item):  # Treat 1D arrays as 2D with one row
                Ci_m_row = [encrypt_param(pi=pr, power_G=power_G, g=g) for pr in row]
                Ci_m_array.append(Ci_m_row)
            ciphertexts.append(Ci_m_array)

    return ciphertexts

