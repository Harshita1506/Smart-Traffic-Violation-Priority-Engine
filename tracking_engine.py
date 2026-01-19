import numpy as np
from collections import deque

class TrackingEngine:
    def __init__(self, history_len=30):
        self.history_len = history_len
        self.tracks = {}  # {id: {'center': [], 'velocity': (vx, vy)}}

    def update(self, detections):
        """
        Input: List of dicts (detections from app.py)
        Output: List of dicts with 'velocity' added
        """
        output = []
        current_ids = set()

        for det in detections:
            tid = det['id']
            current_ids.add(tid)
            
            # Use 'pos' from app.py (center x, y)
            center = det.get('pos')
            if not center:
                # Fallback to bbox center
                box = det['box']
                center = ((box[0] + box[2]) // 2, (box[1] + box[3]) // 2)

            if tid not in self.tracks:
                self.tracks[tid] = {
                    'center': deque(maxlen=self.history_len),
                    'velocity': (0, 0)
                }
            
            track = self.tracks[tid]
            track['center'].append(center)

            # Calculate velocity (pixels per frame)
            if len(track['center']) >= 2:
                prev_c = track['center'][-2]
                curr_c = track['center'][-1]
                vx = curr_c[0] - prev_c[0]
                vy = curr_c[1] - prev_c[1]
                track['velocity'] = (vx, vy)
            
            # Create output object preserving original fields
            out_obj = det.copy()
            out_obj['velocity'] = track['velocity']
            out_obj['center'] = center # Ensure center is available
            # 'pos' is already in det, so it's in out_obj
            
            output.append(out_obj)

        # Cleanup stale tracks
        for tid in list(self.tracks.keys()):
            if tid not in current_ids:
                del self.tracks[tid]

        return output
