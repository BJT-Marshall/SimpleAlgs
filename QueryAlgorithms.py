from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


#Deutsch's Algorithm 

#Classical functions f :sigma -> sigma just for reference.

def f1(inp):
    """f(0) = 0, f(1) = 0"""
    return 0

def f2(inp):
    """f(0) = 0, f(1) = 1"""
    return inp

def f3(inp):
    """f(0) = 1, f(1) = 0"""
    if inp == 0:
        out = 1
    if inp == 1:
        out = 0
    return out

def f4(inp):
    """f(0) = 1, f(1) = 0"""
    return 1


def U_f1():
    """
    Generates a unitary gate with action :math:`U_f\ket{x}\ket{y} = \ket{x}\ket{y XOR f(x)}` for function 
    :math:`f: \sigma \rightarrow \sigma`, :math:`f(x) = f_1(x) = 0`.
    

    :returns gate: :python:`UnitaryGate` object implementing :math:`U_{f1}`.
    :rtype gate: UnitaryGate
    """
    qc = QuantumCircuit(2)
    gate = qc.to_gate()
    gate.label = 'U_f1'

    return gate

def U_f2():
    """
    Generates a unitary gate with action :math:`U_f\ket{x}\ket{y} = \ket{x}\ket{y XOR f(x)}` for function 
    :math:`f: \sigma \rightarrow \sigma`, :math:`f(x) = f_2(x) = x`.
    

    :returns gate: :python:`UnitaryGate` object implementing :math:`U_{f1}`.
    :rtype gate: UnitaryGate
    """
    qc = QuantumCircuit(2)
    qc.cx(0,1)
    gate = qc.to_gate()
    gate.label = 'U_f2'

    return gate

def U_f3():
    """
    Generates a unitary gate with action :math:`U_f\ket{x}\ket{y} = \ket{x}\ket{y XOR f(x)}` for function 
    :math:`f: \sigma \rightarrow \sigma`, :math:`f(x) = f_3(x) = 1` if :math:`x = 0` or :math:`f(x) = f_3(x) = 0` if :math:`x = 1`.
    

    :returns gate: :python:`UnitaryGate` object implementing :math:`U_{f1}`.
    :rtype gate: UnitaryGate
    """
    qc = QuantumCircuit(2)
    qc.cx(0,1)
    qc.x([0,1])
    gate = qc.to_gate()
    gate.label = 'U_f3'

    return gate

def U_f4():
    """
    Generates a unitary gate with action :math:`U_f\ket{x}\ket{y} = \ket{x}\ket{y XOR f(x)}` for function 
    :math:`f: \sigma \rightarrow \sigma`, :math:`f(x) = f_4(x) = 1`.
    

    :returns gate: :python:`UnitaryGate` object implementing :math:`U_{f1}`.
    :rtype gate: UnitaryGate
    """
    qc = QuantumCircuit(2)
    qc.x(1)
    gate = qc.to_gate()
    gate.label = 'U_f4'

    return gate



def deutsch_algorithm(U):
    """
    Generates a circuit performing Deutsch's algorithm given a unitary gate, :math:`U_f`.
    Deutsch's algorithm detemines whether an inpute oracle function :math:`f(x) : \sigma \rightarrow \sigma`
    is balanced or constant in a single call of the oracle function. 
    The result is measured into a classical register and will measure 0 if the function is constant and 1 if the function is balanced.

    :param U: Function generating a unitary oracle implementing classical function :math:'f(x)' with action :math:`U_f\ket{x}\ket{y} = \ket{x}\ket{y XOR f(x)}`.
    :type U: function
    :return qc: The :python:`QuantumCircuit` object implementing Deutsch's Algorithm with oracle :python:`U`
    :rtype qc: QuantumCircuit

    """
    #initial circuit setup to prepare the state |->|+> accross the two qubits.
    qc = QuantumCircuit(2,1)
    qc.x(1)
    qc.h([0,1])
    qc.barrier()
    #Application of the unitary oracle U_f
    qc.append(U(),[0,1])
    qc.barrier()
    #conversion of the resulting state of the first qubit into the computational basis for measurement
    qc.h(0)
    qc.barrier()
    #measurement of the first qubit to a single classical register
    qc.measure(0,0)

    return qc


def test_deutsch():
    """
    Compiles and runs Deutsch's Algorithm for the four possible oracles :math:`U_f, f:\sigma \rightarrow \sigma` using the :python:`AerSimulator` from :python:`qiskit_aer`.
    A circuit diagram is generated for each case as well as a histogram containing the resulting counts from 1024 shots of the algorithm.
    """
    deutsch_algorithm(U_f1).draw(output = 'mpl', filename = 'f1Test')
    qc = deutsch_algorithm(U_f1)
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()

    plot_histogram(counts, filename = 'DeutschTestF1')

    deutsch_algorithm(U_f2).draw(output = 'mpl', filename = 'f2Test')
    qc = deutsch_algorithm(U_f2)
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()

    plot_histogram(counts, filename = 'DeutschTestF2')

    deutsch_algorithm(U_f3).draw(output = 'mpl', filename = 'f3Test')
    qc = deutsch_algorithm(U_f3)
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()

    plot_histogram(counts, filename = 'DeutschTestF3')

    deutsch_algorithm(U_f4).draw(output = 'mpl', filename = 'f4Test')
    qc = deutsch_algorithm(U_f4)
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()

    plot_histogram(counts, filename = 'DeutschTestF4')

    return None


test_deutsch()