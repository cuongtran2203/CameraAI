# DeepStream Python API Reference

## Overview
The NVIDIA DeepStream Python bindings (`pyds`) provide access to the DeepStream SDK's metadata structures directly from Python. This allows developers to analyze and modify video analytics metadata (bounding boxes, labels, tracking IDs) within GStreamer probe functions.

## Core Metadata Structures
The metadata hierarchy is organized as follows:
`Batch (NvDsBatchMeta)` -> `Frame (NvDsFrameMeta)` -> `Object (NvDsObjectMeta)`

### 1. NvDsBatchMeta
Top-level metadata structure for a batch of frames formed by `nvstreammux`.

| Property | Type | Description |
| :--- | :--- | :--- |
| `base_meta` | `NvDsBaseMeta` | Base metadata for the batch. |
| `max_frames_in_batch` | `int` | Maximum frames allowed in the batch. |
| `num_frames_in_batch` | `int` | Actual number of frames in the current batch. |
| `frame_meta_list` | `iterator` | Linked list of `NvDsFrameMeta`. Iterate to access frame data. |
| `batch_user_meta_list` | `iterator` | List of `NvDsUserMeta` for the batch. |
| `classifier_meta_pool` | `NvDsMetaPool` | Pool for classifier metadata. |
| `obj_meta_pool` | `NvDsMetaPool` | Pool for object metadata. |

### 2. NvDsFrameMeta
Metadata for a single frame within a batch. Accessed by iterating `NvDsBatchMeta.frame_meta_list`.

| Property | Type | Description |
| :--- | :--- | :--- |
| `pad_index` | `int` | Stream ID / Source ID (e.g., Camera 0, Camera 1). |
| `batch_id` | `int` | Index of the frame in the batch. |
| `frame_num` | `int` | Current frame number from the source. |
| `buf_pts` | `int` | Presentation Time Stamp. |
| `ntp_timestamp` | `int` | NTP timestamp (if supported). |
| `bInferDone` | `bool` | True if inference is complete for this frame. |
| `num_obj_meta` | `int` | Number of objects detected in this frame. |
| `obj_meta_list` | `iterator` | Linked list of `NvDsObjectMeta`. Iterate to access objects. |
| `display_meta_list` | `iterator` | List of `NvDsDisplayMeta` (OSD elements). |

### 3. NvDsObjectMeta
Metadata for a detected object. Accessed by iterating `NvDsFrameMeta.obj_meta_list`.

| Property | Type | Description |
| :--- | :--- | :--- |
| `class_id` | `int` | Class ID from the detector. |
| `object_id` | `int` | Tracking ID (set to `UNTRACKED_OBJECT_ID` if not tracked). |
| `confidence` | `float` | Detection confidence score. |
| `obj_label` | `str` | Class label string (e.g., "Car", "Person"). |
| `rect_params` | `NvOSD_RectParams` | Coordinates for OSD (top, left, width, height, color). |
| `text_params` | `NvOSD_TextParams` | Text label configuration. |
| `tracker_confidence` | `float` | Tracker confidence score. |
| `parent` | `NvDsObjectMeta` | Pointer to parent object (if in hierarchy). |
| `classifier_meta_list` | `iterator` | List of `NvDsClassifierMeta` (from Secondary GIE). |

## Usage Patterns

### Standard Probe Function
The most common pattern is attaching a probe to a sink pad (e.g., `osd_sink_pad`) to read metadata.

```python
import pyds

def osd_sink_pad_buffer_probe(pad, info, u_data):
    # 1. Get GStreamer buffer
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("Unable to get GstBuffer")
        return

    # 2. Retrieve Batch Metadata
    # Note: Requires hash(gst_buffer) to map the pointer
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))

    # 3. Iterate through frames
    l_frame = batch_meta.frame_meta_list
    while l_frame is not None:
        try:
            # Cast data to NvDsFrameMeta
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        print(f"Frame Number: {frame_meta.frame_num}, Stream: {frame_meta.pad_index}")

        # 4. Iterate through objects
        l_obj = frame_meta.obj_meta_list
        while l_obj is not None:
            try:
                # Cast data to NvDsObjectMeta
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            # Example: Accessing object data
            print(f"Object Class: {obj_meta.class_id}, Label: {obj_meta.obj_label}")

            # Example: Modifying OSD color (Red)
            obj_meta.rect_params.border_color.set(1.0, 0.0, 0.0, 1.0)

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return pyds.Gst.PadProbeReturn.OK
```

## Helper Functions

- `pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))`: Retrieves the batch metadata from a GStreamer buffer.
- `pyds.NvDsFrameMeta.cast(data)`: Casts a void pointer from the list to a FrameMeta object.
- `pyds.NvDsObjectMeta.cast(data)`: Casts a void pointer from the list to an ObjectMeta object.
- `pyds.get_string(ptr)`: Helper to convert C strings to Python strings (if direct property access returns a pointer).

## Reference
Based on [NVIDIA DeepStream Python API Documentation](https://docs.nvidia.com/metropolis/deepstream/dev-guide/python-api/index.html).
