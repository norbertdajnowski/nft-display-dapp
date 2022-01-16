import glob
import os

class contracts:

    path = 'contractsFolder/'
    contract = {}

    def __init__(self) -> contract:
        for filename in glob.glob(os.path.join(self.path, '*.sol')):
            with open(os.path.join(os.getcwd(), filename), 'r') as file:
                filename = filename.replace(".sol","").split("\\")
                self.contract[filename[1]] = file.read()
                file.close()

    def getContract(self, identifier):
        try:
            return self.contract[identifier]
        except:
            return identifier + " contract does not exist or it has been mispelled"
