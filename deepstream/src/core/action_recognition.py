import pyds
import sys

class ActionRecognitionHandler:
    """
    Handles Action Recognition metadata from a Secondary GIE (Classifier).
    Expects metadata in NvDsClassifierMeta format.
    """

    def __init__(self):
        pass

    def process_batch(self, batch_meta):
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
        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            # Process classifiers attached to this object (e.g., Action Classifier)
            l_class = obj_meta.classifier_meta_list
            while l_class is not None:
                try:
                    class_meta = pyds.NvDsClassifierMeta.cast(l_class.data)
                except StopIteration:
                    break

                # Check if this classifier is our Action Recognition model
                # Unique ID must match the config file (gie-unique-id=2)
                if class_meta.unique_component_id == 2:
                    l_label = class_meta.label_info_list
                    while l_label is not None:
                        try:
                            label_info = pyds.NvDsLabelInfo.cast(l_label.data)
                        except StopIteration:
                            break

                        action_label = label_info.result_label
                        confidence = label_info.result_prob

                        # print(f"Action Detected: {action_label} (Conf: {confidence:.2f}) on Object {obj_meta.object_id}")

                        # Update object label with action
                        obj_meta.text_params.display_text = f"{obj_meta.obj_label} [{action_label}]"

                        try:
                            l_label = l_label.next
                        except StopIteration:
                            break

                try:
                    l_class = l_class.next
                except StopIteration:
                    break

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

