import random
from enum import Enum
import csv


class Gate(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    NOR = "NOR"
    XOR = "XOR"
    XNOR = "XNOR"
    NAND = "NAND"
    BUFF = "BUFF"
    NONE = "NONE"  # should not happen


line_limit = 150
line_i = 0


def limitedPrint(str):
    global line_i
    global line_limit
    strlen = len(str)
    if (line_i + strlen) > line_limit:
        # create new line:
        print("\n", end="")
        line_i = len(str)
        print(str, end="")
    else:
        line_i = line_i + strlen
        print(str, end="")


def evalGate(g, list):
    assert len(list) > 0
    for val in list:
        assert val == 0 or val == 1
    if g == Gate.NOT:
        assert len(list) == 1
        return bool(not list[0])
    elif g == Gate.AND:
        express = 1
        for val in list:
            express = express * val
        return bool(express)
    elif g == Gate.NAND:
        return not evalGate(Gate.AND, list)
    elif g == Gate.OR:
        for val in list:
            if val == 1:
                return True
        return False
    elif g == Gate.NOR:
        return not evalGate(Gate.OR, list)
    elif g == Gate.XOR:
        # if number of 1s is 1, 3, 5, (odd) return 1
        ones = 0
        for val in list:
            if val == 1:
                ones = ones + 1
        if ones % 2 == 0:
            return False
        return True
    elif g == Gate.XNOR:
        return not evalGate(Gate.XOR, list)
    elif g == Gate.BUFF:
        assert len(list) == 1
        return list[0]
    assert g != Gate.NONE


INTEGER_MAX = 2147483648


# given the controllability of the input nodes, and this gate,
# return the controllability value of this gate
def evalControllability(g, list):
    for i in range(len(list)):
        assert len(list[i]) == 2
        assert isinstance(list[i][0], int)
        assert isinstance(list[i][1], int)

    inputC0arr = [INTEGER_MAX] * len(list)
    for i in range(len(list)):
        inputC0arr[i] = list[i][0]
    inputC1arr = [INTEGER_MAX] * len(list)
    for i in range(len(list)):
        inputC1arr[i] = list[i][1]

    c0 = INTEGER_MAX
    c1 = INTEGER_MAX

    if g == Gate.BUFF:
        assert len(list) == 1
        c0 = list[0][0] + 1
        c1 = list[0][1] + 1
    elif g == Gate.AND:
        c0 = min(inputC0arr) + 1
        c1 = sum(inputC1arr) + 1
    elif g == Gate.OR:
        c0 = sum(inputC0arr) + 1
        c1 = min(inputC1arr) + 1
    elif g == Gate.XOR:
        # todo check if this XOR controllability works for 3+ input
        c0 = min(sum(inputC0arr), sum(inputC1arr)) + 1
        arr1 = [INTEGER_MAX] * len(list)
        arr2 = [INTEGER_MAX] * len(list)
        for i in range(1, len(list) + 1):
            idx = i - 1
            if i % 2 == 0:
                arr1[idx] = inputC0arr[idx]
                arr2[idx] = inputC1arr[idx]
            else:
                arr1[idx] = inputC1arr[idx]
                arr2[idx] = inputC0arr[idx]
        c1 = min(sum(arr1), sum(arr2)) + 1
    elif g == Gate.NOT:
        rlist = evalControllability(Gate.BUFF, list)
        rlist.reverse()
        return rlist
    elif g == Gate.NAND:
        rlist = evalControllability(Gate.AND, list)
        rlist.reverse()
        return rlist
    elif g == Gate.NOR:
        rlist = evalControllability(Gate.OR, list)
        rlist.reverse()
        return rlist
    elif g == Gate.XNOR:
        rlist = evalControllability(Gate.XOR, list)
        rlist.reverse()
        return rlist
    rtn = [c0, c1]
    assert rtn is not None
    return rtn


def hexToBinList(hex):
    msbList = []
    for i in range(len(hex)):
        hexchar = hex[i]
        if hexchar == '0':
            msbList.append(False)
            msbList.append(False)
            msbList.append(False)
            msbList.append(False)
        elif hexchar == '1':
            msbList.append(False)
            msbList.append(False)
            msbList.append(False)
            msbList.append(True)
        elif hexchar == '2':
            msbList.append(False)
            msbList.append(False)
            msbList.append(True)
            msbList.append(False)
        elif hexchar == '3':
            msbList.append(False)
            msbList.append(False)
            msbList.append(True)
            msbList.append(True)
        elif hexchar == '4':
            msbList.append(False)
            msbList.append(True)
            msbList.append(False)
            msbList.append(False)
        elif hexchar == '5':
            msbList.append(False)
            msbList.append(True)
            msbList.append(False)
            msbList.append(True)
        elif hexchar == '6':
            msbList.append(False)
            msbList.append(True)
            msbList.append(True)
            msbList.append(False)
        elif hexchar == '7':
            msbList.append(False)
            msbList.append(True)
            msbList.append(True)
            msbList.append(True)
        elif hexchar == '8':
            msbList.append(True)
            msbList.append(False)
            msbList.append(False)
            msbList.append(False)
        elif hexchar == '9':
            msbList.append(True)
            msbList.append(False)
            msbList.append(False)
            msbList.append(True)
        elif hexchar == 'A':
            msbList.append(True)
            msbList.append(False)
            msbList.append(True)
            msbList.append(False)
        elif hexchar == 'B':
            msbList.append(True)
            msbList.append(False)
            msbList.append(True)
            msbList.append(True)
        elif hexchar == 'C':
            msbList.append(True)
            msbList.append(True)
            msbList.append(False)
            msbList.append(False)
        elif hexchar == 'D':
            msbList.append(True)
            msbList.append(True)
            msbList.append(False)
            msbList.append(True)
        elif hexchar == 'E':
            msbList.append(True)
            msbList.append(True)
            msbList.append(True)
            msbList.append(False)
        else:
            assert hexchar == 'F'
            msbList.append(True)
            msbList.append(True)
            msbList.append(True)
            msbList.append(True)
    return msbList


# given some string of text, returns a list of strings representing node inputs
# Such that "INPUT(a1,b20,ccc)" returns ["a1","b20","ccc"]
def parseVarsOut(line):
    post1 = line.find("(")
    post2 = line.find(")")
    if post2 < post1 or post2 == post1 + 1:
        raise RuntimeError("Error: Malformed bench file, poor syntax involving '(' on line " + line)
    inner = line[post1 + 1:post2]
    varlist = inner.split(",")
    for i in range(len(varlist)):
        v = varlist[i]
        varlist[i] = str(v.strip())
    return varlist


gateEnumByName: dict[str, Gate] = {}

for g in Gate:
    gateEnumByName[g.value.upper()] = g


def getGateType(str):
    g = gateEnumByName.get(str.upper())
    return g


class Bench:

    def __init__(self, benchLines):

        #####
        self.inputs = list()
        self.outputs = list()
        self.nodes = set()

        #####
        self.nodeGateTypes: dict[str, Gate] = {}
        self.nodeGateInputs: dict[str, set] = {}

        #####
        self.nodesToLevel: dict[str, int] = {}
        self.levelsToNodes: dict[int, set] = {}

        #####
        self.nodeValues: dict[str, bool] = {}

        #####
        self.gateInputFaults: dict[str, dict] = {}
        self.gateOutputFaults: dict[str, bool] = {}

        ####
        self.controllabilities: dict[str, list] = {}

        self.mc_ref = None
        self.mc_sims = 0

        i = 0
        for line in benchLines:
            self.levelsToNodes[i] = set()
            if "INPUT" in line:
                varlist = parseVarsOut(line)
                assert len(varlist) == 1
                varname = str(varlist[0])
                self.inputs.append(varname)
                self.nodes.add(varname)
                self.levelsToNodes.get(0).add(varname)
                self.nodesToLevel[varname] = 0
            elif "OUTPUT" in line:
                varlist = parseVarsOut(line)
                assert len(varlist) == 1
                varname = str(varlist[0])
                self.nodes.add(varname)
                self.outputs.append(varname)
            elif "=" in line:
                post2 = line.find("=")
                gateName = line[:post2]
                gateName = gateName.strip()

                post1 = line.find("(")
                post2 = line.find(")")

                i = post1

                while i > 0:
                    if line[i - 1] == ' ' or line[i-1] == '=':
                        gateTypeStr = line[i:post1]
                        break;
                    i = i - 1
                #gateTypeStr = gateTypeStr
                gate = getGateType(gateTypeStr)

                varlist = parseVarsOut(line)
                self.nodeGateInputs[gateName] = set()
                for v in varlist:
                    self.nodeGateInputs[gateName].add(v)
                self.nodes.add(gateName)
                self.nodeGateTypes[gateName] = gate
            i = i + 1

        self.maxlvl = -1
        # Levelization
        while True:
            progress = False
            for varName in self.nodeGateInputs:
                if varName in self.nodesToLevel:
                    continue
                lvl = -1
                for inputVar in self.nodeGateInputs[varName]:
                    if inputVar not in self.nodesToLevel:
                        lvl = -1
                        break
                    else:
                        lvl = max(lvl, self.nodesToLevel.get(inputVar) + 1)
                if lvl != -1:
                    self.nodesToLevel[varName] = lvl
                    if self.levelsToNodes.get(lvl) is None:
                        self.levelsToNodes[lvl] = {varName}
                    else:
                        self.levelsToNodes.get(lvl).add(varName)
                    progress = True
                    self.maxlvl = max(lvl, self.maxlvl)
            if progress is False:
                break

        # assert all types
        for nodeName in self.nodes:
            assert isinstance(nodeName, str)
        for nodeName in self.nodeGateInputs:
            assert isinstance(nodeName, str)
        for nodeName in self.nodesToLevel:
            assert isinstance(nodeName, str)

        # controllability mapping
        for i in range(self.maxlvl + 1):
            nodes = self.levelsToNodes[i]
            if i == 0:
                for node in nodes:
                    self.controllabilities[node] = [1, 1]
            else:
                for node in nodes:
                    inputControllabilitiesList = [list()] * len(self.nodeGateInputs[node])
                    j = 0
                    for gateInput in self.nodeGateInputs[node]:
                        v1 = self.controllabilities[gateInput]
                        inputControllabilitiesList[j] = v1
                        j = j + 1
                    # print("Evaluating for " + node)
                    gateType = self.nodeGateTypes[node]
                    eval = evalControllability(gateType, inputControllabilitiesList)
                    assert eval is not None
                    self.controllabilities[node] = eval

    def printFaultList(self):
        # Create entire fault list:
        print()

        for n in self.nodes:
            # print fautls of gates input

            if n in self.inputs:  # unless node is not an input
                continue  # then just skip
            for inp in self.nodeGateInputs[n]:
                ti = str(n) + "-" + str(inp) + "-0" + ", " + str(n) + "-" + str(inp) + "-1" + ", "
                limitedPrint(ti)

            # print faults of gate output
            tp = str(n) + "-0, " + str(n) + "-1, "
            limitedPrint(tp)
        print()

    def testAllFaults(self, tv):
        for n in self.nodes:

            # test fault at a input
            if n in self.inputs:  # unless node is not an input
                continue  # then just skip
            for inp in self.nodeGateInputs[n]:
                self.addGateInputFault(n, inp, False)
                self.printResult(tv)
                self.addGateInputFault(n, inp, True)
                self.printResult(tv)
                # ok now remove fault
                self.removeGateInputFault(n, inp)

            # test output fault
            self.addGateOutputFault(n, True)
            self.printResult(tv)
            self.addGateOutputFault(n, False)
            self.printResult(tv)
            self.removeGateOutputFault(n)

    def faultCatchAnalysis(self, tv):
        tests = 0
        catches = 0

        for n in self.nodes:

            # test fault at a input
            if n in self.inputs:  # unless node is not an input
                continue  # then just skip
            for inp in self.nodeGateInputs[n]:
                b = self.gateInputFaultIsDetected(tv, n, inp, True)
                tests = tests + 1
                if b:
                    catches = catches + 1
                b = self.gateInputFaultIsDetected(tv, n, inp, False)
                tests = tests + 1
                if b:
                    catches = catches + 1

            # test output fault
            b = self.gateOutputFaultIsDetected(tv, n, True)
            tests = tests + 1
            if b:
                catches = catches + 1
            b = self.gateOutputFaultIsDetected(tv, n, False)
            tests = tests + 1
            if b:
                catches = catches + 1

        percentage_catch = 100 * (catches / tests)
        print("")
        print("TV ", end="")
        self.printTV()
        print(" Detects " + str(round(percentage_catch, 6)) + "% of all faults, " + str(catches) + "/" + str(tests))

    def printTV(self):
        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            if (self.nodeValues[varname] == True):
                print("1", end="")
            else:
                assert self.nodeValues[varname] == False
                print("0", end="")

    def gateOutputFaultIsDetected(self, tv, flt_node, flt_val):
        # most likely these maps are already empty but to be sure:
        self.gateInputFaults = {}
        self.gateOutputFaults = {}

        output1 = self.evaluate(tv)
        self.addGateOutputFault(flt_node, flt_val)
        output2 = self.evaluate(tv)
        self.removeGateOutputFault(flt_node)
        return self.listIsDifferent(output1, output2)

    def gateInputFaultIsDetected(self, tv, gateVarname, flt_inp, flt_val):
        # most likely these maps are already empty but to be sure:
        self.gateInputFaults = {}
        self.gateOutputFaults = {}

        output1 = self.evaluate(tv)
        self.addGateInputFault(gateVarname, flt_inp, flt_val)
        output2 = self.evaluate(tv)
        self.removeGateInputFault(gateVarname, flt_inp)
        return self.listIsDifferent(output1, output2)

    # given two lists of boolean values (representing outputs in this project)
    # returns true if they are  different
    # otherwise, returns false
    def listIsDifferent(self, a, b):
        assert len(a) == len(b)
        for i in range(len(a)):
            if a[i] != b[i]:
                # if they are different
                return True
        return False  # lists are same

    # given some list of str (node names), give their values
    # only call on variables you know were already evaluated
    def resolveInputs(self, gateVarname, inlist):
        sz = len(inlist)
        b = [False] * sz
        someFaults = self.gateInputFaults.__contains__(gateVarname)
        for i in range(len(inlist)):
            if someFaults and self.gateInputFaults[gateVarname].__contains__(inlist[i]):
                # print("Fault at input  " + inlist[i] + " SA-" + str(self.gateInputFaults[gateVarname][inlist[i]]))
                b[i] = self.gateInputFaults[gateVarname][inlist[i]]
            else:
                b[i] = self.nodeValues[inlist[i]]
        return b

    def randomizeInputTV(self):
        b = [False] * len(self.inputs)
        for i in range(len(self.inputs)):
            b[i] = random.choice([True, False])
        return b

    # evaluates the circuit given some tv [boolean list] and a fault map {varName, boolean}
    # returns the circuit output
    def evaluate(self, tv_in):
        tv = tv_in[::-1]
        bout = [False] * len(self.outputs)
        # assert len(tv) == len(self.nodeInputs)
        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            self.nodeValues[varname] = bool(tv[i])
        for i in range(1, self.maxlvl + 1):
            assignNow = self.levelsToNodes.get(i)
            for varname in assignNow:
                if varname in self.gateOutputFaults:
                    self.nodeValues[varname] = self.gateOutputFaults[varname]
                    continue
                gate = self.nodeGateTypes.get(varname)
                inputs = list(self.nodeGateInputs.get(varname))
                eval = evalGate(gate, self.resolveInputs(varname, inputs))
                self.nodeValues[varname] = eval
        for i in range(len(self.outputs)):
            varname = self.outputs[i]
            bout[i] = self.nodeValues[varname]
        return bout

    def addGateInputFault(self, gateVarName, gateInputVarname, val):
        assert type(val) is bool
        assert self.nodeGateInputs[gateVarName].__contains__(gateInputVarname)
        if not self.gateInputFaults.__contains__(gateVarName):
            self.gateInputFaults[gateVarName] = {}
        self.gateInputFaults[gateVarName][gateInputVarname] = val

    def removeGateInputFault(self, gateVarname, gateInputVarname):
        del self.gateInputFaults[gateVarname][gateInputVarname]

    def addGateOutputFault(self, gateVarName, val):
        assert type(val) is bool
        self.gateOutputFaults[gateVarName] = val

    def removeGateOutputFault(self, gateVarname):
        del self.gateOutputFaults[gateVarname]

    def printResult(self, tv):
        a = self.evaluate(tv)

        print("")
        print("Faults:")

        for varname in self.gateInputFaults:
            for inputVar in self.gateInputFaults[varname]:
                b = self.gateInputFaults[varname][inputVar]
                if b:
                    print(varname + "-" + inputVar + "-1")
                else:
                    assert b == False
                    print(varname + "-" + inputVar + "-0")

        for varname in self.gateOutputFaults:
            b = self.gateOutputFaults[varname]
            if (b):
                print(varname + "-1")
            else:
                assert b == False
                print(varname + "-0")

        print("")

        print("Input:")
        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            if (self.nodeValues[varname] == True):
                print("1", end="")
            else:
                assert self.nodeValues[varname] == False
                print("0", end="")

        print("")

        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            print(str(varname) + " ", end="")

        print("")
        print("")
        print("Output:")

        for i in range(len(a)):
            if (a[i] == True):
                print("1", end="")
            else:
                assert a[i] == False
                print("0", end="")
        print("")
        for i in range(len(self.outputs)):
            varname = self.outputs[i]
            print(str(varname) + " ", end="")
        print("")

    def printControlabities(self):
        for i in range(self.maxlvl + 1):
            nodes = self.levelsToNodes[i]
            print("L" + str(i))
            for node in nodes:
                c_n = self.controllabilities[node]
                c0 = c_n[0]
                c1 = c_n[1]
                print(" " + node + " (" + str(c0) + ", " + str(c1) + "), ", end="")
            print("\n", end="")

    def printResultWithIntermediates(self, tv):
        a = self.evaluate(tv)

        print("")
        print("Faults:")

        for varname in self.gateInputFaults:
            for inputVar in self.gateInputFaults[varname]:
                b = self.gateInputFaults[varname][inputVar]
                if b:
                    print(varname + "-" + inputVar + "-1")
                else:
                    assert b == False
                    print(varname + "-" + inputVar + "-0")

        for varname in self.gateOutputFaults:
            b = self.gateOutputFaults[varname]
            if (b):
                print(varname + "-1")
            else:
                assert b == False
                print(varname + "-0")

        print("")

        print("Input:")
        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            if (self.nodeValues[varname] == True):
                print("1", end="")
            else:
                assert self.nodeValues[varname] == False
                print("0", end="")

        print("")

        for i in range(len(self.inputs)):
            varname = self.inputs[i]
            print(str(varname) + " ", end="")

        print("")
        print("Progression to output:")
        for lvv in range(self.maxlvl + 1):
            print("-------->")
            print("Level " + str(lvv) + ":")
            for n in self.levelsToNodes[lvv]:
                b = self.nodeValues[n]
                if b:
                    print(str(n) + " 1")
                else:
                    print(str(n) + " 0")

        print("")
        print("")
        print("Output:")

        for i in range(len(a)):
            if (a[i] == True):
                print("1", end="")
            else:
                assert a[i] == False
                print("0", end="")
        print("")
        for i in range(len(self.outputs)):
            varname = self.outputs[i]
            print(str(varname) + " ", end="")
        print("")

    def nMonteCarlo(self, n):
        #               v size 2 array of times 0,1
        mc: dict[str, list] = {}
        total_iterations = n #of times to simulate random tvs
        for i in range(total_iterations):
            tv = self.randomizeInputTV()
            self.evaluate(tv)
            for node in self.nodes:
                if node not in mc:
                    mc[node] = [0, 0]
                valFromSim = self.nodeValues[node]
                if valFromSim == True:
                    mc[node][1] = mc[node][1] + 1
                else:
                    mc[node][0] = mc[node][0] + 1
        #report results:
        #Print by level
        for i in range(self.maxlvl + 1):
            nodes = self.levelsToNodes[i]
            print("L" + str(i))
            for node in nodes:
                perc0 = round(100*mc[node][0] / total_iterations,2)
                perc1 = round(100*mc[node][1] / total_iterations,2)
                print(" " + node + " (" + str(perc0) + "%, " + str(perc1) + "%), ", end="")
            print("\n", end="")
        self.mc_ref = mc
        self.mc_sims = total_iterations

    def csvSCOAPvsMC(self,name):
        #how many rows in csv?
        #rows will be the amount of nodes
        numRows = len(self.nodes)
        numCol = 5
        writePos = 0
        data = [None] * (numRows+1) #but one extra row for headers
        for i in range(len(data)):
            data[i] = [None]*numCol

        data[0] = ["Node","c(c0)","c(c1)","mc_0","mc_1"]
        writePos=writePos+1
        for i in range(self.maxlvl+1):
            nodes = self.levelsToNodes[i]
            for node in nodes:
                #scoap values
                c0 = self.controllabilities[node][0]
                c1 = self.controllabilities[node][1]
                #mc percentages
                c0perc = 100 * self.mc_ref[node][0] / self.mc_sims
                c1perc = 100 * self.mc_ref[node][1] / self.mc_sims
                data[writePos][0] = str(node)
                data[writePos][1] = str(c0)
                data[writePos][2] = str(c1)
                data[writePos][3] = str(c0perc) + "%"
                data[writePos][4] = str(c1perc) + "%"
                writePos= writePos+1

        with open(name+'.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row
            writer.writerow(data[0])
            # Write the data rows
            writer.writerows(data[1:])

        print("saved csv to " + name + ".csv")