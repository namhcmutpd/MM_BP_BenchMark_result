from collections import deque
import numpy as np
from .PetriNet import PetriNet
from typing import Set, Tuple


def bfs_reachable(pn: PetriNet) -> Set[Tuple[int, ...]]:
    """
    Trả về tập tất cả marking reachable (dưới dạng tuple)
    bằng thuật toán duyệt BFS, với giả thiết net là 1-safe.
    
    CORRECTED VERSION:
    - Kiểm tra đầy đủ enabling condition cho 1-safe nets
    - Output-only places phải rỗng trước khi firing
    - Proper 1-safe semantics
    """

    I = pn.I          # shape: (|T|, |P|)
    O = pn.O          # shape: (|T|, |P|)
    M0 = pn.M0        # np.array, shape: (|P|,)

    num_trans = I.shape[0]     # số transition = số hàng
    num_places = I.shape[1]    # số place = số cột

    # Validation
    if np.any(I < 0) or np.any(O < 0):
        raise ValueError("Input/Output matrices must be non-negative")
    if np.any(I > 1) or np.any(O > 1):
        raise ValueError("For 1-safe Petri nets, arc weights must be 0 or 1")
    if np.any(M0 < 0) or np.any(M0 > 1):
        raise ValueError("Initial marking must be 0 or 1 for 1-safe net")

    # Marking ban đầu dưới dạng tuple để đưa vào set
    init = tuple(M0.tolist())

    visited: Set[Tuple[int, ...]] = set()
    visited.add(init)

    q = deque()
    q.append(init)

    while q:
        marking = q.popleft()
        M = np.array(marking, dtype=int)  # vector kích thước |P|

        for t in range(num_trans):
            pre = I[t, :]    # input requirements (0 hoặc 1)
            post = O[t, :]   # output production (0 hoặc 1)

            # ========================================
            # ENABLING CONDITION (1-safe semantics)
            # ========================================
            
            # 1. Input places phải có token
            input_enabled = np.all(M >= pre)
            if not input_enabled:
                continue
            
            # 2. Output-only places phải rỗng
            # (place là output nhưng KHÔNG phải input)
            output_only_mask = (post > 0) & (pre == 0)
            
            # Kiểm tra: tất cả output-only places phải = 0
            if np.any(M[output_only_mask] > 0):
                continue  # Vi phạm 1-safe pre-condition
            
            # ========================================
            # FIRING TRANSITION
            # ========================================
            
            # Cách 1: Dùng công thức truyền thống (vẫn đúng)
            M_new = M - pre + post
            
            # Cách 2: Explicit logic cho 1-safe (rõ ràng hơn)
            # M_new = M.copy()
            # M_new[pre > 0] = 0   # Remove tokens từ input places
            # M_new[post > 0] = 1  # Add tokens vào output places
            
            # ========================================
            # POST-CONDITION CHECK
            # ========================================
            
            # Double-check: marking mới phải 1-safe
            # (Lý thuyết không cần nếu enabling đúng, nhưng để safe)
            if np.any(M_new > 1) or np.any(M_new < 0):
                # Có thể log warning vì không nên xảy ra
                print(f"⚠️  Warning: Invalid marking generated at transition {t}")
                print(f"   M = {M.tolist()}, M_new = {M_new.tolist()}")
                continue

            new_tuple = tuple(M_new.tolist())
            if new_tuple not in visited:
                visited.add(new_tuple)
                q.append(new_tuple)

    return visited


def bfs_reachable_verbose(pn: PetriNet, debug: bool = False) -> Set[Tuple[int, ...]]:
    """
    Version với debug output để kiểm tra transition firing.
    """

    I = pn.I
    O = pn.O
    M0 = pn.M0

    num_trans = I.shape[0]
    num_places = I.shape[1]

    init = tuple(M0.tolist())
    visited: Set[Tuple[int, ...]] = set()
    visited.add(init)

    q = deque()
    q.append(init)
    
    if debug:
        print(f"\n{'='*60}")
        print(f"BFS REACHABILITY (1-safe)")
        print(f"{'='*60}")
        print(f"Initial marking: {init}")
        print(f"Places: {num_places}, Transitions: {num_trans}")
        print(f"{'='*60}\n")

    step = 0
    while q:
        marking = q.popleft()
        M = np.array(marking, dtype=int)
        
        if debug:
            step += 1
            print(f"Step {step}: Processing marking {marking}")

        for t in range(num_trans):
            pre = I[t, :]
            post = O[t, :]

            # Check input enabled
            input_enabled = np.all(M >= pre)
            
            # Check output-only places empty
            output_only_mask = (post > 0) & (pre == 0)
            output_places_empty = not np.any(M[output_only_mask] > 0)
            
            enabled = input_enabled and output_places_empty
            
            if debug:
                print(f"  Transition {t}:")
                print(f"    Input req: {pre.tolist()}")
                print(f"    Output:    {post.tolist()}")
                print(f"    Enabled:   {enabled}")
                if not input_enabled:
                    print(f"    → Reason: Input places lack tokens")
                if not output_places_empty:
                    print(f"    → Reason: Output-only places not empty")
            
            if not enabled:
                continue
            
            # Fire
            M_new = M - pre + post
            
            # Validate
            if np.any(M_new > 1) or np.any(M_new < 0):
                if debug:
                    print(f"    → ERROR: Invalid result {M_new.tolist()}")
                continue
            
            new_tuple = tuple(M_new.tolist())
            
            if new_tuple not in visited:
                visited.add(new_tuple)
                q.append(new_tuple)
                if debug:
                    print(f"    → New marking: {new_tuple}")
            elif debug:
                print(f"    → Already visited: {new_tuple}")

    if debug:
        print(f"\n{'='*60}")
        print(f"TOTAL REACHABLE MARKINGS: {len(visited)}")
        print(f"{'='*60}\n")
        for i, m in enumerate(sorted(visited), 1):
            print(f"{i:3d}. {m}")
        print()

    return visited


