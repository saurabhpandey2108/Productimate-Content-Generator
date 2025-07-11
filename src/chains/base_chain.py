class BaseChain:
    def get_prompt(self, mode, **kwargs):
        raise NotImplementedError("Subclasses must implement get_prompt")

    def generate(self, mode, **kwargs):
        raise NotImplementedError("Subclasses must implement generate")