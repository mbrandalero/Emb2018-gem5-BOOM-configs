# -*- coding: utf-8 -*-

from __future__     import print_function

import m5
from m5.objects     import *
from m5.util        import addToPath

from argparse       import ArgumentParser

addToPath("./systems/")
addToPath("./systems/cpus/")
addToPath("./systems/caches/")
addToPath("./systems/bt/")

from benchmarks     import PARSECBenchmarkManager
from benchmarks     import MiBenchBenchmarkManager

from system_manager import SystemManager

# Beautiful COLors for formatting
class bcol:
    MAGENTA    = '\033[95m'
    BLUE       = '\033[94m'
    GREEN      = '\033[92m'
    YELLOW     = '\033[93m'
    RED        = '\033[91m'
    BOLD       = '\033[1m'
    UNDERLINE  = '\033[4m'
    END        = '\033[0m'

    @staticmethod
    def H(msg):
        return bcol.MAGENTA + msg + bcol.END

    @staticmethod
    def I(msg):
        return bcol.BLUE + msg + bcol.END

    @staticmethod
    def W(msg):
        return bcol.YELLOW + msg + bcol.END

    @staticmethod
    def OK(msg):
        return bcol.GREEN + msg + bcol.END

    @staticmethod
    def E(msg):
        return bcol.RED + msg + bcol.END


print(bcol.H( \
"***************************************************************************"))
print(bcol.H( \
"********************** gem5 configuration script **************************"))
print(bcol.H( \
"***************************** simulate.py *********************************"))
print(bcol.H( \
"***************************************************************************"))
print("")

############################################################
## Script options
############################################################

main_parser = ArgumentParser(description = "Top-level simulation script.")
main_parser.add_argument("--env", default = "",
                    help = """List of ";-separated" environment variables to be
                    set before running the binary. Ex: --env "VAR1=X;VAR2=Y""")
main_parser.add_argument("--cpu",
                    help = "CPU to use.",
                         choices = SystemManager.available_cpus.keys(),
                         default = SystemManager.available_cpus.keys()[0])

subparsers = main_parser.add_subparsers(
    title = "Commands available",
    help  = "Use \"<command> --help\" for additional options.",
    dest = "subcommand")
parser_other  = subparsers.add_parser(
    'run-benchmark',
    help = "Runs your own benchmark.")

# Other benchmarks
parser_other.add_argument(
    "-c", "--cmd", default = "",
    help = "Binary file to run.")
parser_other.add_argument(
    "-o", "--options", default = "",
    help = """Command-line options to the binary.
    Use "" around the string.""")

args = main_parser.parse_args()

############################################################
# Setup system
############################################################

print(bcol.I("Setting up system ..."))
print(bcol.W("Using " + args.cpu + " CPU."))
system = SystemManager().getSystem(args)
print(bcol.OK("Done."))
print("")

############################################################
# Setup process
############################################################

print(bcol.I("Setting up the process to run ..."))
process = Process()

if args.subcommand == "run-benchmark":
    print(bcol.W("Custom benchmark selected."))
    print(bcol.W("Command           : " + args.cmd))
    print(bcol.W("Command-line args : " + (args.options
                                          if args.options else "(none)")))

    if args.cmd:
        process.executable = args.cmd
        process.cmd = args.cmd

        if args.options != "": # Args.args is a string
            process.cmd += args.options.split() # That becomes a list here
    else:
        exit(bcol.E("Must specify the program to run (--cmd <program>)."))
    print(bcol.OK("Done"))
else:
    exit(bcol.E("FATAL: command ") + bcol.E(args.subcommand) + \
         bcol.E(" is invalid."))
print("")

############################################################
## Setup environmental variables
############################################################

print(bcol.I("Setting environmental variables ..."))
if args.env:
    evars = args.env.split(";")
    process.env = evars

    print(bcol.W("\n".join([str(i) for i in evars])))
else:
    print(bcol.W("(no environmental variables to set)"))
print(bcol.OK("Done"))
print("")

############################################################
## Instantiate stuff
############################################################

print(bcol.I("Instantiating process ..."))
print(bcol.I("Program to run: " + \
                "".join([str(i)+" " for i in process.cmd])))

for core in system.cpu:
    core.workload = process
    core.createThreads()
print(bcol.OK("Done"))
print("")

print(bcol.I("Instantiating system ..."))
root = Root(full_system = False, system = system)
m5.instantiate()
print(bcol.OK("Done"))
print("")

print(bcol.H( \
"*********************** Beginning gem5 simulation ************************"))
simulation = m5.simulate()
if simulation.getCause() == "exiting with last active thread context":
    print(bcol.H( \
"**************************************************************************"))
    print(bcol.OK("Done."))
    print(bcol.OK("Finished at tick %i." %(m5.curTick())))
    print(bcol.OK("Status: %s." % (simulation.getCause())))
    print(bcol.H( \
"**************************************************************************"))
else:
    print(bcol.H( \
"**************************************************************************"))
    print(bcol.E("Status: %s." % (simulation.getCause())))
    print(bcol.H( \
"**************************************************************************"))
