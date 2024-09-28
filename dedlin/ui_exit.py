import logging
import signal
import sys

LOGGER = logging.getLogger(__name__)


def confirm_exit(signum: int, frame) -> None:
    """Handle the Ctrl+C (SIGINT) or Ctrl+Break (SIGBREAK) signals by prompting the user for confirmation.

    Args:
        signum (int): The signal number.
        frame: The current stack frame (required by the signal handler signature).
    """
    LOGGER.info("Received signal: %d. Prompting for exit confirmation.", signum)
    try:
        answer = input("Do you really want to exit? (y/n): ").strip().lower()
        if answer == "y":
            LOGGER.info("User confirmed exit. Exiting the program.")

            sys.exit(0)
        else:
            LOGGER.info("User declined to exit. Continuing the program.")
    except RuntimeError:
        LOGGER.info("Can't confirm exit, exiting")
        sys.exit(0)


def setup_signal_handlers() -> None:
    """Set up signal handlers for SIGINT, SIGBREAK, and SIGABRT to ask for user confirmation before exiting."""
    signal.signal(signal.SIGINT, confirm_exit)
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, confirm_exit)
    if hasattr(signal, "SIGABRT"):
        signal.signal(signal.SIGABRT, confirm_exit)
    LOGGER.info("Signal handlers set up for SIGINT, SIGBREAK, and SIGABRT.")


if __name__ == "__main__":

    def run() -> None:
        """Example."""
        logging.basicConfig(level=logging.INFO)
        setup_signal_handlers()

        LOGGER.info("Program is running. Press Ctrl+C to test the signal handler.")

        # Keep the program running indefinitely to test the signal handling.
        try:
            while True:
                input("blah")
        except KeyboardInterrupt:
            # This block will never be reached because the signal is handled in `confirm_exit`.
            LOGGER.info("KeyboardInterrupt caught. Exiting.")

    run()
