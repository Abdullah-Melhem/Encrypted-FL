# **Secure Aggregation with Modular Arithmetic**

This repository contains an implementation of a secure aggregation scheme using modular arithmetic. The code computes the aggregated result \( Y \) for encrypted data while maintaining privacy, leveraging element-wise operations and modular arithmetic.

## **Features**
- Element-wise operations with modular exponentiation.
- Support for secure aggregation in a cryptographic setting.
- Handles operations like encryption, decryption, and aggregation securely.

## **Mathematical Overview**
The code implements the following formulas:
1. **Encryption**:
   \[
   C_t^i[p[m]] = g^{(s_i \cdot u^{\ell_t} + p_t^i[m])} \mod p
   \]
   Each participant encrypts their data using a secret key \( s_i \) and a hashed round identifier \( u^{\ell_t} \).

2. **Aggregation**:
   The aggregated result is computed as:
   \[
   Y = \prod_{i=1}^N (C_t^i[p[m]])^{w_i} \mod p
   \]
   Where \( w_i \) represents the weight of each participant.

3. **Decryption**:
   Decrypt the aggregated result using the shared secret and hashed identifiers.

## **Setup**

### Prerequisites
- Python 3.7 or later
- Libraries:
  - [Charm-Crypto](https://github.com/JHUISI/charm): For cryptographic operations.
  - `hashlib`: For secure hashing.
  

