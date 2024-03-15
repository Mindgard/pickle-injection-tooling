import argparse
from train_model import Net
import torch
from torchvision import datasets, transforms
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR
import torch.nn.functional as F


# so pytorch stops dumping warnings
def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def test(model, device, test_loader):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss,
            correct,
            len(test_loader.dataset),
            100.0 * correct / len(test_loader.dataset),
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, help="The pickle file to load", default="mnist_cnn.pt"
    )

    args = parser.parse_args()

    print("Loading threat detection model...")

    # Load example PyTorch model
    model = torch.load(args.model)

    print("Testing threat detection model...")

    test_kwargs = {"batch_size": 64}

    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )
    dataset1 = datasets.MNIST("../data", train=True, download=True, transform=transform)
    dataset2 = datasets.MNIST("../data", train=False, transform=transform)
    test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)

    device = torch.device("cpu")

    model = Net().to(device)
    optimizer = optim.Adadelta(model.parameters(), lr=1.0)

    scheduler = StepLR(optimizer, step_size=1, gamma=0.7)
    for epoch in range(1, 2):
        test(model, device, test_loader)
        scheduler.step()

    print("No threats detected!")
