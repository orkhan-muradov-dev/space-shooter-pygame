# ==============================================================================
# A class to manage and persist the high score.
# ==============================================================================

from .settings import HIGH_SCORE_FILE

class HighScoreManager:
    def __init__(self):
        self.path = HIGH_SCORE_FILE
        self._high_score = self.load_high_score()

    def load_high_score(self) -> int:
        """
        Loads the high score from a file. If the file doesn't exist,
        it creates the file and initializes the high score to 0.
        """
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except (IOError, ValueError):
            # File not found or invalid content, return 0.
            return 0

    def save_high_score(self, score: int):
        """Saves a new high score to the file if it's greater than the current high score."""
        if score > self._high_score:
            self._high_score = score
            with open(self.path, 'w') as f:
                f.write(str(self._high_score))
            return True
        return False

    def get_high_score(self):
        """Returns the current high score."""
        return self._high_score