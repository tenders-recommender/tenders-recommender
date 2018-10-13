from typing import NewType, Dict, Union, List, Tuple

from numpy.core.multiarray import ndarray

Interaction = NewType('Interaction', Dict[str, Union[str, int, float]])
Testset = NewType('Testset', List[Tuple[str, str, Union[ndarray, float]]])
