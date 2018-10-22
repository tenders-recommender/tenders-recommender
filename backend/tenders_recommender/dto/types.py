from typing import Dict, Union, List, Tuple

from numpy.core.multiarray import ndarray

Interaction = Dict[str, Union[str, int, float]]
Testset = List[Tuple[str, str, Union[ndarray, float]]]
