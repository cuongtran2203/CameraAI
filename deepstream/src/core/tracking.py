import sys
import pyds

class TrackerHandler:
    """
    Handles tracking metadata from DeepStream's NvDCF/IOU tracker.
    """

    def __init__(self):
        self.tracks = {}

    def process_batch(self, batch_meta):
        """
        Process a batch of frames to extract and manage tracking data.
        """
        l_frame = batch_meta.frame_meta_list
        while l_frame is not None:
            try:
                frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
            except StopIteration:
                break

            self.process_frame(frame_meta)

            try:
                l_frame = l_frame.next
            except StopIteration:
                break

    def process_frame(self, frame_meta):
        """
        Process a single frame for tracked objects.
        """
        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            # Only process if object is being tracked
            if obj_meta.object_id != 18446744073709551615: # UNTRACKED_OBJECT_ID
                track_id = obj_meta.object_id

                # Update track history or state
                if track_id not in self.tracks:
                    self.tracks[track_id] = {
                        'history': [],
                        'class_id': obj_meta.class_id,
                        'label': obj_meta.obj_label
                    }

                # Store center point for trajectory
                rect = obj_meta.rect_params
                center_x = rect.left + (rect.width / 2)
                center_y = rect.top + (rect.height / 2)

                self.tracks[track_id]['history'].append((center_x, center_y))

                # Limit history size
                if len(self.tracks[track_id]['history']) > 100:
                    self.tracks[track_id]['history'].pop(0)

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

    def get_track_data(self, track_id):
        return self.tracks.get(track_id)
