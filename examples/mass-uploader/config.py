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

import json, os

class Config:
    valid_config = False
    cfg_obj = {}

    def __init__(self, cwd: str) -> None:
        with open(os.path.join(cwd, "config.json"), encoding='utf-8') as json_cfg:
            try:
                self.cfg_obj = json.load(json_cfg)
                self.valid_config = self.__validate_config()

                if self.valid_config: 
                    print("[+] config loaded")
                else: 
                    print("[-] invalid config")

            except Exception as ex:
                print(f"[!] exception: {ex}")

    def __validate_config(self) -> bool:
        return all([
            "token" in self.cfg_obj,
            "task_params" in self.cfg_obj
        ])

    def get_token(self) -> str:
        if self.valid_config:
            return self.cfg_obj["token"]
        
    def get_task_params(self) -> dict:
        if self.valid_config:
            return self.cfg_obj["task_params"]

    def get_obj(self) -> dict:
        if self.valid_config:
            return self.cfg_obj
