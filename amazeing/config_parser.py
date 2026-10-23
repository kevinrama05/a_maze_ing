from typing import Union, Any, TypedDict
from sys import exit


class ConfigurationDictionary(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


class ConfigParser:
    """
    The use of this class is to read the configration files and
    validate if all the requirement keys are present and validates
    if the values given to the keys won't crash the program (negative
    number, out-of-bound coordinates, etc)

    Attributes:
        None
    """

    def check_keys(self, configs: dict[str, str]) -> None:
        """
        This method gets the configuration keys, and checks if
        the required keys are all present in the configuration
        dictionary. If not, the program ends and it prits the
        required keys which are missing

        Args:
            configs (dict[str, str]): The dictionary which holds
                                      all the configuration keys
                                      and it's value

        Returns:
            None
        """
        required_keys = [
            "HEIGHT", "WIDTH", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
        ]
        available_keys = [key for key in configs]
        for key in available_keys:
            try:
                required_keys.remove(key)
            except Exception:
                pass

        if required_keys != []:
            print("Missing required keys: ", end="")

            for i in range(0, len(required_keys) - 1):
                print(f"{required_keys[i]}, ", end="")

            exit(f"{required_keys[-1]}")

    def load_config(self, path: str) -> dict[str, str]:
        """
        Reads the configuration keys from the path, and saves
        them as dictionary. It converts them as below;
        KEY=VALUE -> config['KEY'] = 'VALUE'

        Args:
            path (str): The path of the file with the configuration keys

        Returns:
            dict[str, str]: The configuration dictionary (not valudated)
        """
        config: dict[str, str] = {}

        with open(path, "r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
        self.check_keys(config)
        return config

    def parse_value(
        self, key: str, value: str
    ) -> Union[int, float, bool, str, tuple[int, int], None]:
        """
        Casts the values from the configuration key to the
        necessary type and returns the casted value

        Args:
            key (str): The configuration key
            value (str): The configuration value

        Returns:
            Union[int, float, bool, str, tuple[int, int]]: The configuration
                                                           value after is been
                                                           casted

        """
        if key in ["HEIGHT", "WIDTH"]:
            try:
                return int(value)
            except ValueError:
                exit(f"ERROR: {key} must be an integer(ex. 12)")
        elif key in ["ENTRY", "EXIT"]:
            try:
                x, y = value.split(",", 1)
                return (int(x.rstrip()), int(y.rstrip()))
            except Exception:
                exit(
                    f"ERROR: {key}'s coordinates should"
                    "be whole numbers(ex. 13,15)"
                )
        elif key == "OUTPUT_FILE":
            return value
        elif key == "PERFECT":
            try:
                return bool(value)
            except ValueError:
                exit(f"ERROR: {key} should be True or False")
        elif key == "SEED":
            try:
                return int(value)
            except ValueError:
                exit(f"ERROR: {key} can only be an integer")
        else:
            return None

    def validate_config(self, data: dict[str, Any]) -> None:
        """
        The purpose of this module is to validate all the values, so
        the values won't crash the program, or having undefined behaviour

        Args:
            data (dict[str, Any] :
                The configuration dictonary with all
                the keys and values with the casted values

        Return:
            None
        """

        if data["HEIGHT"] <= 0:
            exit("ERROR: HEIGHT cannot be a negative number")

        elif data["WIDTH"] <= 0:
            exit("ERROR: WIDTH cannot be a negative number")

        if data["HEIGHT"] > 150:
            exit("ERROR: HEIGHT cannot be greater than 150")

        elif data["WIDTH"] > 150:
            exit("ERROR: WIDTH cannot be greater than 150")

        entry_x, entry_y = data["ENTRY"]
        if (
            not (0 <= entry_x < data["HEIGHT"]
                 and 0 <= entry_y < data["WIDTH"])
        ):
            exit("ERROR: ENTRY is out of bounds")

        exit_x, exit_y = data["EXIT"]
        if not (0 <= exit_x < data["HEIGHT"] and 0 <= exit_y < data["WIDTH"]):
            exit("ERROR: EXIT is out of bounds")

    def get_config(self, path: str) -> ConfigurationDictionary:
        """
        This conbines all the methods above, and returns
        the finalized configuration with the proper type for each value

        Args:
            path (str): The configuration path

        Returns:
            ConfigurationDictionary: The dictionary with the correctly
                                     casted values
        """
        raw = self.load_config(path)

        parsed: dict[str, Any] = {}
        for key, value in raw.items():
            parsed[key] = self.parse_value(key, value)

        self.validate_config(parsed)
        if "SEED" not in parsed:
            parsed["SEED"] = 42

        return ConfigurationDictionary(
            HEIGHT=parsed["HEIGHT"],
            WIDTH=parsed["WIDTH"],
            ENTRY=parsed["ENTRY"],
            EXIT=parsed["EXIT"],
            OUTPUT_FILE=parsed["OUTPUT_FILE"],
            PERFECT=parsed["PERFECT"],
            SEED=parsed["SEED"],
        )
