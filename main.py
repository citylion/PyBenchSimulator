from benchlib import *
file_path = "hw1.bench"


benchLines = []

try:
    with open(file_path, 'r') as file:
        i=0
        for line in file:
            benchLines.append(line.strip())
            i=i+1
except FileNotFoundError:
    print("Error: No such file \"" + file_path+ "\" present in this script's directory!")
except Exception as e:
    print("Error: Exception as follows, " + str(e))


b = Bench(benchLines)


#2
b.printFaultList()



'''
#3i
tv = [1,1,0]
b.printResult(tv)
'''

'''
#3ii
tv = [1,0,1]
b.printResult(tv)
'''

'''
#4
print("Simulation of " + file_path)
print("")
tv = hexToBinList("00050007")

b.printResultWithIntermediates(tv)
'''


'''
#5i
#fault sim
print("Fault simulation of " + file_path)
tv = [1,1,0] #cba

b.addGateOutputFault("y",True)
b.printResult(tv)
'''

'''
#5ii
#fault sim
print("Fault simulation of " + file_path)
tv = [1,1,0] #cba

b.addGateOutputFault("y",False)
b.printResult(tv)
'''

'''
#6i
#fault sim
print("Fault simulation of " + file_path)

tv = [0,0,0,0,0]

b.addGateInputFault("22","10",False)

b.printResult(tv)
'''

'''
#6ii
#fault sim
print("Fault simulation of " + file_path)

tv = [1,1,1,1,1]

b.addGateInputFault("22","10",False)

b.printResult(tv)
'''

'''
#7i
tv = [1,1,0]
b.testAllFaults(tv)
'''

'''
#7ii
tv = [1,0,1]
b.testAllFaults(tv)
'''


'''
#8.i
print("Fault simulation of " + file_path)
tv = hexToBinList("000ABCD1234")
b.testAllFaults(tv)
'''

'''
#8.ii
for i in range(11):
    tv = b.randomizeInputTV()
    b.faultCatchAnalysis(tv)
'''