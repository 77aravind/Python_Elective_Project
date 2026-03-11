class DashboardManager:
    """
    Manages session data including password history and dashboard table entries.
    """
    def __init__(self):
        self.history = []  # List of dicts: {'password', 'platform', 'score', 'crack_time', 'entropy'}
        self.dashboard_data = [] # Full list of all generated passwords in session

    def add_entry(self, entry):
        """
        Adds a new password entry to history and dashboard.
        """
        # Add to full dashboard list
        self.dashboard_data.append(entry)
        
        # Add to history (limit to last 5)
        self.history.append(entry)
        if len(self.history) > 5:
            self.history.pop(0)

    def get_history(self):
        return self.history[::-1] # Newest first

    def get_dashboard_data(self):
        return self.dashboard_data

    def get_latest_analytics_data(self):
        """
        Returns data formatted for analytics (platform names and scores).
        """
        platforms = []
        scores = []
        for entry in self.dashboard_data:
            platforms.append(entry['platform'])
            scores.append(entry['score'])
        return platforms, scores
