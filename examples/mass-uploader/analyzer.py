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

import os

from anyrun import AnyRunClient
from config import Config

class SamplesAnalyzer:
    def __init__(self, cwd: str, config: Config) -> None:
        self.cwd = cwd
        self.anyrun_client = AnyRunClient(config)

    def analyze_all(self) -> bool:
        samples_path = os.path.join(self.cwd, "samples")
        with open("result.log", 'w') as log:
            log.write("[>] starting test\n")
            for filename in os.listdir(samples_path):
                file = os.path.join(samples_path, filename)
                if os.path.isfile(file):
                    print(f"[>] analyzing {filename}..")
                    if self.anyrun_client.perform_analysis(file) == True:
                        log.write(
                            f"\n[+] saved report as {filename}.json"
                            f"\ntask link: https://app.any.run/tasks/{self.anyrun_client.get_last_task_uuid()}\n"
                        )
                    else:
                        log.write(f"\n[-] failed to save report for {filename}\n")
