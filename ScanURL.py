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

# AnyRun API documentation:
# https://any.run/api-documentation/

import sys, os, requests, json

def scan_url(url: str) -> str:
    return requests.post( \
        "https://api.any.run/v1/analysis",
        headers = {
            "Authorization": f"API-Key {os.environ['API_KEY']}"
        },
        data = {
            "env_os": "windows",
            "env_bitness": "64",
            "env_version": "10",
            "env_type": "complete",
            "opt_privacy_type": "bylink",
            "opt_timeout": 120,

            # URL scan options
            "obj_type": "url",
            "obj_ext_browser": "Google Chrome",
            "obj_url": url
        }
    ).text

def process_response(response):
    json_data = json.loads(response)

    if json_data.get('error', False):
        error_message = json_data.get('message', 'Unknown error')
        print(f'Error: {error_message}')
    else:
        task_id = json_data['data']['taskid']
        url = f'https://app.any.run/tasks/{task_id}'
        print(f'URL: {url}')

def main() -> None:
    if len(sys.argv) < 2:
        print ("[!] Usage example: python ScanURL.py https://www.microsoft.com")
        return

    url = sys.argv[1]
    process_response(scan_url(url))

if __name__ == "__main__":
    main()
