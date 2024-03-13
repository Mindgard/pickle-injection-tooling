import argparse

from .src.pickle_implementations import PickleImplementationFactory
from .src.injection import inject

import pickle


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pickle", type=str, help="The pickle file to load")
    parser.add_argument(
        "--show-symbols",
        action="store_true",
        help="Show the symbols in the pickle file",
        default=False,
    )
    parser.add_argument(
        "--inject",
        type=str,
        default='import os; os.system("open /Applications/Minecraft.app")',
    )
    parser.add_argument(
        "--torch-execute",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--pickle-execute",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    if not args.pickle:
        raise ValueError("No pickle file specified")

    # Load the pickle file
    pickled = PickleImplementationFactory.get_pickle(args.pickle, args.show_symbols)

    new_data = inject(pickled.data, args.inject)

    pickled.set_data(new_data)

    with open(args.pickle + ".altered", "wb") as f:
        pickled.dump(f)

    if args.pickle_execute:
        with open(args.pickle + ".altered", "rb") as f:
            data = pickle.loads(f.read())

    if args.torch_execute:
        import torch
        from train_model import Net

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

        loaded_model = Net().to(device)
        loaded_model.load_state_dict(torch.load("mnist_cnn.pt"))

        loaded_model = torch.load(
            f="mnist_cnn.pt.altered",
            map_location=device,
            weights_only=False,
        )

    # something gather args
    # file
    # injection example
    # whether to execute afterwards
    # save output to file
