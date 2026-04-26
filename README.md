This is a fork of the JUAMI Pytentiostat project for University of Delaware club Stem Beyond the Books. It has been slightly modified but has the same functionality as the original software.

 ## Installation

1. Clone the repository. Windows users will require a git emulator like Git Bash or thers.
2. Enter the working directory for the project
3. run `python3 -m venv/`. Windows users might have to write it like `python3 -m venv C:\path\to\Udentiostat\`
4. Activate the virtual environment. On Linux or Mac, run `source venv/bin/activate`. On Windows run `.\scripts\activate`
5. Now that the environment is active, run `pip install .` to install all the dependencies. This might take a bit so give it some time.
6. You are now ready to run the software. Yay.

## Usage

To confure an experiment, there is a file called config.yml. This file must be in the same directory as the other python files. This file is how you can set up the parameters of the experiment. To run the code, type `python3 main.py` in the src/pytentiostat directory.
