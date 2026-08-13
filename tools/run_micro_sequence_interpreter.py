#!/usr/bin/env python3
from pathlib import Path
import runpy

CURRENT = Path(__file__).resolve().with_name('run_micro_sequence_interpreter_v1_2.py')
runpy.run_path(str(CURRENT), run_name='__main__')
