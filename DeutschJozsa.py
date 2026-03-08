from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import numpy as np

#Deutsch-Jozsa Algorithm.

#Extension of Deutsch's algorithm to functions of the form f: sigma^n -> sigma.
#Assumed promise is that all functions considered for the Deutsch-Jozsa algorithm are either balanced or constant. 
#Any other functions are considered "dont-care" inputs.

#Outputs 0 if f is constant, outputs 1 if f is balanced.

#promise requires constant functions and balanced functions only.

def constant_oracle(n):
    #Strictly speaking this is not needed to demonstrate the DJ algorithm as any constant function (i.e Identity over all qubits)
    #would suffice to demonstrate the ability of DJ to distinguish constant from balanced functions. 
    #Circuit implementing a constant oracle for use in demonstrating the Deutsch Jozsa algorithm.
    qc = QuantumCircuit(n+1)
    flip_flag = np.random.randint(0,2)
    if flip_flag:
        qc.x(list(range(n)))
        qc.mcx(list(range(n)),-1)
        qc.x(list(range(n)))
        return qc
    else:
        qc.mcx(list(range(n)),-1)
        return qc
    
def balanced_oracle(n):
    #Circuit implementing a balanced oracle for use in demonstrating the Deutsch Jozsa algorithm.
    qc = QuantumCircuit(n+1)

    #pick half of the input states to output 1 (i.e. manipulate such that the action of an mcx gate flips the target qubit)
    
    def adjust_binary(state):
        while len(state) !=n:
            state = '0'+state
        return state

    flip_inds = np.random.choice(np.arange(2**n),2**(n-1), replace = False)
    flip_states = [adjust_binary(f"{state:0b}") for state in flip_inds]


    for state in flip_states:
        #for each state that needs manipulation
        for i in range(len(state)):
            if state[i] == '0':
                qc.x(i)
        qc.mcx(list(range(n)),-1)
        for i in range(len(state)):
            if state[i] == '0':
                qc.x(i)
        qc.barrier()

    #the other half of the input states should not trigger the mcx gate to flip the target qubit which doesnt need handling
    #i.e. has action of identity

    return qc


def deutsch_jozsa_oracle(n):
    if np.random.randint(0,2):
        qc = constant_oracle(n)
    else:
        qc = balanced_oracle(n)
    return qc

def deutsch_jozsa(oracle):
    qubit_list = [i for i in range(oracle.num_qubits)]
    qc = QuantumCircuit(len(qubit_list),len(qubit_list)-1)
    qc.x(-1)
    qc.h(qubit_list)
    qc.compose(oracle, inplace=True)
    qubit_list.pop(-1)
    qc.h(qubit_list)
    qc.measure(qubit_list,qubit_list)

    return qc


def test_deutsch_jozsa(oracle, draw = False, filename = None): 
    qc = deutsch_jozsa(oracle)
    if draw:
        qc.draw(output = 'mpl', filename = filename)
    results = AerSimulator().run(qc, shots = 1, memory=True).result()
    measurement = results.get_memory()
    if "1" in measurement[0]:
        return "balanced"
    return "constant"


print(test_deutsch_jozsa(deutsch_jozsa_oracle(5),draw = True, filename = 'TestDJ'))



