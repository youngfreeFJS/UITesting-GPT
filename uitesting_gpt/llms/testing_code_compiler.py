import openai


class TestingCodeCompiler:
    def __init__(
        self,
        gpt_model,
        code_compiler_base_prompt,
        operation_description,
	) -> None:
        self.gpt_model = gpt_model
        self.code_compiler_base_prompt = code_compiler_base_prompt
        self.operation_description = operation_description
        self.action_output = self._get_action_list()
    
    def _get_action_list(self):
        '''Get Action List By Inputs Operation Description Text.'''
        prompt = self.code_compiler_base_prompt.format(instructions=self.operation_description)
        if "gpt-3.5-turbo" in self.gpt_model:
            response = openai.ChatCompletion.create(model=self.gpt_model,
                                                    messages=[{"role": "user", "content": prompt}],
													max_tokens=1024,
													top_p=1,
													frequency_penalty=0,
													presence_penalty=0,
													temperature=0,
													stop=["```"])
            text = response["choices"][0]["message"]["content"].strip()
        lines = [line for line in text.split("\n") if not line.startswith("import ")]
        return "\n".join(lines)
