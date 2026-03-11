#Simons algorithm

#Simons problem: 
# 
#Function of the form f: sigma^n -> sigma^m
#Promise: There exists a string s in sigma^n such that [f(x) = f(y)] implies and is implied by [(x=y) OR (x XOR s = y)] for all x,y in sigma^n
#Outputs: the string s in sigma^n


#Two cases to consider: 
# 
#1) s in sigma^n, s = 0^n (i.e. the zero string of length n). This simplifies the promsise to simple [f(x) = f(y)] iff [x = y]. 
#   i.e. any one to one function f:sigma^n -> sigma^m has solution s = 0^n for this problem.
#
#2) s in sigma^n, s != 0^n. This would require that the function is two-to-one. i.e. there exists two input strings (x and x XOR s) that produce the output f(x) for each x in sigma^n.

#For each function f, there is only one string, s, that can satisfy the promise for all input values x in sigma^n (if a solution exists) so there is a unique s for each function you try.



from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
from qiskit.visualization import plot_histogram
from sympy import Matrix
import matplotlib.pyplot as plt

def simons_circuit(oracle: QuantumCircuit, n: int, m: int):
    """
    Generates the circuit implementation of Simon's Algorithm for an oracle :math:`U_f` implementing the function :math:`f: \\sigma^n \\rightarrow \\sigma^m` furiling the 
    promise of Simon's Problem.

    NOT USED in this example. Using a specific example oracle, :math:`U_f`, an implementation of Simon's Algorithm is manually recoded.

    :parmam oracle: :python:`QuantumCircuit` object implementing the oracle :math:`U_f` that implements a function of the form :math:`f: \\sigma^n \\rightarrow \\sigma^m` 
    furfiling the promise of Simon's Problem.
    :type oracle: QuantumCircuit
    :param n: Length of the input string for the function :math:`f` implemented by oracle :math:`U_f`.
    :type n: int
    :param m: Length of the output string for the function :math:`f` implemented by oracle :math:`U_f`.
    :type m: int


    :returns qc: :python:`QuantumCircuit` object implementing Simon's Algorithm for oracle :math:`U_f`.
    :rtpye qc: QuantumCircuit
    """
    qc = QuantumCircuit(n+m,n)
    qc.h(list(range(n)))
    qc.compose(oracle,list(range(n+m)), inplace=True)
    qc.h(list(range(n)))
    qc.measure(list(range(n)),list(range(n)))

    return qc


