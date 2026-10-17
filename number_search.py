print("GROVER QUANTUM SEARCH")
print("Enter five distinct numbers between 0 and 15.")

numbers = []

for i in range(5):
    while True:
        try:
            n = int(input(f"Enter number {i + 1}: "))

            if n < 0 or n > 15:
                print("Enter a number between 0 and 15.")
            elif n in numbers:
                print("Number already entered. Try again.")
            else:
                numbers.append(n)
                break

        except ValueError:
            print("Please enter an integer.")

while True:
    try:
        target = int(input("Enter target number (0-15): "))

        if 0 <= target <= 15:
            break

        print("Target must be between 0 and 15.")

    except ValueError:
        print("Please enter an integer.")

print("Numbers:", numbers)
print("Target:", target)

input("Press ENTER to continue...")

print("\nSTEP 2: BINARY REPRESENTATIONS")

for n in numbers:
    print(f"{n:2d} = {n:04b}")

print(f"Target {target} = {target:04b}")

input("Press ENTER to continue...")

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from math import pi

DATA = [0, 1, 2, 3]
EQUALITY_FLAGS = [4, 5, 6, 7, 8]
MEMBER_FLAG = 9
TARGET_FLAG = 10
PHASE_QUBIT = 11

TOTAL_QUBITS = 12

print("\nSTEP 3: QUANTUM REGISTERS")
print("Data qubits:", DATA)
print("Equality flags:", EQUALITY_FLAGS)
print("Membership flag:", MEMBER_FLAG)
print("Target flag:", TARGET_FLAG)
print("Phase qubit:", PHASE_QUBIT)

input("Press ENTER to continue...")

def compare_value(qc, value, flag):
    for q in DATA:
        if ((value >> q) & 1) == 0:
            qc.x(q)

    qc.mcx(DATA, flag)

    for q in DATA:
        if ((value >> q) & 1) == 0:
            qc.x(q)


oracle = QuantumCircuit(TOTAL_QUBITS)

# Compare against all five input numbers.
for value, flag in zip(numbers, EQUALITY_FLAGS):
    compare_value(oracle, value, flag)

# Record whether the candidate belongs to the list.
for flag in EQUALITY_FLAGS:
    oracle.cx(flag, MEMBER_FLAG)

# Compare against the target.
compare_value(oracle, target, TARGET_FLAG)

# Mark the phase only if both conditions are true.
oracle.mcx([MEMBER_FLAG, TARGET_FLAG], PHASE_QUBIT)

# Uncompute the target flag.
compare_value(oracle, target, TARGET_FLAG)

# Uncompute the membership flag.
for flag in EQUALITY_FLAGS:
    oracle.cx(flag, MEMBER_FLAG)

# Uncompute the equality flags.
for value, flag in reversed(list(zip(numbers, EQUALITY_FLAGS))):
    compare_value(oracle, value, flag)

print("\nSTEP 4: ORACLE CREATED")
print(oracle.draw(output="text"))

input("Press ENTER to continue...")

def apply_diffusion(qc):
    for q in DATA:
        qc.h(q)

    for q in DATA:
        qc.x(q)

    qc.h(DATA[3])
    qc.mcx(DATA[:3], DATA[3])
    qc.h(DATA[3])

    for q in DATA:
        qc.x(q)

    for q in DATA:
        qc.h(q)


print("\nSTEP 5: DIFFUSION OPERATOR CREATED")

input("Press ENTER to continue...")

qc = QuantumCircuit(TOTAL_QUBITS, 4)

for q in DATA:
    qc.h(q)

# Prepare the phase qubit in the |-> state.
qc.x(PHASE_QUBIT)
qc.h(PHASE_QUBIT)

print("\nSTEP 6: SUPERPOSITION CREATED")
print(qc.draw(output="text"))

input("Press ENTER to continue...")

iterations = round((pi / 4) * (16 ** 0.5) - 0.5)

print("\nSTEP 7: GROVER ITERATIONS")
print("Number of iterations:", iterations)

input("Press ENTER to continue...")

for step in range(iterations):
    print(f"\nGROVER ITERATION {step + 1}")

    qc.compose(oracle, inplace=True)

    apply_diffusion(qc)

    print(qc.draw(output="text"))

    input("Press ENTER for the next iteration...")

    for q in DATA:
        qc.measure(q, q)

print("\nSTEP 9: FINAL CIRCUIT")
print(qc.draw(output="text"))

input("Press ENTER to execute the simulation...")

simulator = AerSimulator()

result = simulator.run(qc, shots=1024).result()

counts = result.get_counts()

print("\nSTEP 10: MEASUREMENT RESULTS")
print(counts)

input("Press ENTER to decode the results...")

print("\nSTEP 11: DECODED RESULTS")

for bitstring, count in sorted(
    counts.items(),
    key=lambda item: item[1],
    reverse=True
):
    value = int(bitstring, 2)

    print(
        f"Binary: {bitstring} | "
        f"Decimal: {value} | "
        f"Count: {count}"
    )

most_frequent_bits = max(counts, key=counts.get)
measured_value = int(most_frequent_bits, 2)

print("\nMost frequent measured value:", measured_value)
print("Requested target:", target)

# Classical verification after measurement.
if measured_value == target and measured_value in numbers:
    print("SUCCESS: Target found!")
else:
    print("Target not confirmed by the most frequent result.")
    print("Inspect the measurement counts.")
    print("This result alone cannot prove that the target is absent.")

