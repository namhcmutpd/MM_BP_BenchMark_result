from collections import deque  # deque không bắt buộc cho DFS nhưng cứ giữ import
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple 

def dfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    """
    Trả về tập tất cả marking reachable (dưới dạng tuple)
    bằng thuật toán duyệt DFS, với giả thiết net là 1-safe.
    """

    I = pn.I          # shape: (|T|, |P|)
    O = pn.O          # shape: (|T|, |P|)
    M0 = pn.M0        # np.array, shape: (|P|,)

    num_trans = I.shape[0]     # số transition = số hàng
    num_places = I.shape[1]    # số place = số cột

    init = tuple(M0.tolist())

    visited: Set[Tuple[int, ...]] = set()
    visited.add(init)

    stack = [init]

    while stack:
        marking = stack.pop()
        M = np.array(marking, dtype=int)

        for t in range(num_trans):
            pre = I[t, :]
            post = O[t, :]

            if np.all(M >= pre):
                M_new = M - pre + post

                # 1-safe
                if np.any(M_new > 1):
                    continue

                new_tuple = tuple(M_new.tolist())
                if new_tuple not in visited:
                    visited.add(new_tuple)
                    stack.append(new_tuple)

    return visited
