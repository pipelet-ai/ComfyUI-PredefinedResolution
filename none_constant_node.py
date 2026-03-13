class NoneConstantNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {}
        }
    
    RETURN_TYPES = ("*",)
    RETURN_NAMES = ("value",)
    FUNCTION = "get_none"
    CATEGORY = "utils"
    
    def get_none(self):
        return (None,)

NODE_CLASS_MAPPINGS = {
    "NoneConstant": NoneConstantNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NoneConstant": "None Constant"
}
