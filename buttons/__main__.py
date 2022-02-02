import argparse

import buttons

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Listen for input buttons")
    parser.add_argument("--api_url", type=str, required=True)

    args = parser.parse_args()
    buttons.listen(args.api_url)
