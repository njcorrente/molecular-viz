import os
import sys
import matplotlib

# Configure matplotlib
matplotlib.use('TkAgg')
os.environ['MATPLOTLIBDATA'] = matplotlib._get_data_path()

# Fix macOS-specific issues
if getattr(sys, 'frozen', False):
    os.environ["TCL_LIBRARY"] = os.path.join(sys._MEIPASS, "tcl")
    os.environ["TK_LIBRARY"] = os.path.join(sys._MEIPASS, "tk")
