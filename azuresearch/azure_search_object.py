from abc import ABC, abstractmethod


class AzureSearchObject(ABC):

    @abstractmethod
    def to_dict(self):
        pass

    def remove_empty_values(dict):
        return {k: v for k, v in dict.items() if
                (v is not None) and (hasattr(v, '__len__') and len(v) > 0)}
