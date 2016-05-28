#!/usr/bin/env python3

import sys,os
import subprocess

minh = 0
maxh = 0
filename = "default.lp"
tablefile = "default.csv"
output = "default.csv"
shell = "bash"
command = "cplex -c \"read {}\" \"optimize\" \"display solution variables -\""

class Link(object):
    def __init__(self, name, bounds=[], cost=None, cap=None):
        self.name = name
        self.capacity = cap
        self.cost = cost
        self.bounds = bounds
        self.demandflow = 0
    
    def __repr__(self):
        s = "LINK<" + self.name 
        s = s + ' cap:' + str(self.capacity)
        s = s + ' cost:' + str(self.cost)
        s = s + ' bounds:' + repr(self.bounds)
        return s + '>'
    
    def obj(self):
        return str(self.cost) + ' x' + self.name

class Constraint(object):
    def __init__(self, name, lhs=[], eq=None, rhs=None):
        self.name = name
        self.lhs = lhs
        self.eq = eq
        self.rhs = rhs

    def __repr__(self):
        s = "CSTR<" + self.name 
        s = s + ' '
        return s + '>'
    
    def __str__(self):
        s += "{:<12}".format(cstr.name + ':')
        for i in cstr.lhs:
            o = (('',''),(' -',' +'))[i != cstr.lhs[0]][i[0] >= 0]
            s += o + str(i[0]) + ' x' + i[1].name + ' '
        s += cstr.eq + ' ' + str(cstr.rhs)
        return s
        
class Bound(object):
    def __init__(self, lhs=None, eq=None, rhs=None):
        self.lhs = lhs
        self.eq = eq
        self.rhs = rhs

    def __repr__(self):
        s = "BND <"
        s = s + ' '
        return s + '>'
    
    def __str__(self):
        s = 'x' + self.lhs.name
        s += ' ' + self.eq + ' ' + str(self.rhs)
        return s
        

def getDVRange():
    #minh = float(input("Minimum Demand Volume: "))
    #maxh = float(input("Maximum Demand Volume: "))
    minh = float(sys.argv[1])
    maxh = float(sys.argv[2])
    return (minh, maxh)
    
    
def write_objective(f, links):
    s = "Minimize\n"
    l = len(links)
    s += "  {:<12}".format("objective:")
    for i in range(l):
        s += links[i].obj()
        if (i < l - 1):
            s += " + "
        else:
            s += '\n'
    f.write(s)

def write_constraints(f, constraints):
    # Write demand comstraints
    s = "Subject to\n"
    for cstr in constraints:
        s += "  " + str(cstr) + '\n'
    f.write(s)

def write_capacities(f, links):
    # Write capacity constraints
    s = ""
    for link in links:
        s += "  c{:<11}".format(link.name + ':')
        s += 'x' + link.name + " <= " + str(link.capacity) + '\n'
    f.write(s)

def write_bounds(f, links):
    s = "Bounds\n"
    for link in links:
        for bound in link.bounds:
            s += "  " + bound + '\n'
    f.write(s)

def write_end(f):
    f.write("End\n")


def run_cplex(shell, cplex, filename):
    return subprocess.getoutput(command.format(filename))


# Set up problem
links = [
Link("1",[(0,"<=")],1.0),
Link("2",[(0,"<=")],9.0),
Link("3",[(0,"<=")],3.3),
Link("4",[(0,"<=")],1.7)
]
for link in links: print(link)

# TODO map factors to their links and 
#   construct constraints dynamically from links list
constraints = [
Constraint("demandflow", [(1,link1),(1,link2)], '=', 2.0),
Constraint("cap1", [(1,link1)], '<=', 10),
Constraint("cap2", [(1,link2)], '<=', 10)
]
for cstr in constraints: print(cstr)

# Write head of the table
table = open(tablefile,'w')
table.write('h,')
for link in links:
    table.write('x' + link.name + ',')
table.write('\n')

# Loop over demand volumes
minh, maxh = getDVRange()
for i in range(int(minh*10),int(maxh*10)+1):
    # Initialize problem
    for link in links:
        link.demandflow = 0
    f = open(filename, 'w')
    h = (i / 10.0)

    write_objective(f, links)
    write_constraints(f, constraints)
    write_bounds(f, links)
    write_end(f)
    f.close()

    out = run_cplex(shell, command, filename)
    result = out[out.index("Variable Name"):]
    results = result.split('\n')
    for r in results: #THIS NEEDS OPTIMIZING
        for link in links:
            if r.startswith('x' + link.name):
                link.demandflow = float(r.split()[-1])
    table.write(str(h) + ',')
    for link in links:
        table.write(str(link.demandflow) + ',')
    table.write('\n')
        
table.close()
