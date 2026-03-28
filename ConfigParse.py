from sys import exit


class ConfigParse:
    """
    The whole purpose of this class is to parse the keys and
    values on the configuration file(config.txt by default)
    and checks if the required keys(which are on the required keys list)
    are in the configuration file, and the value is in the right type
    """
    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']

    def __init__(self, file: str = 'config.txt'):
        self.file = file
        self.config = {}

    def read_config_file(self) -> list[str]:
        """
        Gets all the lines in the configuration file
        """
        try:
            with open(self.file, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: {self.file} file does not exists")
        return lines
    
    def get_keys(self) -> dict:
        """
        Removes comments and creates the dictionary with keys
        
        Example:
        WIDTH=20 -> config['WIDTH']: 20
        """
        key_value_lines = list(
            filter(
                lambda l: l.startswith('#') is False, self.read_config_file()
            )
        )
        not_parsed_config = {}
        for i in key_value_lines:
            key, value = i.strip().split('=', 1)
            not_parsed_config[key.strip] = value.strip()

        if not all(k in not_parsed_config for k in self.required_keys):
            raise ValueError("Missing required keys in config file")
        return not_parsed_config
    
    def parse_keys(self) -> None:
        """
        Gets the dictionary from get_keys() method and
        convertsall the values to the corresponding type.
        If an error is caught, is handled.

        HEIGHT, WIDTH -> int type
        ENTRY, EXIT -> set(int, int) type
        OUTPUT_FILE -> str typr
        PERFECT -> bool type
        SET(OPTIONAL) -> float type(default to 42)
        """
        configs = self.get_keys()
        try:
            configs['WIDTH'] = int(configs['WIDTH'])
        except ValueError:
            raise ValueError("WIDTH should be a number(e.g. 15)")
        try:
            configs['HEIGHT'] = int(configs['HEIGHT'])
        except ValueError:
            raise ValueError("HEIGHT should be a number(e.g. 15)")
        try:
            x, y = configs['ENTRY'].split(',', 1)
            configs['ENTRY'] = (int(x), int(y))
        except ValueError:
            raise ValueError(
                "ENTRY should be two numbers separated by a comma(e.g. 0,0)")
        try:
            x, y = configs['EXIT'].split(',', 1)
            configs['EXIT'] = (int(x), int(y))
        except ValueError:
            raise ValueError(
                "EXIT should be two numbers separated by a comma(e.g. 0,0)")
        try:
            configs['PERFECT'] = bool(configs['PERFECT'])
        except ValueError:
            raise ValueError("PERFECT can only be True or False")
        if 'SEED' in configs:
            try:
                configs['SEED'] = float(configs['SEED'])
            except ValueError:
                raise ValueError("SEED can only be a number")
        else:
            configs['SEED'] = 42
        self.config = configs

if __name__ == "__main__":
    configs = ConfigParse()
    try:
        configs.read_config_file()
    except FileNotFoundError as e:
        exit(e)
    try:
        configs.get_keys()
    except ValueError as e:
        exit(e)
    try:
        config.parse_keys()
    except ValueError as e:
        exit(e)

    d = configs.config
    for i, j in d.items():
        print(f"KEY: {i} <-> VALUE: {j}")

