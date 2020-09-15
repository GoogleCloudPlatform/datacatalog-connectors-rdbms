import yaml

from .config_constants import REFRESH_OPTION


class Config:

    def __init__(self, config_path):
        self._config_path = config_path
        self._conf_content = self._read_config_file()
        self.refresh_metadata_tables = False
        self.scrape_optional_metadata = False
        self._determine_scraping_steps()

    def _read_config_file(self):
        with open(self._config_path, 'r') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf or dict()

    def _determine_scraping_steps(self):
        if self._conf_content.get(REFRESH_OPTION) is not None:
            self.refresh_metadata_tables = self._conf_content[REFRESH_OPTION]
        options = self.get_chosen_metadata_options()
        if len(options):
            self.scrape_optional_metadata = True

    def get_chosen_metadata_options(self):
        '''
        From the config contents, retrieve options that user has marked as true
        '''
        options = [
            option for option, choice in self._conf_content.items()
            if choice and option != REFRESH_OPTION
        ]
        return options
