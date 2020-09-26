from pyquil.quil import Program, DefGate
from pyquil.quilatom import Parameter, quil_sin, quil_cos, quil_sqrt, quil_exp
from pyquil import api, get_qc
from pyquil.api import WavefunctionSimulator
from pyquil.gates import *
import numpy as np

from gates import Gates

qc = get_qc('9q-square-qvm')


'''
Function to decompose following 
quantum gates {I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ}
to a restricted set of {RX, RY, CZ}

@param program: pyQuil `Program` containing a quantum circuit
@return: Modified circuit consisting of only {RX, RY, CZ}
'''
def compile(program):
    p = Program()
    g = Gates()

    # Iterate over incoming gates
    for gate in program.instructions:
        gate_str = str(gate)
        g_info = gate_str.split(" ")

        # Parse angle
        if(g_info[0].find("(") > -1):
            g_name = g_info[0].split("(")[0]
            g_angle = g_info[0].split("(")[1].strip(")")
        else:
            g_name = g_info[0]
            g_angle = None

        # Parse qubits
        g_qubits = []
        for i in range(1, len(g_info)):
            g_qubits.append(int(g_info[i]))

        # Replace gate with respective decompositions
        if(g_name == "I"):
            g.I(p, g_qubits)
        elif(g_name == "H"):
            g.H(p, g_qubits)
        elif(g_name == "X"):
            g.X(p, g_qubits)
        elif(g_name == "Y"):
            g.Y(p, g_qubits)
        elif(g_name == "Z"):
            g.Z(p, g_qubits)
        elif(g_name == "RY"):
            # g_angle to be of the format = x*np.pi/y
            g.RY(p, g_qubits, g_angle)
        elif(g_name == "RX" or g_name == "RZ" or g_name == "CZ"):
            p += gate
        elif(g_name == "CNOT"):
            g.CNOT(p, g_qubits)
        else:
            raise Exception("Gate not found in set: {I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ}")

    return p

'''
Function to find gate name inside a string.

@param find_in: String to find gate name in
@param gate_name: Notation of the gate

@return: Boolean
'''
def is_gate(find_in, gate_name):
    return gate_name in find_in

'''
Function to compile and run a quantum circuit.

@param program: pyQuil program object

@return: result of pyQuil `run_and_measure` fn
'''
def execute(program):
    print('Incoming Program:', program)
    compiled_prog = compile(program)
    print('Compiled Program:', compiled_prog)
    return qc.run_and_measure(compiled_prog, trials=1)

'''
Execute and print result of a simple CNOT gate.
'''
if __name__ == '__main__':
    program = Program()
    program += X(0)
    program += CNOT(0, 1)
    result = execute(program)
    print('RESULT QUBIT 0:', result[0])
    print('RESULT QUBIT 1:', result[1])