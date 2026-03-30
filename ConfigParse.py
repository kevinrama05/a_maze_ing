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
            exit(f"[ERROR]: {self.file} file does not exists")
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
            not_parsed_config[key.strip()] = value.strip()

        for i in self.required_keys:
            if i not in not_parsed_config:
                exit("[ERROR]: Error: Required keys are missing")
        return not_parsed_config
    
    def parse_keys(self) -> dict:
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
            exit("[ERROR]: WIDTH should be a number(e.g. 15)")
        try:
            configs['HEIGHT'] = int(configs['HEIGHT'])
        except ValueError:
            exit("[ERROR]: HEIGHT should be a number(e.g. 15)")
        try:
            x, y = configs['ENTRY'].split(',', 1)
            configs['ENTRY'] = (int(x), int(y))
        except ValueError:
            exit(
                "[ERROR]: ENTRY should be two numbers separated by a comma(e.g. 0,0)")
        try:
            x, y = configs['EXIT'].split(',', 1)
            configs['EXIT'] = (int(x), int(y))
        except ValueError:
            exit(
                "[ERROR]: EXIT should be two numbers separated by a comma(e.g. 0,0)")
        try:
            configs['PERFECT'] = bool(configs['PERFECT'])
        except ValueError:
            exit("[ERROR]: PERFECT can only be True or False")
        if 'SEED' in configs:
            try:
                configs['SEED'] = float(configs['SEED'])
            except ValueError:
                exit("[ERROR]: SEED can only be a number")
        else:
            configs['SEED'] = 42
        return configs

    def validate_values(self) -> None:
        """
        Validates all the keys, so that it won't break
        the maze in the building process.

        Rules:
        ENTRY cannot be the same as EXIT
        HEIGHT or WIDTH cannot be less than 2
        ENTRY or EXIT cannot be in an invalid location (e.g 5,5 in a 2x2)
        """
        configs = self.parse_keys()
        if configs['ENTRY'] == configs['EXIT']:
            exit(
                "[ERROR]: ENTRY cannot be in teh same location as EXIT"
            )
        elif configs['HEIGHT'] < 2:
            exit(
                "[ERROR]: HEIGHT cannot be less than 2"
            )
        elif configs['WIDTH'] < 2:
            exit("[ERROR]: WIDTH cannot be less than 2")
        elif (configs['ENTRY'][0] < 0 or configs['ENTRY'][0] > configs['HEIGHT'] - 1) or (configs['ENTRY'][1] < 0 or configs['ENTRY'][1] > configs['WIDTH'] - 1):
            exit("[ERROR]: ENTRY cannot be outside of the maze")
        elif (configs['EXIT'][0] < 0 or configs['EXIT'][0] > configs['HEIGHT'] - 1) or (configs['EXIT'][1] < 0 or configs['EXIT'][1] > configs['WIDTH'] - 1):
            exit("[ERROR]: EXIT cannot be outside of the maze")
        self.config = configs
        
if __name__ == "__main__":
    configs = ConfigParse()
    configs.read_config_file()
    configs.get_keys()
    configs.parse_keys()
    configs.validate_values()
    d = configs.config
    for i, j in d.items():
        print(f"KEY: {i} <-> VALUE: {j}")