def example_oracle():
    """
    Generates an :python:`QuantumCircuit` object implementing an example oracle :math:`U_f` implementing the function :math:`f: \\sigma^3 \\rightarrow \\sigma^5` detailed bellow.

    Uses two ancillary qubits and classical feedforward operations to identify the correct functional output (see Mapping of ancillary qubits bellow) which is returned along with the register holding the measurements of
    the two ancillary qubits for straighforward composition of this oracle with larger :python:`QuantumCircuit` objects. 
    
    Action defining the example function:
    :math:`f: \\sigma^3 \\rightarrow \\sigma^5,
    f(000) = 10011,
    f(001) = 00101,
    f(010) = 00101,
    f(011) = 10011,
    f(100) = 11010,
    f(101) = 00001,
    f(110) = 00001,
    f(111) = 11010`

    This function obeys the promise of Simon's Problem with the string :math:`s = 011`.

    Mapping of ancillary qubit set [a1,a2] measurment outcomes to functional outputs :math:`f(x)`:
    [a1,a2] -> f(x):
    [0,0]   -> 10011    [:python:`y1`],
    [0,1]   -> 00101    [:python:`y2`],
    [1,0]   -> 11010    [:python:`y3`],
    [1,1]   -> 00001    [:python:`y4`]

    :returns qc: The QuantumCircuit object implementing the example oracle :math:`U_f`.
    :rtpye QuantumCircuit:
    :returns ancillary_clbits: The ClassicalRegister containing the resulting measurement of the ancillary qubits used in classical feed forward computations.
    :rtype ClassicalRegister: 
    """

    def y1():
        """
        Generates a ciruit mapping the zero state :math:`\\ket{00000}` to the output state :math:`\\ket{y1} = \\ket{10011}`
        
        :returns qc: QuantumCircuit implementing the above mapping.
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(5)
        qc.x([0,3,4])
        qc.name = 'y1'

        return qc
    
    def y2():
        """
        Generates a ciruit mapping the zero state :math:`\\ket{00000}` to the output state :math:`\\ket{y2} = \\ket{00101}`
        
        :returns qc: QuantumCircuit implementing the above mapping.
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(5)
        qc.x([2,4])
        qc.name = 'y2'

        return qc
    
    def y3():
        """
        Generates a ciruit mapping the zero state :math:`\\ket{00000}` to the output state :math:`\\ket{y3} = \\ket{11010}`
        
        :returns qc: QuantumCircuit implementing the above mapping.
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(5)
        qc.x([0,1,3])
        qc.name = 'y3'

        return qc
    
    def y4():
        """
        Generates a ciruit mapping the zero state :math:`\\ket{00000}` to the output state :math:`\\ket{y4} = \\ket{00001}`
        
        :returns qc: QuantumCircuit implementing the above mapping.
        :rtype: QuantumCircuit
        """
        qc = QuantumCircuit(5)
        qc.x(4)
        qc.name = 'y4'

        return qc

    ancillary_clbits = ClassicalRegister(2) #2 classical registers for measuring ancillary qubits
    qubits = QuantumRegister(10) #n+m+2 qubits, n=3, m=5
    qc = QuantumCircuit(qubits,ancillary_clbits) 

    qc.cx(0,8) #first input qubit -> first ancillary
    qc.barrier() 
    #Input detection mapping to ancillary qubits
    qc.cx(1,9) #these two combined give action of q1 XOR q2 with the output going to the second ancillary qubit
    qc.x(9)
    qc.cx(2,9) 
    qc.x(9)
    qc.barrier()
    #Ancillary qubits mapping the correct output state to the output qubits
    qc.measure([9,8],ancillary_clbits)
    #I can do this dynamically because its ancillary qubits so it doesnt matter if the infomation gets destroyed in the process
    with qc.if_test((ancillary_clbits, 0b00)):
        qc.append(y1(),list(range(3,8)))
    with qc.if_test((ancillary_clbits, 0b01)):
        qc.append(y2(),list(range(3,8)))
    with qc.if_test((ancillary_clbits, 0b10)):
        qc.append(y3(),list(range(3,8)))
    with qc.if_test((ancillary_clbits, 0b11)):
        qc.append(y4(),list(range(3,8)))
    
    return qc, ancillary_clbits






def run_simons_circuit():
    """
    Generates and runs an instance of the Simon's Algorithm circuit using the example oracle implemented in the :python:`example_oracle` method.
    
    :returns y: The output state :math:`y` for the example oracle implemented in the :python:`example_oracle` method.
    :rtpye str:
    """
    
    #Set up circuit
    oracle, anc = example_oracle()
    qreg = QuantumRegister(10)
    meas = ClassicalRegister(3)
    qc = QuantumCircuit(qreg,anc)
    qc.add_register(meas)

    #Hadamards on the output qubits
    qc.h(list(range(3)))

    qc.compose(oracle,list(range(10)), inplace = True)

    #Hadamards on the output qubits
    qc.h(list(range(3)))
    
    #Measure the output qubits to the 'meas' register
    qc.measure([2,1,0],meas)
    
    #Run the circuit on the AerSimulator
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ, shots =1).result()
    counts = results.get_counts()
    #Handle the returned counts to return the string of the resulting state |y>
    y = list(counts.keys())[0][:3]
      
    return y

#Only getting 000, 011, 100, 111 as outputs which is good thats 2^(n-1) outputs with seemingly 1/(2^(n-1)) probability.




def simons_algorithm(k_runs):
    """
    Runs the full implementation of Simon's Algorithm including classical post processing to identify the string :math:`s` furfilling the promise of Simon's Problem for the oracle
    implemented in the :python:`example_oracle` function.

    Theory:
    :math:`M\\vec{s} = \\vec{0}` where :math:`M` is the matrix containing :math:`k`-rows of strings returned from runs of the Simon's Algorithm circuit, 
    if the matrix-vector multiplication is done modulo 2.
    
    Given :math:`k = n + r` for an arbitrary integer :math:`r`, the probability that the vectors corresponding to the zero vector and :math:`s` are alone in the 
    null space of :math:`M` is :math:`1-2^{-r}`.
    
    :param k_runs: The number of runs of the Simon's Algorithm circuit to run. Also determines the shape of the matrix :math:`M`.
    :type k_runs: int
    :returns s: Returns the string that furfils Simon's Promise for the oracle implemented in :python:`example_oracle` with probability :math:`p(s) = 1-2^{-r}`.
    :rtype str:
    """
    
    M = []
    for i in range(k_runs): #run_simons_circuit() k_runs times
        row = [int(char) for char in run_simons_circuit()]
        M.append(row) #3 x k matrix for k runs

    nullspace = [Matrix(M).nullspace()[0][i] for i in range(3)]
    nullspace = [nullspace[i]%2 for i in range(len(nullspace))]

    s = ''
    for i in nullspace:
        s+=str(i)
    
    return s

def probability_test(runs,iters,filename):
    """
    Runs Simon's Algorithm for various values of :math:`k` to gather statistical data on its success rate that is predicted by the formula :math:`p(s) = 1-2^{-r}` for :math:`r` calls.
    Generates a plot of the probability of successfully determining :math:`s` as a function of calls. Additionally plots the theoretical results on the same axis for comparison.

    :param runs: The number of calls of Simon's Algorithm used to determine the matrix :math:`M`.
    :type runs: list
    :param iters: The number of iterations to repeat each set of runs of Simon's Algorithm for statistical sampling.
    :type iters: int
    :param filename:
    :type filename: str
    """
    #run simons using k_runs = r a total of iters times for varying r.
    probs_data = []
    probs_expected = [1-0.5**r for r in runs]

    for r in runs:
        prob = 0
        for i in range(iters):
            s = simons_algorithm(r)
            if s == '011':
                prob +=1
        probs_data.append(prob/iters)


    plt.plot(runs,probs_data, color = 'b', label = 'Data')
    plt.plot(runs,probs_expected, color = 'r', label = 'Theoretical Expectation')
    plt.xlabel('Number of Runs')
    plt.ylabel('Probability of Returning s')
    plt.title('Success Probability of Simons Algorithm for Example Oracle as a Function of Runs')
    plt.legend()
    plt.savefig(filename)

    return None

#probability_test(list(range(1,15)),50,'TestProbabilitySimons')

#----------------------------------------------------------------------------Extra Functions and Testing----------------------------------------------------------------------------

def test_example_oracle(input_state):
    """
    Tests the action of the :python:`example_oracle` function using any 3-bit binary input. Expected outputs are listed bellow.

    :math:`f: \\sigma^3 \\rightarrow \\sigma^5
    f(000) = 10011,
    f(001) = 00101,
    f(010) = 00101,
    f(011) = 10011,
    f(100) = 11010,
    f(101) = 00001,
    f(110) = 00001,
    f(111) = 11010`

    :param input_state: String representation of the binary input to the oracle implemented in :python:`example_oracle`.
    :type input_state: str
    :returns output: The output of the oracle implemented in :python:`example_oracle`, alternatively written as :math:`f(x)` for input :math:`x`.
    :rtype str:
    """
    state = []
    i=0
    for char in input_state:
        if char == '1':
            state.append(i)
        i+=1 
    oracle, anc = example_oracle()
    qreg = QuantumRegister(10)
    qc = QuantumCircuit(qreg,anc)
    if len(state) !=0:
        qc.x(state)
    oracle.draw(output = 'mpl', filename = 'SimonOracleTest')
    qc.compose(oracle,list(range(10)), inplace = True)
    qc.draw(output = 'mpl', filename = 'SimonOracleTest1')

    meas = ClassicalRegister(5)
    qc.add_register(meas)
    qc.measure(list(range(7,2,-1)),meas)
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()
    output = list(counts.keys())[0][:5]

    plot_histogram(counts, filename = 'SimonOracleTestCounts')

    return output

def handle_binary(binary,n):
    """
    Handles n-bit binary data types to convert them the a string of length n including the ussually disregarded leading zeros.

    :param binary: The binary input to be converted to a binary string of length n.
    :type binary: bin
    :param n: The desired length of the binary string.
    :type n: int
    :returns binary_string: The string of n-bit binary including leading zeros.
    :rtype str: 
    """
    binary_string = binary[2:]
    while len(binary_string) != n:
        binary_string = '0'+binary_string
    
    return binary_string

def run_simons_circuit_random_input():
    """
    Generates and runs an instance of the the example oracle implemented in the :python:`example_oracle` method with a random input state and returns the output state.
    
    :returns x: The input state for the example oracle implemented in the :python:`example_oracle` method.
    :rtype str:
    :returns y: The output state for the example oracle implemented in the :python:`example_oracle` method.
    :rtpye str:
    """
    #random call to the oracle
    x = handle_binary(bin(np.random.randint(0,8)),3)
    state = [x.index(char) for char in x if char == '1']
    
    oracle, anc = example_oracle()
    qreg = QuantumRegister(10)
    meas = ClassicalRegister(5)
    qc = QuantumCircuit(qreg,anc)
    qc.add_register(meas)
    if len(state) !=0:
        qc.x(state)
    qc.compose(oracle,list(range(10)), inplace = True)
    qc.measure(list(range(7,2,-1)),meas)
    
    #Run the circuit on the AerSimulator
    simulator = AerSimulator()
    circ = transpile(qc, simulator)
    results = simulator.run(circ).result()
    counts = results.get_counts()
    #Handle the returned counts to return the string of the resulting state |y>
    y = list(counts.keys())[0][:5]
      
    return x,y



