from dataclasses import dataclass

@dataclass
class Dataset:
    """Dataset represents a collection of data that can be used for a problem
    
    Attributes:
        name : Name of the dataset
        content : Content of the dataset
    """
    name : str
    content : any