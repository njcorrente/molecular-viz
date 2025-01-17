import os
import matplotlib

# Configure matplotlib
matplotlib.use('TkAgg')
os.environ['MATPLOTLIBDATA'] = matplotlib._get_data_path()
