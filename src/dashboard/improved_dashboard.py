"""
Improved dashboard implementation for the New Jersey Municipal Consolidation Analysis.
This is identical to the main dashboard but runs on port 8053.
"""

import logging
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.dashboard.main_dashboard import MainNJConsolidationDashboard

logger = logging.getLogger(__name__)


class ImprovedNJConsolidationDashboard(MainNJConsolidationDashboard):
    """Improved dashboard - identical to main dashboard but on port 8053."""
    
    def __init__(self, port: int = 8053):
        super().__init__(port)
        logger.info("Improved dashboard initialized (identical to main dashboard)")


def create_improved_dashboard(port: int = 8053) -> ImprovedNJConsolidationDashboard:
    """Factory function to create an improved dashboard instance."""
    return ImprovedNJConsolidationDashboard(port)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    )
    
    # Create and run improved dashboard
    dashboard = create_improved_dashboard(port=8053)
    dashboard.run(debug=True)
