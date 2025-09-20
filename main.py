file_path = "c17.bench"


benchLines = []

nodeInputs = set()
nodeOutputs =  set()
gate_type_set = {"NOT", "AND", "OR", "NOR", "XOR", "XNOR", "NAND"}
#####
nodeGate_TypeMap = {}
nodeGate_InputMap = {}

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

i=0
for line in benchLines:
    i=i+1
    if "INPUT" in line:
        post1 = line.find("(")
        post2 = line.find(")")
        if post2 < post1 or post2 == post1+1:
            raise RuntimeError("Error: Malformed bench file, poor syntax involving '(' at line " + i)
        varName = line[post1+1:post2]
        nodeInputs.add(varName.strip())
    elif "OUTPUT" in line:
        post1 = line.find("(")
        post2 = line.find(")")
        if post2 < post1 or post2 == post1+1:
            raise RuntimeError("Error: Malformed bench file, poor syntax involving '(' at line " + i)
        varName = line[post1+1:post2]
        nodeOutputs.add(varName.strip())
    elif "=" in line:
        post2 = line.find("=")
        varName = line[:post2]
        varName = varName.strip()

        gateType = "NONE"

        for type in gate_type_set:
            if type in line:
                gateType = type

        if gateType == "NONE":
            raise RuntimeError("Error: Gate is not of a valid type at line " + i)

        post1 = line.find("(")
        post2 = line.find(")")
        if post2 < post1 or post2 == post1 + 1:
            raise RuntimeError("Error: Malformed bench file, poor syntax involving '(' at line " + i)
        varsContained = line[post1 + 1:post2]
        varsContained = varsContained.split(",")
        varsContained = [var.strip() for var in varsContained]  # Strip each element individually
        nodeGate_InputMap[varName] = varsContained
        nodeGate_TypeMap[varName] = gateType.strip()

#Build output list:
outputNodesStr = "Output Nodes: ["
i=0
for name in nodeOutputs:
    outputNodesStr = outputNodesStr + name
    if(i != len(nodeOutputs)-1):
        outputNodesStr = outputNodesStr + ", "
    else:
        outputNodesStr = outputNodesStr + "]"
    i=i+1

#Build input list:
inputNodeStr = "Input Nodes : ["
i=0
for name in nodeInputs:
    inputNodeStr = inputNodeStr + name
    if(i != len(nodeInputs)-1):
        inputNodeStr = inputNodeStr + ", "
    else:
        inputNodeStr = inputNodeStr + "]"
    i = i + 1
print("----------------------------")
print(inputNodeStr)
print(outputNodesStr)
print("----------------------------")
print("Node description as follows:")
for name in nodeGate_TypeMap:
    desc = ""
    type = nodeGate_TypeMap.get(name)
    inputStr = str(nodeGate_InputMap.get(name))
    inputStr = inputStr.replace("'","").replace("\"","").replace(" ","").replace(",",", ")
    desc = desc + name
    if len(name) == 1:
        desc = desc + " "
    desc = desc + ": " + type
    if type == "OR":
        desc = desc + " "
    desc = desc + " of " + inputStr
    print(desc)
print("----------------------------")



levels: dict[str, int] = {}

for varName in nodeInputs:
    levels[varName] = 0

while True: # could be optimized later..
    progress=False
    for varName in nodeGate_InputMap:
        if varName in levels:
            continue
        l = -1
        for inputVar in nodeGate_InputMap[varName]:
            if inputVar not in levels or levels[inputVar] is None:
                l = -1
                break
            else:
                l = max(l, levels[inputVar])
        if l != -1:
            levels[varName] = l+1
            progress = True
    if progress is False:
        break

print("Node levels:")
print("Node | Level")

for x in levels:
    addSpace = 4 - len(x)
    if addSpace < 0:
        addSpace = 0
    print(str(x) + " "*addSpace + ": " + str(levels[x]))

print("----------------------------")