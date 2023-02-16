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
                        log.write(f"\n[-] failed to saved report for {filename}\n")
