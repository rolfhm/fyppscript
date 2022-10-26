from argparse import ArgumentParser
from pathlib import Path
import fypp

def input_parser():
    """
    Use argparse to parse command line arguments
    """
    parser = ArgumentParser()

    parser.add_argument(
        "src_dir",
        help = "directory to search for fypp files",
        nargs = 1,
        type = str,
        metavar = 'src dir',
    )

    parser.add_argument(
        "-m",
        "--modules",
        help = "modules needed by fypp to process any files",
        nargs = "*",
        type = str,
        default = [],
    )

    parser.add_argument(
        "-M",
        "--module-directories",
        help = "directories to search for modules",
        nargs = "*",
        type = str,
        default = [],
    )

    args = parser.parse_args()
    return args


def process_dir(directory, modules, module_directories=None):
    """
    Find all fypp files in directory and its subdirectories
    and process them with Fypp.
    """

    #Create Path object from directory
    fyppdir = Path(directory).resolve()

    #Generate FyppOptions based on input
    options = fypp.FyppOptions()
    options.modules = modules
    options.moduledirs = module_directories

    #Generate fypp tool
    tool = fypp.Fypp(options)

    #Loop over all fypp files in directory and its subdirectories
    for fyppfile in fyppdir.rglob('*.fypp'):

        #Generate a Path to a .F90 file in the same directory
        fortranfile = fyppfile.with_suffix('.F90')

        #Process the fyppfile and write to fortranfile
        tool.process_file(str(fyppfile), str(fortranfile))


def main():
    """
    Read input directory from command line and call fypp script
    """

    args = input_parser()

    process_dir(args.src_dir[0], args.modules, args.module_directories)

if __name__ == "__main__":
    main()
