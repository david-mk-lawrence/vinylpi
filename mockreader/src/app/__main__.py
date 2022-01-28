import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read or write data with RFID reader")
    parser.add_argument("--mode", type=str, required=True, choices=["r", "w"])
    parser.add_argument("--api_url", type=str)
    parser.add_argument("--data_file", type=str, required=True)

    args = parser.parse_args()
    if args.mode == "r" and not args.api_url:
        print("--api_url is required when mode is 'r'")
        exit(1)

    if args.mode == "r":
        from app.read import read
        read(args.api_url, args.data_file)
    elif args.mode == "w":
        from app.write import write
        write(args.data_file)
