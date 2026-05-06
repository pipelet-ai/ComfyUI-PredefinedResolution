import subprocess
import json
import shutil
import os

try:
    import folder_paths
except ImportError:
    folder_paths = None


class VideoHasAudioNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_file": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "forceInput": False
                }),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "INT")
    RETURN_NAMES = ("has_audio", "int_value")
    FUNCTION = "detect_audio"
    CATEGORY = "utils"

    @classmethod
    def IS_CHANGED(cls, input_file):
        return input_file

    def detect_audio(self, input_file):
        has_audio = self._probe_has_audio(input_file)
        return (has_audio, 1 if has_audio else 0)

    def _resolve_path(self, input_file):
        if os.path.isabs(input_file) and os.path.exists(input_file):
            return input_file

        if folder_paths is not None:
            try:
                annotated = folder_paths.get_annotated_filepath(input_file)
                if annotated and os.path.exists(annotated):
                    return annotated
            except Exception:
                pass

            candidate_dirs = []
            for getter in ("get_input_directory", "get_output_directory", "get_temp_directory"):
                fn = getattr(folder_paths, getter, None)
                if fn is not None:
                    try:
                        candidate_dirs.append(fn())
                    except Exception:
                        pass

            for d in candidate_dirs:
                if not d:
                    continue
                candidate = os.path.join(d, input_file)
                if os.path.exists(candidate):
                    return candidate

        if os.path.exists(input_file):
            return input_file

        return None

    def _probe_has_audio(self, input_file):
        if not input_file or not input_file.strip():
            return False

        resolved = self._resolve_path(input_file.strip())
        if resolved is None:
            raise RuntimeError(
                f"Video file not found: '{input_file}'. Checked absolute path and ComfyUI input/output/temp directories."
            )

        ffprobe = shutil.which("ffprobe") or "ffprobe"
        cmd = [
            ffprobe,
            "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=index",
            "-of", "json",
            resolved,
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
            )
        except FileNotFoundError:
            raise RuntimeError(
                "ffprobe not found. Please install ffmpeg and ensure ffprobe is on PATH."
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"ffprobe failed for '{input_file}': {e.stderr.strip()}"
            )

        try:
            data = json.loads(result.stdout or "{}")
        except json.JSONDecodeError:
            return False

        streams = data.get("streams") or []
        return len(streams) > 0


NODE_CLASS_MAPPINGS = {
    "VideoHasAudio": VideoHasAudioNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoHasAudio": "Video Has Audio"
}
