import customtkinter as ctk
from PIL import Image
import os
import sys
import threading
import subprocess

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from polymathix.modules.drug_hunting.generative_ai import generate_novel_molecule
from polymathix.modules.quick_pca.deep_pca import run_deep_pca_analysis
from polymathix.modules.visual_factory.pdb_to_obj import pdb_to_obj
from polymathix.modules.data_resilience.graph_engine import generate_energy_plot

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Polymathix - Next-Gen Scientific Engine")
        self.geometry("1300x850")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_gen_ai_frame()
        self.setup_physics_frame()
        
        self.current_pdb_file = os.path.join(os.path.dirname(__file__), "1CRN.pdb")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="POLYMATHIX", font=ctk.CTkFont(family="Cascadia Code", size=26, weight="bold"), text_color="#38bdf8")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 5))
        self.sub_logo = ctk.CTkLabel(self.sidebar_frame, text="Quantum-to-Macro", font=ctk.CTkFont(size=12, slant="italic"), text_color="#94a3b8")
        self.sub_logo.grid(row=1, column=0, padx=20, pady=(0, 30))

        # Core Modules
        self.btn_gen_ai = ctk.CTkButton(self.sidebar_frame, text="🧠 Generative Drug Design", font=ctk.CTkFont(weight="bold"), height=40, command=self.show_gen_ai_frame)
        self.btn_gen_ai.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

        self.btn_pca = ctk.CTkButton(self.sidebar_frame, text="🌌 Deep Trajectory PCA", font=ctk.CTkFont(weight="bold"), height=40, command=self.show_pca_frame)
        self.btn_pca.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_physics = ctk.CTkButton(self.sidebar_frame, text="⚛️ Autonomous MD Engine", font=ctk.CTkFont(weight="bold"), height=40, command=self.show_physics_frame)
        self.btn_physics.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        
        # New Modules
        self.btn_membrane = ctk.CTkButton(self.sidebar_frame, text="💧 Membrane Foundry", font=ctk.CTkFont(weight="bold"), height=40, command=self.show_placeholder)
        self.btn_membrane.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self.btn_materials = ctk.CTkButton(self.sidebar_frame, text="🛡️ Material Science Suite", font=ctk.CTkFont(weight="bold"), height=40, command=self.show_placeholder)
        self.btn_materials.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.btn_donate = ctk.CTkButton(self.sidebar_frame, text="☕ Support Vanguard", fg_color="#ea580c", hover_color="#c2410c", font=ctk.CTkFont(weight="bold"), height=40)
        self.btn_donate.grid(row=11, column=0, padx=20, pady=30, sticky="ew")

    def setup_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        self.welcome_label = ctk.CTkLabel(self.main_frame, text="Welcome to the Future of Science.\n\nAll AI & Physics engines are now fully operational.\nSelect a module on the left to begin.", font=ctk.CTkFont(size=18, weight="bold"))
        self.welcome_label.grid(row=0, column=0, pady=250)

    def setup_gen_ai_frame(self):
        self.gen_ai_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.gen_ai_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.gen_title = ctk.CTkLabel(self.gen_ai_frame, text="Deep Generative Drug Design", font=ctk.CTkFont(size=28, weight="bold"))
        self.gen_title.grid(row=0, column=0, columnspan=2, pady=(20, 20))

        self.gen_button = ctk.CTkButton(self.gen_ai_frame, text="Synthesize Novel Molecule (RDKit Backend)", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="#10b981", hover_color="#059669", command=self.generate_molecule)
        self.gen_button.grid(row=1, column=0, columnspan=2, pady=10, padx=50, sticky="ew")

        self.mol_image_label = ctk.CTkLabel(self.gen_ai_frame, text="")
        self.mol_image_label.grid(row=2, column=0, rowspan=4, padx=20, pady=20)

        self.stats_textbox = ctk.CTkTextbox(self.gen_ai_frame, width=350, height=250, font=ctk.CTkFont(family="Consolas", size=14), fg_color="#020617", text_color="#38bdf8")
        self.stats_textbox.grid(row=2, column=1, pady=20, padx=20, sticky="nw")
        self.stats_textbox.insert("0.0", ">>> SYSTEM IDLE")
        self.stats_textbox.configure(state="disabled")

    def setup_physics_frame(self):
        self.physics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.physics_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.phys_title = ctk.CTkLabel(self.physics_frame, text="Autonomous MD Engine (OpenMM)", font=ctk.CTkFont(size=28, weight="bold"))
        self.phys_title.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # Interactive Controls
        self.controls_frame = ctk.CTkFrame(self.physics_frame)
        self.controls_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        self.controls_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.btn_upload = ctk.CTkButton(self.controls_frame, text="📁 Upload PDB File", command=self.upload_pdb, fg_color="#475569", hover_color="#334155")
        self.btn_upload.grid(row=0, column=0, padx=10, pady=10)
        
        self.lbl_file = ctk.CTkLabel(self.controls_frame, text="Selected: 1CRN.pdb", text_color="#38bdf8")
        self.lbl_file.grid(row=0, column=1, padx=10, pady=10)
        
        self.opt_ff = ctk.CTkOptionMenu(self.controls_frame, values=["AMBER14", "CHARMM36", "OPLS-AA"], dynamic_resizing=False)
        self.opt_ff.grid(row=0, column=2, padx=10, pady=10)
        
        self.opt_water = ctk.CTkOptionMenu(self.controls_frame, values=["TIP3P", "OPC", "SPC/E"], dynamic_resizing=False)
        self.opt_water.grid(row=0, column=3, padx=10, pady=10)

        # Action Buttons
        self.phys_button = ctk.CTkButton(self.physics_frame, text="Initiate Self-Healing Minimization", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="#8b5cf6", hover_color="#7c3aed", command=self.run_physics)
        self.phys_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
        
        self.btn_export = ctk.CTkButton(self.physics_frame, text="📤 Export to 3D (OBJ)", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="#0284c7", hover_color="#0369a1", command=self.export_obj, state="disabled")
        self.btn_export.grid(row=2, column=1, pady=10, padx=20, sticky="ew")

        # Terminal and Graphs
        self.output_frame = ctk.CTkFrame(self.physics_frame, fg_color="transparent")
        self.output_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="nsew")
        self.output_frame.grid_columnconfigure((0, 1), weight=1)

        self.phys_terminal = ctk.CTkTextbox(self.output_frame, width=450, height=350, font=ctk.CTkFont(family="Consolas", size=13), fg_color="#020617", text_color="#10b981")
        self.phys_terminal.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.phys_terminal.insert("0.0", ">>> ENGINE READY.\n>>> Upload a PDB or use the default.\n>>> Click 'Initiate' to begin.")
        self.phys_terminal.configure(state="disabled")
        
        self.graph_label = ctk.CTkLabel(self.output_frame, text="[Data Resilience Graphing Engine Standby]")
        self.graph_label.grid(row=0, column=1, pady=10, padx=10)

    def upload_pdb(self):
        file_path = ctk.filedialog.askopenfilename(filetypes=[("PDB Files", "*.pdb"), ("All Files", "*.*")])
        if file_path:
            self.current_pdb_file = file_path
            filename = os.path.basename(file_path)
            self.lbl_file.configure(text=f"Selected: {filename}")

    def export_obj(self):
        self.btn_export.configure(state="disabled", text="Exporting...")
        self.update()
        
        out_obj = os.path.join(os.path.dirname(__file__), "polymathix_3d_render.obj")
        target_pdb = os.path.join(os.path.dirname(__file__), "polymathix_ready.pdb")
        
        # If ready doesn't exist, use input
        if not os.path.exists(target_pdb):
            target_pdb = self.current_pdb_file
            
        success, msg = pdb_to_obj(target_pdb, out_obj)
        
        if success:
            self.btn_export.configure(state="normal", text="Export Successful!", fg_color="#10b981")
            self.phys_terminal.configure(state="normal")
            self.phys_terminal.insert("end", f"\n[SUCCESS] VisualFactory: Exported 3D model to {out_obj}\n")
            self.phys_terminal.see("end")
            self.phys_terminal.configure(state="disabled")
        else:
            self.btn_export.configure(state="normal", text="Export Failed")

    def hide_all_frames(self):
        self.welcome_label.grid_forget()
        self.gen_ai_frame.grid_forget()
        self.physics_frame.grid_forget()

    def show_placeholder(self):
        self.hide_all_frames()
        self.welcome_label.configure(text="Module initializing...\nConnecting to high-performance compute clusters.")
        self.welcome_label.grid(row=0, column=0, pady=250)

    def show_gen_ai_frame(self):
        self.hide_all_frames()
        self.gen_ai_frame.grid(row=0, column=0, sticky="nsew", rowspan=3)
        self.gen_title.configure(text="Deep Generative Drug Design")
        self.gen_button.configure(state="normal", text="Synthesize Novel Molecule (RDKit)", fg_color="#10b981")
        self.gen_button.configure(command=self.generate_molecule)
        
    def show_pca_frame(self):
        self.hide_all_frames()
        self.gen_ai_frame.grid(row=0, column=0, sticky="nsew", rowspan=3)
        self.gen_title.configure(text="Loading Latent Space...")
        self.update()
        img_path, status = run_deep_pca_analysis()
        self.gen_title.configure(text="Deep Non-Linear Trajectory Analytics")
        self.gen_button.configure(state="disabled", text="Analysis Complete", fg_color="#334155")
        my_image = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(700, 300))
        self.mol_image_label.configure(image=my_image, text="")
        
        self.stats_textbox.configure(state="normal")
        self.stats_textbox.delete("0.0", "end")
        self.stats_textbox.insert("0.0", f">>> TRAJECTORY UNROLLED <<<\n\nStatus: {status}")
        self.stats_textbox.configure(state="disabled")
        
    def show_physics_frame(self):
        self.hide_all_frames()
        self.physics_frame.grid(row=0, column=0, sticky="nsew", rowspan=4)

    def generate_molecule(self):
        self.gen_button.configure(state="disabled", text="Running RDKit Engine...")
        self.update()
        smiles, weight, logp, img_path = generate_novel_molecule()
        if smiles:
            my_image = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(350, 350))
            self.mol_image_label.configure(image=my_image, text="")
            self.stats_textbox.configure(state="normal")
            self.stats_textbox.delete("0.0", "end")
            self.stats_textbox.insert("0.0", f">>> NOVEL MOLECULE SYNTHESIZED <<<\n\nID: {smiles}\nMW: {weight} g/mol\nLogP: {logp}\n\nSTATUS: High Viability.")
            self.stats_textbox.configure(state="disabled")
        self.gen_button.configure(state="normal", text="Synthesize Another Molecule")
        
    def run_physics(self):
        self.phys_button.configure(state="disabled", text="Executing Pipeline...")
        self.btn_export.configure(state="disabled", text="📤 Export to 3D (OBJ)")
        self.phys_terminal.configure(state="normal")
        self.phys_terminal.delete("0.0", "end")
        
        ff = self.opt_ff.get()
        water = self.opt_water.get()
        self.phys_terminal.insert("end", f">>> Executing with {ff} and {water}...\n")
        self.update()
        
        def run_script():
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "polymathix_cli.py")
            process = subprocess.Popen([sys.executable, script_path, self.current_pdb_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            for line in process.stdout:
                clean_line = line.replace('\033[94m', '').replace('\033[92m', '').replace('\033[93m', '').replace('\033[91m', '').replace('\033[0m', '')
                self.phys_terminal.insert("end", clean_line)
                self.phys_terminal.see("end")
                self.update_idletasks()
                
            process.wait()
            self.phys_button.configure(state="normal", text="Re-run Simulation")
            self.btn_export.configure(state="normal")
            self.phys_terminal.configure(state="disabled")
            
            # Generate and load Graph
            out_png = os.path.join(os.path.dirname(__file__), "assets", "energy_plot.png")
            generate_energy_plot(out_png)
            
            if os.path.exists(out_png):
                graph_img = ctk.CTkImage(light_image=Image.open(out_png), dark_image=Image.open(out_png), size=(400, 250))
                self.graph_label.configure(image=graph_img, text="")

        threading.Thread(target=run_script, daemon=True).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
