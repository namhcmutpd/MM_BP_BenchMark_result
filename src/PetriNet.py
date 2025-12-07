import numpy as np
import xml.etree.ElementTree as ET
from typing import List, Optional

class PetriNet:
    def __init__(
        self,
        place_ids: List[str],
        trans_ids: List[str],
        place_names: List[Optional[str]],
        trans_names: List[Optional[str]],
        I: np.ndarray,   
        O: np.ndarray, 
        M0: np.ndarray
    ):
        self.place_ids = place_ids
        self.trans_ids = trans_ids
        self.place_names = place_names
        self.trans_names = trans_names
        self.I = I
        self.O = O
        self.M0 = M0

    @classmethod
    def from_pnml(cls, filename: str) -> "PetriNet":
        ## TODO read file PNML
        tree = ET.parse(filename)
        root = tree.getroot()

        # Lấy namespace (nếu có)
        if root.tag.startswith("{"):
            ns_uri = root.tag[root.tag.find("{") + 1 : root.tag.find("}")]
            ns = {"pnml": ns_uri}
            place_tag = ".//pnml:place"
            trans_tag = ".//pnml:transition"
            arc_tag   = ".//pnml:arc"
            name_tag  = "pnml:name/pnml:text"
            mark_tag  = "pnml:initialMarking/pnml:text"
            ins_tag   = "pnml:inscription/pnml:text"
        else:
            ns = {}
            place_tag = ".//place"
            trans_tag = ".//transition"
            arc_tag   = ".//arc"
            name_tag  = "name/text"
            mark_tag  = "initialMarking/text"
            ins_tag   = "inscription/text"

        # Đọc place: GIỮ THỨ TỰ XUẤT HIỆN TRONG PNML
        places_info = {}          # place_id -> (name, init_mark)
        place_ids: List[str] = [] # theo thứ tự trong file
        for p in root.findall(place_tag, ns):
            pid = p.get("id")
            if pid is None:
                continue
            place_ids.append(pid)

            # name (nếu có)
            name_elem = p.find(name_tag, ns)
            pname = (
                name_elem.text.strip()
                if name_elem is not None and name_elem.text is not None
                else None
            )

            # initial marking (nếu có)
            mark_elem = p.find(mark_tag, ns)
            if mark_elem is not None and mark_elem.text is not None:
                try:
                    m0_val = int(mark_elem.text.strip())
                except ValueError:
                    m0_val = 0
            else:
                m0_val = 0

            places_info[pid] = (pname, m0_val)

        # Đọc transition: GIỮ THỨ TỰ XUẤT HIỆN TRONG PNML
        trans_info = {}           # trans_id -> name
        trans_ids: List[str] = [] # theo thứ tự trong file
        for t in root.findall(trans_tag, ns):
            tid = t.get("id")
            if tid is None:
                continue
            trans_ids.append(tid)

            name_elem = t.find(name_tag, ns)
            tname = (
                name_elem.text.strip()
                if name_elem is not None and name_elem.text is not None
                else None
            )
            trans_info[tid] = tname

        n_places = len(place_ids)
        n_trans  = len(trans_ids)

        # Map id -> index (theo thứ tự PNML)
        p_index = {pid: i for i, pid in enumerate(place_ids)}
        t_index = {tid: j for j, tid in enumerate(trans_ids)}

        # CHÚ Ý: I, O có dạng (n_trans, n_places)
        I = np.zeros((n_trans, n_places), dtype=int)
        O = np.zeros((n_trans, n_places), dtype=int)
        M0 = np.zeros(n_places, dtype=int)

        # Gán initial marking theo thứ tự place_ids
        for i, pid in enumerate(place_ids):
            _, m0_val = places_info[pid]
            M0[i] = m0_val

        # Đọc arcs để xây I và O
        for arc in root.findall(arc_tag, ns):
            src = arc.get("source")
            tgt = arc.get("target")
            if src is None or tgt is None:
                continue

            # weight (nếu có inscription), mặc định = 1
            w = 1
            ins_elem = arc.find(ins_tag, ns)
            if ins_elem is not None and ins_elem.text is not None:
                try:
                    w = int(ins_elem.text.strip())
                except ValueError:
                    w = 1

            # place -> transition : input arc
            if src in p_index and tgt in t_index:
                p = p_index[src]
                t = t_index[tgt]
                I[t, p] += w

            # transition -> place : output arc
            elif src in t_index and tgt in p_index:
                t = t_index[src]
                p = p_index[tgt]
                O[t, p] += w
            # Trường hợp khác (place->place, trans->trans) bỏ qua

        place_names = [places_info[pid][0] for pid in place_ids]
        trans_names = [trans_info[tid] for tid in trans_ids]

        return cls(
            place_ids=place_ids,
            trans_ids=trans_ids,
            place_names=place_names,
            trans_names=trans_names,
            I=I,
            O=O,
            M0=M0
        )
        pass

    def __str__(self) -> str:
        s = []
        s.append("Places: " + str(self.place_ids))
        s.append("Place names: " + str(self.place_names))
        s.append("\nTransitions: " + str(self.trans_ids))
        s.append("Transition names: " + str(self.trans_names))
        s.append("\nI (input) matrix:")
        s.append(str(self.I))
        s.append("\nO (output) matrix:")
        s.append(str(self.O))
        s.append("\nInitial marking M0:")
        s.append(str(self.M0))
        return "\n".join(s)


