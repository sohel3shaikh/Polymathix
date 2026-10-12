import matplotlib.pyplot as plt
import os
import numpy as np

def generate_energy_plot(output_path):
    # Simulated energy curve for the minimization process
    steps = np.arange(0, 100, 1)
    # Exponential decay to simulate minimization convergence
    energy = -140000 - 6000 * (1 - np.exp(-0.1 * steps)) + np.random.normal(0, 100, len(steps))
    
    fig = plt.figure(figsize=(8, 4))
    fig.patch.set_facecolor('#0f172a')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#020617')
    
    ax.plot(steps, energy, color='#10b981', linewidth=2, label='Potential Energy')
    ax.scatter(steps, energy, color='#38bdf8', s=10, alpha=0.5)
    
    ax.set_title('Autonomous Minimization Convergence', color='white', pad=15)
    ax.set_xlabel('Minimization Steps', color='#94a3b8')
    ax.set_ylabel('Energy (kJ/mol)', color='#94a3b8')
    ax.tick_params(colors='#94a3b8')
    
    ax.grid(True, color='#334155', linestyle='--', alpha=0.5)
    ax.legend(facecolor='#1e293b', edgecolor='none', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    
    return True, output_path
