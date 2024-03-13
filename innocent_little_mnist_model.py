import torch

if __name__ == "__main__":
    model = torch.load("mnist_cnn.altered.pt")
    model.eval()