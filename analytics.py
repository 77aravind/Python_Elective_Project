from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsPlotter:
    """
    Handles Matplotlib graph creation for password strength comparison using OO API.
    """
    def __init__(self, master_frame):
        self.master_frame = master_frame
        # Use Figure directly (OO API) for better stability in GUI apps
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.ax.set_facecolor('#ffffff')
        self.fig.patch.set_facecolor('#f8f9fa')

    def update_graph(self, platforms, scores):
        """
        Updates the bar chart with new data and larger fonts.
        """
        self.ax.clear()
        
        if not platforms:
            self.ax.text(0.5, 0.5, 'No data available', 
                        horizontalalignment='center', verticalalignment='center',
                        fontsize=13)
        else:
            # Classic colors for bars (Red for weak, Yellow for medium, Green for strong)
            colors = ['#c62828' if s < 2 else '#2e7d32' if s >= 4 else '#fbc02d' for s in scores]
            
            x_indices = range(len(platforms))
            self.ax.bar(x_indices, scores, color=colors, alpha=0.85, edgecolor='#1565c0')
            
            # Formatting with larger fonts
            self.ax.set_xticks(x_indices)
            self.ax.set_xticklabels(platforms, rotation=25, ha='right', fontsize=10)
            self.ax.set_ylabel('Strength Score (0-4)', fontsize=11, fontweight='bold')
            self.ax.set_title('Password Strength Comparison', fontsize=15, fontweight='bold', pad=20)
            self.ax.set_ylim(0, 5)
            self.ax.grid(axis='y', linestyle='--', alpha=0.7)

        self.fig.tight_layout()
        self.canvas.draw()
