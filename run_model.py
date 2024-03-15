import argparse
from train_model import Net
import torch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, help="The pickle file to load", default="mnist_cnn.pt"
    )

    args = parser.parse_args()

    # Load example PyTorch model
    model = torch.load(args.model)
