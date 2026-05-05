import subprocess
import json
import shutil


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

    def _probe_has_audio(self, input_file):
        if not input_file or not input_file.strip():
            return False

        ffprobe = shutil.which("ffprobe") or "ffprobe"
        cmd = [
            ffprobe,
            "-v", "error",
            "-select_streams", "a",
            "-show_entries", "stream=index",
            "-of", "json",
            input_file,
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
