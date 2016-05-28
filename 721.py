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
    def __init__(self, name, cap=None, cost=None, bounds=[]):
        self.name = name
        self.capacity = cap
        self.cost = cost
        self.bounds = []
        for bound in bounds:
            self.bounds.append(bound)
        self.demandflow = 0
    
    def __repr__(self):
        s = self.name 
        s = s + ' cap:' + str(self.cap)
        s = s + ' cost:' + str(self.cost)
        return s
    
    def obj(self):
        return str(self.cost) + ' x' + self.name

def getDVRange():
    #minh = float(input("Minimum Demand Volume: "))
    #maxh = float(input("Maximum Demand Volume: "))
    minh = float(sys.argv[1])
    maxh = float(sys.argv[2])
    return (minh, maxh)
    
    
def write_objective(f, links):
    s = "Minimize\n  "
    l = len(links)
    for i in range(l):
        s += links[i].obj()
        if (i < l - 1):
            s += " + "
        else:
            s += '\n'
    f.write(s)

def write_constraints(f, links, h):
    # Write demand comstraints
    s = "Subject to\n  demandflow: "
    for link in links:
        s += 'x' + link.name
        if (link != links[-1]):
            s += ' + '
        else:
            s += ' = ' + str(h) + '\n'
    f.write(s)
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



link1 = Link('12',10,10,("0 <= x12",))
link2 = Link('132',10,5,("0 <= x132",))
links = (link1,link2)

table = open(tablefile,'w')
table.write('h,')
for link in links:
    table.write('x' + link.name + ',')
table.write('\n')

# loop over demand volumes
minh, maxh = getDVRange()
for i in range(int(minh*10),int(maxh*10)+1):
    # Initialize problem
    for link in links:
        link.demandflow = 0
    f = open(filename, 'w')
    h = (i / 10.0)

    write_objective(f, links)
    write_constraints(f, links, h)
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
