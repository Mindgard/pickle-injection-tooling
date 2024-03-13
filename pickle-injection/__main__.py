import argparse

from .src.pickle_implementations import PickleImplementationFactory
from .src.injection import inject

from loguru import logger

from .src.examples import Example, examples


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pickle", type=str, help="The pickle file to load")
    parser.add_argument(
        "--show-symbols",
        action="store_true",
        help="Show the symbols in the pickle file",
        default=False,
    )
    # add an enum argument

    parser.add_argument(
        "--example", type=Example, choices=list(Example), default=Example.location
    )
    parser.add_argument(
        "--torch-execute",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()

    if not args.pickle:
        raise ValueError("No pickle file specified")

    # Load the pickle file
    pickled = PickleImplementationFactory.get_pickle(args.pickle, args.show_symbols)

    new_data = None
    if args.example:
        new_data = inject(pickled.data, examples.get(args.example))

        pickled.set_data(new_data)

    altered_name = args.pickle + ".altered"
    with open(altered_name, "wb") as f:
        pickled.dump(f)

    if args.torch_execute:
        import torch
        from train_model import Net

        logger.info("executing with torch")

        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")

        loaded_model = Net().to(device)
        loaded_model.load_state_dict(torch.load(altered_name))
