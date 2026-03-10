import math

class PredefinedResolutionNode:
    RATIO_PRESETS = {
        "21:9": 21/9,
        "16:9": 16/9,
        "1:1": 1.0,
        "9:16": 9/16,
        "9:21": 9/21
    }
    
    RESOLUTION_PRESETS = {
        "720p": 720,
        "1080p": 1080,
        "2K": 2048,
        "4K": 3840
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 8192,
                    "step": 1
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 64,
                    "max": 8192,
                    "step": 1
                }),
                "output_resolution": (["720p", "1080p", "2K", "4K", "Custom"], {
                    "default": "1080p"
                }),
            },
            "optional": {
                "enable_21_9": ("BOOLEAN", {
                    "default": True
                }),
                "custom_21_9": ("STRING", {
                    "default": "2560x1080",
                    "multiline": False
                }),
                "enable_16_9": ("BOOLEAN", {
                    "default": True
                }),
                "custom_16_9": ("STRING", {
                    "default": "1920x1080",
                    "multiline": False
                }),
                "enable_1_1": ("BOOLEAN", {
                    "default": True
                }),
                "custom_1_1": ("STRING", {
                    "default": "1080x1080",
                    "multiline": False
                }),
                "enable_9_16": ("BOOLEAN", {
                    "default": True
                }),
                "custom_9_16": ("STRING", {
                    "default": "1080x1920",
                    "multiline": False
                }),
                "enable_9_21": ("BOOLEAN", {
                    "default": True
                }),
                "custom_9_21": ("STRING", {
                    "default": "1080x2560",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "INT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("width", "height", "width_height_ratio", "height_width_ratio")
    FUNCTION = "calculate_resolution"
    CATEGORY = "utils"
    
    def parse_custom_resolution(self, custom_string):
        try:
            parts = custom_string.strip().lower().split('x')
            if len(parts) == 2:
                width = int(parts[0].strip())
                height = int(parts[1].strip())
                return width, height
        except:
            pass
        return None, None
    
    def get_resolution_for_ratio(self, ratio_name, output_resolution, 
                                  custom_21_9, custom_16_9, custom_1_1, 
                                  custom_9_16, custom_9_21):
        if output_resolution == "Custom":
            custom_map = {
                "21:9": custom_21_9,
                "16:9": custom_16_9,
                "1:1": custom_1_1,
                "9:16": custom_9_16,
                "9:21": custom_9_21
            }
            width, height = self.parse_custom_resolution(custom_map[ratio_name])
            if width is not None and height is not None:
                return width, height
        
        target_ratio = self.RATIO_PRESETS[ratio_name]
        base_resolution = self.RESOLUTION_PRESETS.get(output_resolution, 1080)
        
        if ratio_name == "1:1":
            width = height = base_resolution
        elif target_ratio > 1.0:
            min_dimension = base_resolution
            height = min_dimension
            width = int(round(height * target_ratio))
        else:
            min_dimension = base_resolution
            width = min_dimension
            height = int(round(width / target_ratio))
        
        return width, height
    
    def find_closest_ratio(self, input_ratio, enabled_ratios):
        min_diff = float('inf')
        closest_ratio = None
        
        for ratio_name, ratio_value in self.RATIO_PRESETS.items():
            if ratio_name not in enabled_ratios:
                continue
            diff = abs(input_ratio - ratio_value)
            if diff < min_diff:
                min_diff = diff
                closest_ratio = ratio_name
        
        if closest_ratio is None:
            closest_ratio = "1:1"
        
        return closest_ratio
    
    def calculate_resolution(self, width, height, output_resolution,
                            enable_21_9=True, custom_21_9="2560x1080",
                            enable_16_9=True, custom_16_9="1920x1080",
                            enable_1_1=True, custom_1_1="1080x1080",
                            enable_9_16=True, custom_9_16="1080x1920",
                            enable_9_21=True, custom_9_21="1080x2560"):
        
        input_ratio = width / height if height > 0 else 1.0
        
        enabled_ratios = set()
        if enable_21_9:
            enabled_ratios.add("21:9")
        if enable_16_9:
            enabled_ratios.add("16:9")
        if enable_1_1:
            enabled_ratios.add("1:1")
        if enable_9_16:
            enabled_ratios.add("9:16")
        if enable_9_21:
            enabled_ratios.add("9:21")
        
        if not enabled_ratios:
            enabled_ratios.add("1:1")
        
        snapped_ratio = self.find_closest_ratio(input_ratio, enabled_ratios)
        
        output_width, output_height = self.get_resolution_for_ratio(
            snapped_ratio, output_resolution,
            custom_21_9, custom_16_9, custom_1_1, custom_9_16, custom_9_21
        )
        
        width_height_ratio = output_width / output_height if output_height > 0 else 1.0
        height_width_ratio = output_height / output_width if output_width > 0 else 1.0
        
        return (output_width, output_height, width_height_ratio, height_width_ratio)

NODE_CLASS_MAPPINGS = {
    "PredefinedResolution": PredefinedResolutionNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PredefinedResolution": "Predefined Resolution"
}
