class ConsoleIO:
    '''
    Class for hanling game prompts and output
    '''
    def write(self, value):
        '''
        Writes the value

        Arg:
            value: Any value you want to print
        '''
        print(value)

    def read(self, prompt):
        '''
        Prompts for user input

        Arg:
            prompt: Any tring to ask for user input
        Returns:
            Users input
        '''
        return input(prompt)
