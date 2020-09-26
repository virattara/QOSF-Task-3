# QOSF-Task-3
*Submitted By: Virat Tara*

## TASK DETAILS:
Please write a simple compiler – program, which translates one quantum circuit into another, using a restricted set of gates.

You need to consider just the basic gates for the input circuit, such as (I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ).

The output circuit should consist only from the following gates: RX, RZ, CZ. In other words, each gate in the original circuit must be replaced by an equivalent combination of gates coming from the restricted set (RX, RZ, CZ) only.

For example, a Hadamard gate after compilation looks like this:
RZ(pi/2)
RX(pi/2)
RZ(pi/2)

Analyze what’s the overhead of the compiled program compared to the original one and propose how to improve it. What we mean by overhead is the following: by replacing all the initial gates with the restricted set of gates given in the problem, you will see that the resulting circuit is much more involved than the original one. This is what we called the overhead, and you may think about how to treat this problem, i.e. you could try to simplify as much as possible the resulting circuit.

## SOLUTION & PROCEDURE:
### 1. PREREQUISITES
Firstly, I studied the matrix representation of the restricted set gates and euler angles[1]. Below are the matrices of RX(θ), RZ(θ), CZ


        RX(θ) = [[cos(θ/2),  -i*sin(θ/2)],
                 [-isin(θ/2,     cos(θ/2)]]

        RZ(θ)[1] = [[exp(-iθ/2), 0],
                    [0,   exp(iθ/2)]]

        RZ(θ)[2] = [[1,      0],
                    [0, exp(iθ)]]

        NOTE: RZ(θ)[1] & RZ(θ)[2] differ by a global phase of exp(iθ/2) only.

        CZ = [[1, 0, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, 0],
              [0, 0, 0, -1]]

#### PROGRAMMING LANGUAGE USED: 
Python v3.7.3

#### TOOLS USED:
a). [rigetti/pyquil](https://github.com/rigetti/pyquil) v2.20.0 <br />
b). [quirk](https://algassert.com/quirk)


### 2. METHOD
Next I tried to calculated what combination of the restricted set matrices would result in the following gate set (I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ) individually. Generally, rotation in a 3d plane (XYZ) can be done using the combination of RZ(θ1)⊗RX(θ2)⊗RX(θ3). 

Below is the decomposition of each gate in the input gate set.

    a). Identity Gate (I):

            Decomposition:
                I = RZ(0)[2]

            Matrix representation:
                [[1, 0],
                 [0, 1]]

[Online circuit](https://bit.ly/335ExO4)



    b). Hadamard Gate (H):

            Decomposition:
                H = RZ(pi/2)[2] ⊗ RX(pi/2) ⊗ RZ(pi/2)[2]

            Matrix representation:
                (1/sqrt(2))*[[1,  1], = [[1, 0], ⊗ [[1/sqrt(2), -i/sqrt(2)] ⊗ [[1, 0],
                             [1, -1]]    [0, i]]    [-i/sqrt(2), 1/sqrt(2)]]   [0, i]]

[Online circuit](https://bit.ly/3j7DRgq)

    c). Pauli-X Gate (X):

            Decomposition:
                X = RZ(pi)[1] ⊗ RX(pi) ⊗ RZ(-pi)[2]

            Matrix representation:
                [[0, 1], = [[-i, 0],  ⊗ [[0, -i], ⊗ [[1  0)],
                 [1, 0]]    [0,  i]]     [-i, 0]]    [0, -1]]

[Online circuit](https://bit.ly/2FTMMUI)

    d). Pauli-Y Gate (Y):

            Decomposition:
                Y = RZ(-pi)[1] ⊗ RX(pi)

            Matrix representation:
                [[0, -i], = [[1,  0], ⊗ [[0, -i],
                 [i,  0]]    [0, -1]]    [-i, 0]]

[Online circuit](https://bit.ly/3j54D9i)

    e). Pauli-Z Gate (Z):

            Decomposition:
                Z = RZ(pi)[2]

            Matrix representation:
                [[1,  0],
                 [0, -1]]

[Online circuit](https://bit.ly/3i43Mo3)

    f). RY Gate:

            Decomposition:
                Z = RZ(pi/2)[2] ⊗ RX(θ) ⊗ RZ(-pi/2)[2]

            Matrix representation:
                [[cos(θ/2), -sin(θ/2)], = [[1, 0], ⊗ [[cos(θ/2),   -i*sin(θ/2)], ⊗ [[1,  0],
                 [sin(θ/2),  cos(θ/2)]]    [0, i]]     [-i*sin(θ/2), cos(θ/2)]]     [0  -i]]

[Online circuit](https://bit.ly/2RYiuSW) {RY(pi)}

    g). CNOT Gate:

            Decomposed circuit:

                |q1>_________x_____________
                             |
                |q2>____[H]_[CZ]_[H]_______

[Online circuit](https://bit.ly/3i5CJZI)


### 3. CODE STRUCTURE:
The code is written in Python and uses Rigetti's `pyquil`(v2.20.0) library. Code has been divided into two files with the following objectives.

a). compiler.py => Parse the incoming pyQuil `Program` object and decompose incoming gates from (I, H, X, Y, Z, RX, RY, RZ, CNOT, CZ) to the restricted set of (RX, RZ, CZ). If any incoming gate is not in the specified set, the code throws an exception.

b). gates.py => Contains the decomposition rules of the various gates to the restricted set.


### 4. ANALYSIS & OPTIMIZATIONS:
The decomposition surely increases overhead but might be useful on a hardware that supports only (RX, RZ, CZ). A simple circuit containing a Pauli-X and CNOT gate now takes 8 single qubit gates and 1 two qubit gate, compared to 1 single qubit and 1 two qubit gate. Below are some optimizations that I propose:

a). Consecutive RZ(θ) gates on a qubit can be applied as one using the following criteria.<br/>

    RZ(θ) ⊗ RZ(θ) ⊗ ... n  = RZ(nθ)

    [[1,      0],  ⊗  [[1,      0],   =  [[1,      0],
     [0, exp(iθ)]]     [0, exp(iθ)]]      [0, exp(i*2θ)]]

b). Consecutive RX(pi) gates can be cancelled out.<br/>

    RX(pi) ⊗ RX(pi) = exp(i*pi)*(I)
    The global phase  of exp(i*pi) can be ignored.

    [[0, -i], ⊗ [[0, -i], = [[-1, 0],
     [-i, 0]]    [-i, 0]]    [0, -1]]


### 5. ONGOING WORK:
Trying to understand implications of the Solovay-Kitaev algorithim[2] on this work.


### 6. REFERENCES:
[1] Euler Angles: https://mathworld.wolfram.com/EulerAngles.html <br />
[2] The Solovay-Kitaev algorithim: https://arxiv.org/pdf/quant-ph/0505030.pdf
