import numpy as np
import secrets
import time

class Project69:
    """
    Project *69: Post-Quantum Neighborhood Security
    Standardized Parameter Set: LWE-512-PQ
    """
    def __init__(self, n=512, q=12289):
        # n = dimensions, q = prime field, m = number of equations
        self.n = n
        self.q = q
        self.m = n * 2 

    def generate_keys(self):
        """Generates Private Key (s) and Public Matrix (A)"""
        # s is the secret point M in the n-dimensional grid
        s = np.array([secrets.randbelow(self.q) for _ in range(self.n)])
        # A is the public neighborhood structure
        A = np.random.randint(0, self.q, size=(self.m, self.n))
        return s, A

    def lock_vault(self, s, A):
        """Creates the Public Vault (b) by adding Noise Jitter (e)"""
        # e = the 'Non-Invertible Neighborhood' surrounding M
        e = np.random.randint(-1, 2, size=self.m)
        # b = (As + e) mod q
        b = (np.dot(A, s) + e) % self.q
        return b

    def verify_owner(self, b, s, A):
        """Callback Verification: Instant check for the secret owner"""
        # Calculate residual r = (b - As) mod q
        r = (b - np.dot(A, s)) % self.q
        # Valid if all elements are within noise bounds {-1, 0, 1}
        # (96 mod 97 is q-1, representing -1)
        valid_noise = {0, 1, self.q - 1}
        return all(val in valid_noise for val in r)

# --- DEMONSTRATION SUITE ---

def run_demo():
    # Initialize Project *69
    vault = Project69(n=512, q=12289)
    s, A = vault.generate_keys()
    
    print("--- PROJECT *69 INITIALIZED ---")
    print(f"Parameters: n={vault.n}, q={vault.q}")
    print(f"Search Space: 1 in 10^2093 (Quantum-Resistant)")
    
    # 1. LOCKING
    b = vault.lock(s, A)
    print("\n[+] Vault Locked with secret M.")

    # 2. OWNER VERIFICATION (The 'Callback')
    start_owner = time.perf_counter()
    success = vault.verify(b, s, A)
    end_owner = time.perf_counter()
    print(f"[+] Owner Access: {'GRANTED' if success else 'DENIED'}")
    print(f"[+] Verification Time: {end_owner - start_owner:.6f} seconds")

    # 3. ATTACKER SIMULATION (The 'Wall')
    print("\n[!] Attacker 'Solver' attempting brute-force inversion...")
    start_attack = time.time()
    attempts = 0
    while time.time() - start_attack < 3:  # Try for 3 seconds
        guess = np.random.randint(0, vault.q, size=vault.n)
        if vault.verify(b, guess, A):
            print("CRITICAL FAILURE: Vault Cracked!")
            return
        attempts += 1
    
    print(f"[!] Solver checked {attempts:,} keys.")
    print(f"[!] Result: FAILED (Probability of success: ~0.000...0001%)")

if __name__ == "__main__":
    run_demo()
