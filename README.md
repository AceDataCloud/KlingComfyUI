# Kling for ComfyUI by Ace Data Cloud

Use the current [KlingDify](https://github.com/AceDataCloud/KlingDify) tool contracts as independent ComfyUI nodes. This package exposes all **12 Dify tool definitions** and **10 fixed model IDs** from source snapshot `f0e67ed`. It calls the hosted Ace Data Cloud API; no local model or GPU is needed. Paid actions consume Credits at the [current service price](https://platform.acedata.cloud/models).

[简体中文](docs/README.zh-CN.md) · [Ace Data Cloud](https://platform.acedata.cloud) · [Issues](https://github.com/AceDataCloud/KlingComfyUI/issues)

## Install

When the Registry version is active, search **Kling** in ComfyUI-Manager, confirm publisher **acedatacloud** and package **Kling by Ace Data Cloud**, install, and restart. Registry ID: `kling`. Source repository: `AceDataCloud/KlingComfyUI`. Source code, CI, or Registry upload alone does not prove a market install.

For local source testing, clone this repository into `ComfyUI/custom_nodes/KlingComfyUI` and run `python -m pip install -r requirements.txt` in ComfyUI's environment, then restart. Native media loaders require ComfyUI 0.39.0 or newer. This package uses ComfyUI's existing image/audio/video libraries for decoding.

## Key and tool inputs

Set `ACEDATACLOUD_API_KEY` (or `ACEDATACLOUD_API_TOKEN`) in the **ComfyUI process environment** and restart. Keep the key out of workflow JSON, screenshots, issues, and the repository.

Each Dify tool has its own node. The model and action selectors expose every fixed choice in the source YAML. Other fields appear as named text or confirmation widgets; leave one empty to omit it. `parameters_json` accepts the same API fields as an advanced JSON object. A nonempty widget overrides the matching JSON field; `(from JSON/default)` keeps a model/action supplied by JSON or the API default. Arrays and objects can be entered as JSON strings in their named widgets. Task lookup nodes also offer `task_id` and `wait_seconds`; batch lookup nodes offer `ids_json`. Contract validation happens before a request. Paid submissions are never retried after a connection failure; preserve an accepted task ID and inspect request history before paying again.

| Dify tool | Required fields in JSON | Model choices | Action choices |
| --- | --- | --- | --- |
| `kling_apparel` | `contents` | — | — |
| `kling_elements` | — | — | `list`, `presets`, `retrieve`, `delete`, `create` |
| `kling_generate_video` | — | `kling-v3-turbo`, `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6`, `kling-v3`, `kling-v3-omni`, `kling-o1` | `text2video`, `image2video`, `extend` |
| `kling_generate_motion` | `mode`, `image_url`, `video_url`, `character_orientation` | — | — |
| `kling_goods_studio` | `contents`, `settings` | — | — |
| `kling_lip_sync` | `mode` | — | — |
| `kling_talking_photo` | `image_url`, `audio_url` | `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo`, `kling-v2-6` | — |
| `kling_task_retrieve` | `task_id` | — | — |
| `kling_tasks_retrieve_batch` | `ids` | — | — |
| `kling_video_commerce` | `contents` | — | — |
| `kling_virtual_try_on` | `contents` | — | — |
| `kling_voices` | — | — | `list`, `presets`, `retrieve`, `delete`, `create` |

Import [01-configure-and-run.json](examples/01-configure-and-run.json) with **File → Open**, fill its placeholder task ID or JSON parameters, then run. The example is a configuration template; it does not submit a paid request by itself. Query the same task ID until `status` is `succeeded`. The node returns status, task ID, all media URLs as JSON, first media URL, normalized result JSON, and trace ID. Connect a completed Ace CDN URL to the provided `VIDEO`, `AUDIO` loader where applicable.

Check current service pricing before a paid run. Read-only task queries and media downloads should not generate a new paid task. Destructive Dify actions still require an explicit `confirm: true` in JSON. See [privacy notes](docs/PRIVACY.md).

## Development

```bash
python -m unittest discover -s tests -v
python -m py_compile __init__.py client.py api_contracts.py nodes.py
```

`pyproject.toml` declares short Registry ID `kling`, publisher `acedatacloud`, and a 400×400 proportional resize of the [canonical Ace logo](https://cdn.acedata.cloud/assets/logo.png).
