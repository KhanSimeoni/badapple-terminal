import sys
import time
import cv2
import os

# Hide the terminal cursor
if os.name == "nt":
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
elif os.name == "posix":
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

opts_args = sys.argv[1:]
opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]


def print_image(
    video,
    columns: int,
    rows: int,
    b_pixel: str,
    w_pixel: str,
    sen: int,
):
    """
    Prints a frame from a given video to the console in black and white.
    Every time this function is run, the next frame will be printed automatically.
    """
    success, pixles = video.read()
    linecounter = 0

    # Step size for sampling colors from the image
    col_step = len(pixles[0]) / columns
    row_step = len(pixles) / rows

    # Iterate through every "pixel" in the terminal and sample the equivelant
    # point on the image to print out either a blank or full pixel (black or white)
    for row in range(rows):
        linecounter += 1
        for column in range(columns):

            # Sample equivilant location from image
            pixel = pixles[int(row * row_step)][int(column * col_step)]

            if sum(pixel) > 256 - int(sen):
                sys.stdout.write(w_pixel)
            else:
                sys.stdout.write(b_pixel)

    # Reset the terminal cursor to the top left
    print("\033[1;1f", end="")


def play_bad_apple(b_pixel: str, w_pixel: str, fixed: bool, sensitivity: int):
    """
    Prints a video to the terminal frame by frame to play animation, specifically bad apple
    """

    terminal_columns, terminal_rows = os.get_terminal_size()
    video = cv2.VideoCapture("badApple.m4v")

    # Print out each frame to the terminal
    for img in range(1, 6570):
        start = time.time()

        # Update image size unless image size is fixed
        if not fixed:
            terminal_columns, terminal_rows = os.get_terminal_size()
        print_image(
            video,
            terminal_columns,
            terminal_rows,
            b_pixel,
            w_pixel,
            sensitivity,
        )
        end = time.time()

        # Wait to keep 30fps. Subtract time taken to render image to prevent slowdown
        try:
            time.sleep(0.033 - (end - start))
        except:
            pass


black_pixel = " "
white_pixel = "█"
sensitivity = 128
fixed_screen = False

help_message = """usage:
    badapple
    badapple <options> [arguments]
    
Options:
    -h --help                          Shows this information
    -v --version                       Shows the current package version
    -f --fixed                         Sets the display to be set to a fixed size
    -w --white         [character]     Set which character to use for white pixles
    -b --black         [character]     set which character to use for black pixles
    -s --sensitivity   [int]           Sets how sensitive to gray pixles the program is, between 0 and 256
"""

version_message = """
⠀⠀⠀⠀⠀⠀⠀⠀⢀⢶⡆⣠⣤⣤⣀                badapple version 1.0   
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣧⣈⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀      5/24/2022
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⢛⣿⣿⣿⣿⠷⠆⠀⠀⠀⠀⠀⠀⠀      created by Khan Simeoni
   ⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣥⣴⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⢠⠞⣸⣿⣿⣿⣟⣓⣶⣒⣠⣤⣤⣄⡀⠀
⠀⠙⠛⠿⠻⠿⣿⣿⠶⠶⠿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡤
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⡿⣿⠀⠉⠙⠛⠛⠿⡿⡿⠟⠃
"""

error = False
if len(args) > 0 or len(opts) > 0:
    if "--help" in opts or "-h" in opts:
        print(help_message)

        error = True
    elif "--version" in opts or "-v" in opts:
        print(version_message)
        error = True

    if "-w" in opts or "--white" in opts:
        try:
            opt_arg = opts_args[opts_args.index("-w") + 1]
            white_pixel = opt_arg
        except:
            try:
                opt_arg = opts_args[opts_args.index("--white") + 1]
                white_pixel = opt_arg
            except:
                print("ERROR: Argument expected after -w or --white")
                error = True

    if "-b" in opts or "--black" in opts:
        try:
            opt_arg = opts_args[opts_args.index("-b") + 1]
            black_pixel = opt_arg
        except:
            try:
                opt_arg = opts_args[opts_args.index("--black") + 1]
                black_pixel = opt_arg
            except:
                print("ERROR: Argument expected after -b or --black")
                error = True

    if "-s" in opts or "--sensitivity" in opts:
        try:
            opt_arg = opts_args[opts_args.index("-s") + 1]
            sensitivity = opt_arg
        except:
            try:
                opt_arg = opts_args[opts_args.index("--sensitivity") + 1]
                sensitivity = opt_arg
            except:
                print("ERROR: Argument expected after -s or --sensitivity")
                error = True

    if "-f" in opts or "--fixed" in opts:
        fixed_screen = True

    if not error:
        play_bad_apple(black_pixel, white_pixel, fixed_screen, sensitivity)


else:
    play_bad_apple(black_pixel, white_pixel, fixed_screen, sensitivity)
