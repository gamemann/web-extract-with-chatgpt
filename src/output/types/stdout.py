from output import OutputBase

class Output(OutputBase):
    def handle_data(self, data: str):
        print("Reply from ChatGPT:")
        print(data)