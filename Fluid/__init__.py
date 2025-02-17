# right hand, Y up
# length: m
# mass: kg
# time: s

import os

from Fluid.SPH.SPH_Solver import SPH_Solver
from Fluid.WCSPH.WCSPH_Solver import WCSPH_Solver
from Fluid.PCISPH.PCISPH_Solver import PCISPH_Solver

from Fluid._basic import *

os.environ["TI_LOG_LEVEL"] = "warn"
import taichi as ti

# global init
ti.init(
    arch=ti.cuda,
    default_ip=ti.i32,
    default_fp=ti.f32
)

def simulation_entry(args):
    # block_3rd_output()
    log("start simulation...")
    solver = None
    if args.method == "sph":
        solver = SPH_Solver()
    elif args.method == "wcsph":
        solver = WCSPH_Solver()
    elif args.method == "pcisph":
        solver = PCISPH_Solver()
    else:
        log(f"{args.method} is not a available algorithm")

    if solver is None:
        return
    
    solver.cmd_args = args

    # build scene with scene json file
    if not solver.build_scene():
        log("cant build scene, exiting...")
        return
    
    solver.run()

def render_entry(args):
    from Fluid.Render.Renderer import Renderer
    log("start rendering...")
    renderer = Renderer(args)
    renderer.render_all()

def build_surface_entry(args):
    log("start building fliud surface...")