from pyquil.quil import Program, DefGate
from pyquil.quilatom import Parameter, quil_sin, quil_cos, quil_sqrt, quil_exp
from pyquil import api, get_qc
from pyquil.api import WavefunctionSimulator
from pyquil.gates import RX,RZ,CZ
import numpy as np

class Gates:
    '''
    ------------------------------------------
    Matrix representations of RX(θ), RY(θ), CZ:
    ------------------------------------------

    RX(θ) = [[cos(θ/2),  -i*sin(θ/2)],
             [-isin(θ/2,     cos(θ/2)]]

    RZ(θ)[1] = [[exp(-iθ/2), 0],
                [0,   exp(iθ/2)]]

    RZ(θ)[2] = [[1,      0],
                [0, exp(i0)]]

    NOTE: RZ(θ)[1] & RZ(θ)[2] differ by a global phase only.

    CZ    = [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, -1]]
    '''

    def I(self, p, g_qubits):
        '''
        --------------
        Identity Gate (I):
        --------------
        Decomposition:
            I = RZ(0)[2]

        Matrix representation:
            [[1, 0],
             [0, 1]]

        Online circuit:
            https://bit.ly/335ExO4
        '''
        p += RZ(0, g_qubits[0])

    def H(self, p, g_qubits):
        '''
        --------------
        Hadamard Gate (H):
        --------------
        Decomposition:
            H = RZ(pi/2)[2] ⊗ RX(pi/2) ⊗ RZ(pi/2)[2]

        Matrix representation:
            (1/sqrt(2))*[[1,  1], = [[1, 0], ⊗ [[1/sqrt(2), -i/sqrt(2)] ⊗ [[1, 0],
                         [1, -1]]    [0, i]]    [-i/sqrt(2), 1/sqrt(2)]]   [0, i]]

        Online circuit:
            https://bit.ly/3j7DRgq
        '''
        p += RZ(np.pi/2, g_qubits[0])
        p += RX(np.pi/2, g_qubits[0])
        p += RZ(np.pi/2, g_qubits[0])

    def X(self, p, g_qubits):
        '''
        -------------
        Pauli-X Gate (X):
        -------------
        Decomposition:
            X = RZ(pi)[1] ⊗ RX(pi) ⊗ RZ(-pi)[2]

        Matrix representation:
            [[0, 1], = [[-i, 0],  ⊗ [[0, -i], ⊗ [[1  0)],
             [1, 0]]    [0,  i]]     [-i, 0]]    [0, -1]]

        Online circuit:
            https://bit.ly/2FTMMUI
        '''
        p += RZ(np.pi, g_qubits[0])
        p += RX(np.pi, g_qubits[0])
        p += RZ(-np.pi, g_qubits[0])

    def Y(self, p, g_qubits):
        '''
        -------------
        Pauli-Y Gate (Y):
        -------------
        Decomposition:
            Y = RZ(-pi)[2] ⊗ RX(pi)

        Matrix representation:
            [[0, -i], = [[1,  0], ⊗ [[0, -i],
             [i,  0]]    [0, -1]]    [-i, 0]]

        Online circuit:
            https://bit.ly/3j54D9i
        '''
        p += RZ(-np.pi, g_qubits[0])
        p += RX(np.pi, g_qubits[0])

    def Z(self, p, g_qubits):
        '''
        -------------
        Pauli-Z Gate (Z):
        -------------
        Decomposition:
            Z = RZ(pi)[2]

        Matrix representation:
            [[1,  0],
             [0, -1]]

        Online circuit:
            https://bit.ly/3i43Mo3
        '''
        p += RZ(np.pi, g_qubits[0])

    def RY(self, p, g_qubits, g_angle):
        '''
        --------
        RY Gate:
        --------
        Decomposition:
            Z = RZ(pi/2)[2] ⊗ RX(θ) ⊗ RZ(-pi/2)[2]

        Matrix representation:
            [[cos(θ/2), -sin(θ/2)], = [[1, 0], ⊗ [[cos(θ/2),   -i*sin(θ/2)], ⊗ [[1,  0],
             [sin(θ/2),  cos(θ/2)]]    [0, i]]     [-i*sin(θ/2), cos(θ/2)]]     [0  -i]]

        Online circuit:
            https://bit.ly/2RYiuSW {RY(pi)}
        '''
        p += RZ(np.pi/2, g_qubits[0])
        p += RX(get_angle(g_angle), g_qubits[0])
        p += RZ(-np.pi/2, g_qubits[0])

    def CNOT(self, p, g_qubits):
        '''
        ----------
        CNOT Gate:
        ----------
        Circuit used for implementing CNOT.

        |q1>_________x_____________
                     |
        |q2>____[H]_[CZ]_[H]_______

        https://bit.ly/3i5CJZI
        '''
        self.H(p, [g_qubits[1]])
        p += CZ(g_qubits[0], g_qubits[1])
        self.H(p, [g_qubits[1]])

'''
Function to return an executable angle

@param angle: Angle of the format x*np.pi/y
@return: A numpy angle
'''
def get_angle(angle):
    parsed_angle = np.pi

    if '*' in angle:
        parsed_angle = parsed_angle*float(angle.split('*')[0])

    if '/' in angle:
        parsed_angle = parsed_angle/float(angle.split('/')[1])

    return parsed_angle