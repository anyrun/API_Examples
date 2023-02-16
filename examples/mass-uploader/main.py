# TODO: 
# - check API limits / parallels limit to create multiple tasks at once

import os

from config import Config
from analyzer import SamplesAnalyzer

def main() -> None:
    cwd = os.getcwd() # get cwd
    cfg = Config(cwd) # load config
    analyzer = SamplesAnalyzer(cwd, cfg) # initialize analyzer
    analyzer.analyze_all() # batch-process samples

if __name__ == "__main__":
    main()
