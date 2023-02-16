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
        
    def get_task_params(self) -> str:
        if self.valid_config:
            return self.cfg_obj["task_params"]

    def get_obj(self) -> dict:
        if self.valid_config:
            return self.cfg_obj
