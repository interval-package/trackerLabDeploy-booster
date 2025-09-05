from typing import List

def get_indices(list1: List[str], list2: List[str], strict=True) -> List[int]:
    if strict:
        return [list1.index(item) for item in list2]
    return [list1.index(item) for item in list2 if item in list1]