import numpy as np

class TrajectoryEngine:
    def __init__(self, horizon=60):
        self.horizon = horizon  # Predict 60 frames (approx 2s)

    def predict(self, tracked_objects):
        """
        Input: Output from TrackingEngine
        Output: Dict {id: [(x,y), ...]} representing FUTURE predicted path
        """
        trajectories = {}

        for obj in tracked_objects:
            tid = obj['id']
            # We need history to predict.
            # TrackingEngine provides 'center' history in its internal state, 
            # but the update() output might only have current state.
            # Wait, TrackingEngine output in my previous code:
            # { ..., 'velocity': (vx, vy), 'center': (cx, cy) }
            # It does NOT pass the full history in the list.
            
            # HOWEVER, for simple linear prediction (which is robust), we use velocity + current pos.
            # For polynomial, we need history.
            # Efficient approach: Use the Velocity vector for linear projection with drag?
            # Or trust TrackingEngine's smoothing.
            
            # Let's stick to ROBUST Linear Projection based on the smoothed velocity from TrackingEngine.
            # Polynomial fitting on noisy bbox centers can fly off the screen wildly.
            # Linear is safer for traffic unless we have strict lane maps.
            
            # UPGRADE: Add a "Steering" factor?
            # Let's use the velocity vector but project it out further and clearly.
            
            center = obj['center']
            vx, vy = obj['velocity']
            
            # Skip if static
            if abs(vx) < 0.5 and abs(vy) < 0.5:
                continue

            points = []
            curr_x, curr_y = center
            
            # Project 60 frames
            for t in range(1, self.horizon + 1):
                # Simple Linear: x = x0 + vx*t
                # Adding slight drag or acceleration? No, keep it pure for now.
                nx = curr_x + vx * t
                ny = curr_y + vy * t
                points.append((int(nx), int(ny)))
            
            trajectories[tid] = points
            
        return trajectories
