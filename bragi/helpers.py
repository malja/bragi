import sys

def require_optional_arguments(required_arguments:list, parserd_arguments, parser):
    """
    Makes sure all of required arguments are provided. If not, error message is printed and
    the program is exited with exit code 1.

    :param list required_arguments: List of all required arguments. This should contain only
    arguments, which are listed as "optional" in argparse, but are necessary for code following
    the call of this function.
    :param argparse.Namespace parsed_arguments: All provided arguments parsed from command line.
    :param argparse.ArgumentParser parser: Command line argument's parser.
    """
    for arg in required_arguments:
        if not hasattr(parserd_arguments, arg):
            parser.print_usage()
            print("{} error: the following arguments are required: --video".format(sys.argv[0]))
            exit(1)

