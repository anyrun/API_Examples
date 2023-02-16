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

import requests, json, time, os

from config import Config
from enum import IntEnum

class EResponseCode(IntEnum):
    OK = 200,
    TASK_FAILED = 422,
    LIMITS_EXCEEDED = 429

class AnyRunClient:
    REPORT_CHECK_DELAY = 10

    def __init__(self, config: Config) -> None:
        self.cfg_obj = config.get_obj()
        self.token = config.get_token()

    def __validate_api_response(self, response):
        if response.status_code == EResponseCode.LIMITS_EXCEEDED: # another task running?
            if len(response.text) != 0:
                api_resp = json.loads(response.text)
                if "message" in api_resp:
                    if api_resp["message"] == "Limits exceeded":
                        print(
                            "[!] seems like there's another task "
                            "which already running (kill it) "
                            "or limits might be exceeded"
                        )
            return None

        if response.status_code == EResponseCode.TASK_FAILED: # task failed?
            if len(response.text) != 0:
                api_resp = json.loads(response.text)
                if "message" in api_resp:
                    if api_resp["message"] == "No content":
                        print(
                            "[!] error occuried while task "
                            "was running, no report available"
                        )
                        return {'no_data': 'true'}

        if response.status_code == EResponseCode.OK: # everything's fine
            if len(response.text) != 0:
                api_resp = json.loads(response.text)
                if "error" in api_resp:
                    if api_resp["error"] == False:
                        return api_resp

            return None

    def __get_report(self, task_uuid: str):
        api_req = requests.get(
            f"https://api.any.run/v1/analysis/{task_uuid}",
            headers={"Authorization": f"API-Key {self.token}"},
        )

        api_resp = self.__validate_api_response(api_req)

        if api_resp == None: 
            return None

        if "data" in api_resp:
            if "status" in api_resp["data"]:
                if api_resp["data"]["status"] == "done": 
                    return api_resp                
                else:
                    return None
        
        if "no_data" in api_resp:
            return api_resp

    def get_last_task_uuid(self) -> str:
        return self.last_task_uuid

    def perform_analysis(self, file_path) -> bool:
        self.last_task_uuid = 0

        with open(file_path, 'rb') as file:
            api_req = requests.post(
                f"https://api.any.run/v1/analysis", 
                files={'file': file.read()}, 
                headers={"Authorization": f"API-Key {self.token}"},
                data=self.cfg_obj["task_params"]
            )

            api_resp = self.__validate_api_response(api_req)
            
            if api_resp == None:
                print(f"[-] failed to create a task! invalid response")
                return False

            if "data" in api_resp:
                if "taskid" in api_resp["data"]:
                    self.last_task_uuid = api_resp["data"]["taskid"]

            if self.last_task_uuid == 0:
                print(f"[-] failed to create a task! api response: {api_req.text}")
                return False

            print(f"[+] created task: {self.last_task_uuid}")
            report_resp = None

            print(f"[>] waiting for report..")

            while report_resp == None:
                report_resp = self.__get_report(self.last_task_uuid)
                if report_resp != None:
                    if "no_data" in report_resp: 
                        return False
                time.sleep(self.REPORT_CHECK_DELAY)
            
            print(f"[+] task finished! saving report..")

            _, filename = os.path.split(file_path)
            with open(f"{filename}_report.json", 'w') as file:
                file.write(json.dumps(report_resp))

            return True
