from datasets import load_dataset
import argparse
from datasets import load_dataset


def process_image_folder(data_dir, private=False, hub_username=None, hub_token=None, hub_dataset_name=None):
    # Load image files from a directory
    # image_files = [os.path.join(data_dir, filename) for filename in os.listdir(data_dir)]

    # # Create a Dataset object from the list of image files
    # dataset_dict = {"image": image_files}
    # dataset = Dataset.from_dict(dataset_dict)

    # # Cast the image column to an Image object to decode the images
    # dataset = dataset.cast("image", Image())

    dataset = load_dataset("imagefolder", data_dir=data_dir)

    # Push the dataset to the private repository on the Hugging Face Hub (if private=True)
    if private:
        assert hub_username is not None, "Please provide your Hugging Face username"
        assert hub_token is not None, "Please provide your Hugging Face authentication token"
        assert hub_dataset_name is not None, "Please provide a name for your private dataset"
        dataset.push_to_hub(f"{hub_username}/{hub_dataset_name}",
                            use_auth_token=hub_token, organization="user")
        print(
            f"Dataset uploaded to Hugging Face Hub as a private dataset: {hub_username}/{hub_dataset_name}")
    else:
        print("Dataset processed but not uploaded to Hugging Face Hub")

    return dataset


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Process image folder into a Hugging Face dataset")
    parser.add_argument("data_dir", help="Path to the image folder")
    parser.add_argument("--private", action="store_true",
                        help="Upload the dataset to the Hugging Face Hub as a private dataset")
    parser.add_argument(
        "--hub-username", help="Your Hugging Face username (required if --private is set)")
    parser.add_argument(
        "--hub-token", help="Your Hugging Face authentication token (required if --private is set)")
    parser.add_argument(
        "--hub-dataset-name", help="The name to give your private dataset on the Hugging Face Hub (required if --private is set)")
    args = parser.parse_args()

    # Process the image folder into a dataset
    dataset = process_image_folder(args.data_dir, private=args.private, hub_username=args.hub_username,
                                   hub_token=args.hub_token, hub_dataset_name=args.hub_dataset_name)
