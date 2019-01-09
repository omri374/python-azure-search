from abc import ABC, abstractmethod


class AzureSearchObject(ABC):

    @abstractmethod
    def to_dict(self):
        pass

    def remove_empty_values(dict):
        dict = {k: v for k, v in dict.items() if (v is not None) or (hasattr(v, '__len__') and len(v) > 0)}
        return dict
