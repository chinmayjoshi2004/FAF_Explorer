# ANSI color codes
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.RESET} {message}")


def print_error(message):
    print(f"{Colors.RED}✗{Colors.RESET} {message}")


def print_warning(message):
    print(f"{Colors.YELLOW}!{Colors.RESET} {message}")


def print_info(message):
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {message}")
