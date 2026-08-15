"""Main entry point for WBAN Node Research application."""
import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from ui.main_window import MainWindow
from config import config
from loguru import logger as loguru_logger

# Setup logging
def setup_logging():
    """Configure logging for the application."""
    log_dir = Path(config.logging.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "wban_research.log"
    
    # Configure loguru
    loguru_logger.remove()  # Remove default handler
    loguru_logger.add(
        str(log_file),
        rotation="500 MB",
        retention="7 days",
        level=config.logging.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )
    
    if config.logging.enable_console_logging:
        loguru_logger.add(
            sys.stdout,
            level=config.logging.log_level,
            format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        )
    
    # Setup Python logging to use loguru
    logging.basicConfig(
        handlers=[logging.StreamHandler(sys.stdout)],
        level=getattr(logging, config.logging.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def main():
    """Main application entry point."""
    # Setup logging
    setup_logging()
    loguru_logger.info("Starting WBAN Node Research Application")
    
    # Create PyQt6 application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("WBAN Node Research")
    app.setApplicationVersion("0.1.0")
    app.setStyle("Fusion")
    
    try:
        # Create and show main window
        window = MainWindow()
        window.show()
        
        loguru_logger.info("Main window displayed")
        
        # Run application
        exit_code = app.exec()
        loguru_logger.info(f"Application closed with exit code: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        loguru_logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
