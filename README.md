# **Secure Aggregation with Modular Arithmetic**

This repository contains an implementation of a secure aggregation scheme using modular arithmetic. The code computes the aggregated result \( Y \) for encrypted data while maintaining privacy, leveraging element-wise operations and modular arithmetic.

## **Features**
- Element-wise operations with modular exponentiation.
- Support for secure aggregation in a cryptographic setting.
- Handles operations like encryption, and aggregation securely.

## **Mathematical Overview**
The code implements the following formulas:
1. **Encryption**:
   Each participant encrypts their data using a secret key \( s_i \) and a hashed round identifier.

2. **Aggregation**:
   The aggregated result is computed as:
   \[
   Y = \prod_{i=1}^N (C_t^i[p[m]])^{w_i} \mod p
   \]
   Where \( w_i \) represents the weight of each participant.


## **Setup**

### Prerequisites
- Python 3.7 or later
- Libraries:
  - [Charm-Crypto](https://github.com/JHUISI/charm): For cryptographic operations.
  - `hashlib`: For secure hashing.

  ### This code is based on the FedSafe feamework
  M. I. Ibrahem, M. M. Fouda and Z. M. Fadlullah, "FedSafe-No KDC Needed: Decentralized Federated Learning with Enhanced Security and Efficiency," 2024 IEEE 21st Consumer Communications & Networking Conference (CCNC), Las Vegas, NV, USA, 2024, pp. 969-975, doi: 10.1109/CCNC51664.2024.10454870. keywords: {Training;Threat modeling;Data privacy;Federated learning;Computational modeling;Training data;Data models;Federated learning;privacy preservation;functional encryption;decentralization},



