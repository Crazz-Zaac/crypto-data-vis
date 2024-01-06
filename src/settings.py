import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go two levels up from src to get the project root

# Add the project root directory to the system path
sys.path.append(ROOT_DIR)

DATASET_DIR = os.path.join(ROOT_DIR, 'data')
SRC_DIR = os.path.join(ROOT_DIR, 'src')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

# print(DATASET_DIR, SRC_DIR)