# Allow direct execution
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import radiko_recorder

if __name__ == '__main__':
    radiko_recorder.main(['-a', 'JP10', '-s'])