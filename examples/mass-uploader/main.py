# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
