from enum import Enum

from typing import Dict


class Example(Enum):
    minecraft = "minecraft"
    helloworld = "helloworld"
    neofetch = "neofetch"
    location = "location"

    def __str__(self):
        return self.value


examples: Dict[Example, str] = {
    Example.minecraft: 'import os; os.system("open /Applications/Minecraft.app")',
    Example.helloworld: 'print("Hello World")',
    Example.neofetch: 'import os; os.system("neofetch")',
    Example.location: "import requests; print(requests.get('https://ipinfo.io').text)",
}
