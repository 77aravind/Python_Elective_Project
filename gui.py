import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from generator import PasswordGenerator
from analyzer import PasswordAnalyzer
from dashboard import DashboardManager
from analytics import AnalyticsPlotter
import pyqrcode
import io
from PIL import Image

# Set appearances
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GradientFrame(ctk.CTkFrame):
    def __init__(self, master, color1="#2e1065", color2="#020617", **kwargs):
        super().__init__(master, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.canvas.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        
        r1, g1, b1 = self.winfo_rgb(self.color1)
        r2, g2, b2 = self.winfo_rgb(self.color2)
        
        for i in range(height):
            r = int(r1 + (r2 - r1) * i / height) // 256
            g = int(g1 + (g2 - g1) * i / height) // 256
            b = int(b1 + (b2 - b1) * i / height) // 256
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        self.canvas.tag_lower("gradient")

class SplashScreen:
    def __init__(self, root, duration=3000):
        self.root = root
        self.root.overrideredirect(True)
        self.duration = duration
        
        self.width, self.height = 900, 750
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.deiconify()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, highlightthickness=0, bg="#020617")
        self.canvas.pack(fill="both", expand=True)

        # Gradient: Deep Purple Midnight
        self._create_premium_background("#4c1d95", "#2e1065", "#020617")
        
        for i in range(0, self.width + self.height, 40):
            self.canvas.create_line(i, 0, i - 400, self.height, fill="#1e1b4b", width=1)

        self.canvas.create_text(self.width//2 + 4, self.height//2 + 4, text="SECUREPASS PRO", 
                                font=('Helvetica', 48, 'bold'), fill="#000000")
        self.canvas.create_text(self.width//2, self.height//2, text="SECUREPASS PRO", 
                                font=('Helvetica', 48, 'bold'), fill="#f5f3ff")
        
        self.canvas.create_text(self.width//2, self.height//2 + 80, 
                                text="Enterprise-Grade Password Security", 
                                font=('Helvetica', 16, 'bold'), fill="#a78bfa")
        
        self.canvas.create_text(self.width//2, self.height - 50, 
                                text="Initializing Secure Environment...", 
                                font=('Helvetica', 10), fill="#94a3b8")

    def _create_premium_background(self, color1, color2, color3):
        self._draw_gradient(0, self.height // 2, color1, color2)
        self._draw_gradient(self.height // 2, self.height, color2, color3)

    def _draw_gradient(self, start_y, end_y, color1, color2):
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)
        h = end_y - start_y
        for i in range(h):
            y = start_y + i
            r = int(r1 + (r2 - r1) * i / h) // 256
            g = int(g1 + (g2 - g1) * i / h) // 256
            b = int(b1 + (b2 - b1) * i / h) // 256
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, y, self.width, y, fill=color)

class SecurePassProGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SecurePass Pro")
        self.root.geometry("1000x800")
        self.root.configure(bg="#020617")
        
        # Managers
        self.analyzer = PasswordAnalyzer()
        self.generator = PasswordGenerator(analyzer=self.analyzer)
        self.dashboard = DashboardManager()

        self._create_widgets()

    def _create_widgets(self):
        # Global Background - SOLID DARK BASE
        self.main_bg = ctk.CTkFrame(self.root, fg_color="#020617")
        self.main_bg.place(x=0, y=0, relwidth=1, relheight=1)

        # Content Container
        self.content = ctk.CTkFrame(self.main_bg, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

        # Professional Header Frame
        self.header_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(0, 20))

        self.header_title = ctk.CTkLabel(self.header_frame, text="SECUREPASS PRO", 
                                         font=ctk.CTkFont(family="Inter", size=32, weight="bold"), 
                                         text_color="#f5f3ff")
        self.header_title.pack()
        
        self.header_subtitle = ctk.CTkLabel(self.header_frame, text="ADVANCED PASSWORD SECURITY SUITE", 
                                            font=ctk.CTkFont(family="Inter", size=10, weight="bold"), 
                                            text_color="#a78bfa")
        self.header_subtitle.pack()

        # Tabview - Professional Deep Purple
        self.tabview = ctk.CTkTabview(self.content, width=950, height=650, 
                                      fg_color="#0f172a", 
                                      segmented_button_selected_color="#7c3aed", 
                                      segmented_button_unselected_color="#1e1b4b", 
                                      border_width=1, border_color="#1e1b4b",
                                      bg_color="#020617")
        self.tabview.pack(fill="both", expand=True)

        tabs = ["Generate", "Test", "Dashboard", "Analytics", "History"]
        for t in tabs:
            self.tabview.add(t)

        self._setup_generate_tab()
        self._setup_test_tab()
        self._setup_dashboard_tab()
        self._setup_analytics_tab()
        self._setup_history_tab()

    def _setup_tab_bg(self, tab_name):
        tab = self.tabview.tab(tab_name)
        # Use a solid background for tabs to ensure perfect widget blending
        tab.configure(fg_color="#0f172a") 
        return tab

    def _setup_generate_tab(self):
        container = self._setup_tab_bg("Generate")
        
        self.label_platform = ctk.CTkLabel(container, text="Select Platform:", font=ctk.CTkFont(size=16), text_color="#f5f3ff")
        self.label_platform.pack(pady=(20, 10))

        self.platform_var = tk.StringVar(value="WiFi")
        self.platform_cb = ctk.CTkComboBox(container, values=self.generator.get_platforms(), variable=self.platform_var, width=300, border_color="#1e1b4b", button_color="#2e1065", bg_color="#0f172a")
        self.platform_cb.pack(pady=10)

        self.gen_btn = ctk.CTkButton(container, text="Generate Secure Password", command=self._generate_password, font=ctk.CTkFont(size=14, weight="bold"), fg_color="#7c3aed", hover_color="#6d28d9", border_width=1, border_color="#4c1d95", bg_color="#0f172a")
        self.gen_btn.pack(pady=20, ipady=10)

        self.pass_entry = ctk.CTkEntry(container, font=ctk.CTkFont(family="Courier", size=24, weight="bold"), width=500, height=60, justify="center", text_color="#f5f3ff", border_color="#1e1b4b", fg_color="#020617", bg_color="#0f172a")
        self.pass_entry.pack(pady=20)

        # QR and Copy Frame
        self.action_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.action_frame.pack(pady=10)

        self.copy_btn = ctk.CTkButton(self.action_frame, text="Copy to Clipboard", width=150, command=self._copy_to_clipboard, fg_color="#1e1b4b", hover_color="#2e1065", bg_color="#0f172a")
        self.copy_btn.pack(side="left", padx=10)

        self.qr_btn = ctk.CTkButton(self.action_frame, text="Show QR Code", width=150, command=self._show_qr, fg_color="#4c1d95", hover_color="#5b21b6", bg_color="#0f172a")
        self.qr_btn.pack(side="left", padx=10)

        # Stats Area
        self.stats_frame = ctk.CTkFrame(container, fg_color="#0a0a0a", border_width=2, border_color="#1e1b4b", bg_color="#0f172a")
        self.stats_frame.pack(pady=20, fill="x", padx=40)

        self.score_lbl = ctk.CTkLabel(self.stats_frame, text="Strength Score: N/A", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f5f3ff", fg_color="transparent")
        self.score_lbl.pack(pady=10)

        self.meter_canvas = tk.Canvas(self.stats_frame, height=10, bg="#1e1b4b", highlightthickness=0)
        self.meter_canvas.pack(fill="x", padx=20, pady=5)
        self.meter_rect = self.meter_canvas.create_rectangle(0, 0, 0, 10, fill="#a855f7", width=0)

        self.crack_lbl = ctk.CTkLabel(self.stats_frame, text="Crack Time: N/A", text_color="#c084fc", fg_color="transparent")
        self.crack_lbl.pack(pady=5)

    def _setup_test_tab(self):
        container = self._setup_tab_bg("Test")
        ctk.CTkLabel(container, text="Manual Password Tester", font=ctk.CTkFont(size=20, weight="bold"), text_color="#f5f3ff", bg_color="#0f172a").pack(pady=30)
        
        self.test_entry = ctk.CTkEntry(container, placeholder_text="Enter password to test...", width=400, height=40, show="*", border_color="#1e1b4b", bg_color="#0f172a")
        self.test_entry.pack(pady=20)

        ctk.CTkButton(container, text="Analyze Strength", command=self._test_password, fg_color="#7c3aed", hover_color="#6d28d9", border_color="#4c1d95", border_width=1, bg_color="#0f172a").pack(pady=10)

    def _setup_dashboard_tab(self):
        container = self._setup_tab_bg("Dashboard")
        from tkinter import ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#0a0a0a", 
                        foreground="#f5f3ff", 
                        fieldbackground="#0a0a0a", 
                        borderwidth=0,
                        font=("Inter", 14),
                        rowheight=35)
        style.configure("Treeview.Heading", 
                        background="#1e1b4b", 
                        foreground="#a78bfa", 
                        font=("Inter", 16, "bold"))
        style.map("Treeview", background=[('selected', '#5b21b6')])
        
        self.tree = ttk.Treeview(container, columns=("platform", "length", "score", "crack_time"), show="headings")
        self.tree.heading("platform", text="Platform")
        self.tree.heading("length", text="Length")
        self.tree.heading("score", text="Score")
        self.tree.heading("crack_time", text="Crack Time")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

    def _setup_analytics_tab(self):
        container = self._setup_tab_bg("Analytics")
        self.graph_frame = ctk.CTkFrame(container, fg_color="#0a0a0a")
        self.graph_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.plotter = AnalyticsPlotter(self.graph_frame)

    def _setup_history_tab(self):
        container = self._setup_tab_bg("History")
        self.history_txt = ctk.CTkTextbox(container, width=600, height=400, fg_color="#0a0a0a", text_color="#f5f3ff", border_color="#1e1b4b")
        self.history_txt.pack(padx=20, pady=20, fill="both", expand=True)

    def _generate_password(self):
        platform = self.platform_var.get()
        password = self.generator.generate(platform)
        analysis = self.analyzer.analyze(password)
        
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, password)
        
        score = analysis['score']
        colors = ["#f87171", "#fb923c", "#facc15", "#4ade80", "#22c55e"]
        color = colors[score]
        
        self.score_lbl.configure(text=f"Strength Score: {score}/4", text_color=color)
        
        # Update Meter
        canvas_w = self.meter_canvas.winfo_width()
        if canvas_w < 10: canvas_w = 800
        target_w = (score / 4) * canvas_w
        self.meter_canvas.coords(self.meter_rect, 0, 0, target_w, 10)
        self.meter_canvas.itemconfig(self.meter_rect, fill=color)

        self.crack_lbl.configure(text=f"Estimated Crack Time: {analysis['crack_time']}")

        # Save to history & dashboard
        entry = {'platform': platform, 'password': password, 'length': len(password), 'score': score, 'crack_time': analysis['crack_time']}
        self.dashboard.add_entry(entry)
        self._refresh_data()

    def _test_password(self):
        pwd = self.test_entry.get()
        if not pwd: return
        analysis = self.analyzer.analyze(pwd)
        messagebox.showinfo("Analysis", f"Score: {analysis['score']}/4\nCrack Time: {analysis['crack_time']}\nFeedback: {analysis['feedback']}")

    def _copy_to_clipboard(self):
        pwd = self.pass_entry.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Success", "Password copied to clipboard!")

    def _show_qr(self):
        pwd = self.pass_entry.get()
        if not pwd: return
        
        qr_window = ctk.CTkToplevel(self.root)
        qr_window.title("QR Code")
        qr_window.geometry("300x350")
        qr_window.attributes("-topmost", True)

        qr = pyqrcode.create(pwd)
        buffer = io.BytesIO()
        qr.png(buffer, scale=6)
        
        img = Image.open(buffer)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
        
        label = ctk.CTkLabel(qr_window, image=ctk_img, text="")
        label.pack(pady=20)
        ctk.CTkLabel(qr_window, text="Scan to copy password").pack()

    def _refresh_data(self):
        # Update Treeview
        for item in self.tree.get_children(): self.tree.delete(item)
        for data in self.dashboard.get_dashboard_data():
            self.tree.insert("", tk.END, values=(data['platform'], data['length'], data['score'], data['crack_time']))
            
        # Update History
        self.history_txt.delete("1.0", tk.END)
        for i, entry in enumerate(self.dashboard.get_history(), 1):
            self.history_txt.insert(tk.END, f"{i}. {entry['platform']} -> {entry['password']} [Score: {entry['score']}]\n\n")

        # Update Analytics
        platforms, scores = self.dashboard.get_latest_analytics_data()
        self.plotter.update_graph(platforms, scores)
