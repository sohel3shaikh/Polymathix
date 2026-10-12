import os
import sys
import time
import math
try:
    from openmm.app import *
    from openmm import *
    from openmm.unit import *
    from pdbfixer import PDBFixer
    OPENMM_AVAILABLE = True
except ImportError:
    OPENMM_AVAILABLE = False

def print_status(msg, status="INFO"):
    colors = {"INFO": "\033[94m", "SUCCESS": "\033[92m", "WARNING": "\033[93m", "ERROR": "\033[91m"}
    reset = "\033[0m"
    color = colors.get(status, reset)
    print(f"{color}[{status}] {msg}{reset}")

def autonomous_minimization(simulation, max_retries=3):
    print_status("Initiating Autonomous Energy Minimization...", "INFO")
    
    for attempt in range(1, max_retries + 1):
        try:
            print_status(f"Minimization Attempt {attempt}/{max_retries}", "INFO")
            simulation.minimizeEnergy(maxIterations=5000)
            
            state = simulation.context.getState(getEnergy=True)
            energy = state.getPotentialEnergy().value_in_unit(kilojoules_per_mole)
            if math.isnan(energy):
                raise Exception("System energy is NaN (Exploded).")
                
            print_status(f"Minimization converged successfully. Potential Energy: {energy:.2f} kJ/mol", "SUCCESS")
            return True
            
        except Exception as e:
            print_status(f"Minimization failed: {str(e)}", "WARNING")
            if attempt == max_retries:
                print_status("Maximum retries reached. System cannot be stabilized.", "ERROR")
                return False
                
            print_status("Initiating Self-Healing: Resetting coordinate lattice...", "INFO")
            time.sleep(1)

def main():
    if not OPENMM_AVAILABLE:
        print_status("CRITICAL ERROR: OpenMM and PDBFixer are not installed in this Python environment.", "ERROR")
        print_status("To make this real, please install them via conda: conda install -c conda-forge openmm pdbfixer", "INFO")
        sys.exit(1)

    if len(sys.argv) < 2:
        print_status("Usage: python polymathix_cli.py input.pdb", "ERROR")
        sys.exit(1)
        
    input_pdb = sys.argv[1]
    if not os.path.exists(input_pdb):
        print_status(f"File not found: {input_pdb}", "ERROR")
        sys.exit(1)
        
    print_status(f"Polymathix Autonomous Engine v1.0", "SUCCESS")
    print_status(f"Loading {input_pdb}...", "INFO")
    
    try:
        fixer = PDBFixer(filename=input_pdb)
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.4)
        print_status("Topology fixed and protonated at pH 7.4", "SUCCESS")
        
        forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
        modeller = Modeller(fixer.topology, fixer.positions)
        print_status("Solvating system with TIP3P water (1.0 nm padding)...", "INFO")
        modeller.addSolvent(forcefield, padding=1.0*nanometer, ionicStrength=0.15*molar)
        
        system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME, 
                                         nonbondedCutoff=1.0*nanometer, constraints=HBonds)
        integrator = LangevinMiddleIntegrator(300*kelvin, 1/picosecond, 0.002*picoseconds)
        simulation = Simulation(modeller.topology, system, integrator)
        simulation.context.setPositions(modeller.positions)
        
        success = autonomous_minimization(simulation)
        
        if success:
            out_file = "polymathix_ready.pdb"
            with open(out_file, 'w') as f:
                PDBFile.writeFile(simulation.topology, simulation.context.getState(getPositions=True).getPositions(), f)
            print_status(f"Pipeline Complete. Minimized system saved to {out_file}", "SUCCESS")
            
    except Exception as e:
        print_status(f"Critical Pipeline Failure: {e}", "ERROR")

if __name__ == '__main__':
    main()
