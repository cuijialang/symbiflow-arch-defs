#!/usr/bin/env python3
"""
Convert a Verilog simulation model to a VPR `model.xml`

The following Verilog attributes are considered on ports:
    - `(* CLOCK *)` : force a given port to be a clock

    - `(* ASSOC_CLOCK="RDCLK" *)` : force a port's associated clock to a given value

The following Verilog attributes are considered on modules:
    - `(* MODEL_NAME="model" *)` : override the name used for <model> and for
    ".subckt name" in the BLIF model. Mostly intended for use with w.py, when several
    different pb_types implement the same model.

"""
import argparse, re
import os, tempfile, sys

import lxml.etree as ET

import yosys.run
from yosys.json import YosysJson


parser = argparse.ArgumentParser(description=__doc__.strip())
parser.add_argument(
    'infiles',
    metavar='input.v', type=str, nargs='+',
    help="""\
One or more Verilog input files, that will be passed to Yosys internally.
They should be enough to generate a flattened representation of the model,
so that paths through the model can be determined.
""")
parser.add_argument(
    '--top',
    help="""\
Top level module, not needed if only one module exists across all input Verilog
files, in which case that module will be used as the top level.
""")
parser.add_argument(
    '-o',
    help="""\
Output filename, default 'model.xml'
""")

args = parser.parse_args()

aig_json = yosys.run.vlog_to_json(args.infiles, True, True)

if "top" in args:
    yj = YosysJson(aig_json, args.top)
else:
    yj = YosysJson(aig_json)

top = yj.top
if top is None:
    print("ERROR: more than one module in design, cannot detect top level. Manually specify the top level module using --top")
    sys.exit(1)

tmod = yj.top_module
models_xml = ET.Element("models")

topname = tmod.attr("MODEL_NAME", top)

model_xml = ET.SubElement(models_xml, "model", {'name': topname})
ports = tmod.ports

inports_xml = ET.SubElement(model_xml, "input_ports")
outports_xml = ET.SubElement(model_xml, "output_ports")

clocks = yosys.run.list_clocks(args.infiles, top)
clk_sigs = dict()
for clk in clocks:
    clk_sigs[clk] = yosys.run.get_clock_assoc_signals(args.infiles, top, clk)

for name, width, iodir in ports:
    attrs = dict(name=name)
    sinks = yosys.run.get_combinational_sinks(args.infiles, top, name)
    if len(sinks) > 0 and iodir == "input":
        attrs["combinational_sink_ports"] = " ".join(sinks)
    if name in clocks:
        attrs["is_clock"] = "1"
    for clk in clocks:
        if name in clk_sigs[clk]:
            attrs["clock"] = clk
    if iodir == "input":
        ET.SubElement(inports_xml, "port", attrs)
    elif iodir == "output":
        ET.SubElement(outports_xml, "port", attrs)
    else:
        assert(False) #how does VPR specify inout (only applicable for PACKAGEPIN of an IO primitive)

outfile = "model.xml"
if "o" in args and args.o is not None:
    outfile = args.o

f = open(outfile, 'w')
f.write(ET.tostring(models_xml, pretty_print=True).decode('utf-8'))
f.close()