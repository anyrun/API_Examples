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

import sys, os, requests

# Upload, unpack and run each file
def UploadUnpackAndRun(filename):
    with open(filename, 'rb') as f:
        return requests.post( \
            "https://api.any.run/v1/analysis",
            files = {
                'file': f.read()
            },
            headers = {
                "Authorization": f"API-Key {os.environ['API_KEY']}"
            },
            data = {
                "env_os": "windows",
                "env_bitness": "64",
                "env_version": "10",
                "env_type": "complete",
                "opt_privacy_type": "bylink",
                "obj_ext_startfolder": "desktop",

                # all the magic happens here
                "obj_ext_cmd": r"""powershell -c "Move-Item -Path %FILENAME% .\f.zip; mkdir C:\Users\admin\Desktop\f; &'C:\Program Files\WinRAR\WinRAR.exe' -p1234 x -ibck .\f.zip *.* .\f | Wait-Job; $files = Get-ChildItem -Recurse -Path "f"; foreach ($file in $files){&$file.FullName};"""
            }
        ).text

def main() -> None:
    if len(sys.argv) < 2:
        print ("[!] Usage example: python UploadUnpackAndRun.py filename.zip")
        return

    filename = sys.argv[1]
    result = UploadUnpackAndRun(filename)

    print(f"[+] Request result: {result}")

if __name__ == "__main__":
    main()
