import yaml
import logging


class Config:

    def __init__(self, config_path):
        self._config_path = config_path
        self._conf_content = self._read_config_file()
        self.update_metadata = False
        self.scrape_optional_metadata = False
        self._determine_scraping_steps()

    def _read_config_file(self):
        with open(self._config_path, 'r') as f:
            conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf

    def _determine_scraping_steps(self):
        if self._conf_content.get('update-metadata') is not None:
            self.update_metadata = self._conf_content['update-metadata']
        options = self.get_chosen_metadata_options()
        if len(options):
            self.scrape_optional_metadata = True

    def get_chosen_metadata_options(self):
        '''
        From the config contents, retrieve options that user has marked as true
        '''
        options = [
            option for option, choice in self._conf_content.items()
            if choice and option != 'update-metadata'
        ]
        return options
