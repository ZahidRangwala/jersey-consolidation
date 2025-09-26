"""
Main application entry point for the New Jersey Municipal Consolidation Analysis.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.core.logging_config import setup_logging
from src.dashboard.main_dashboard import create_dashboard
from src.dashboard.improved_dashboard import create_improved_dashboard


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="New Jersey Municipal Consolidation Analysis Dashboard"
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8051,
        help='Port to run the dashboard on (default: 8051)'
    )
    parser.add_argument(
        '--dashboard',
        choices=['main', 'improved'],
        default='main',
        help='Dashboard type to run (default: main)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Starting {args.dashboard} dashboard on port {args.port}")
        
        # Create appropriate dashboard
        if args.dashboard == 'main':
            dashboard = create_dashboard(port=args.port)
        elif args.dashboard == 'improved':
            dashboard = create_improved_dashboard(port=args.port)
        
        # Run dashboard
        dashboard.run(debug=args.debug)
        
    except KeyboardInterrupt:
        logger.info("Dashboard stopped by user")
    except Exception as e:
        logger.error(f"Error running dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()