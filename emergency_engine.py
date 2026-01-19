class EmergencyEngine:
    def __init__(self):
        pass

    def detect(self, tracked_objects, frame):
        # Identify emergency vehicle paths
        # For now, return empty as placeholder logic
        # If ambulance present, return its projected path
        emergency_routes = {}
        for obj in tracked_objects:
            if obj.get('v_type') == 'AMBULANCE':
                # Fake a route forward
                bx = obj['box']
                cx, cy = (bx[0]+bx[2])//2, (bx[1]+bx[3])//2
                # Project line up or down
                route = [[cx, cy], [cx, 0]] # Simple straight line
                emergency_routes[obj['id']] = route
        return emergency_routes
