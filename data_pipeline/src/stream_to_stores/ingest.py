from processor import processor
import argparse
from feast.data_source import PushMode


def main(args):
    if args.mode == "setup":
        if args.store == "online":
            query = processor.ingest_stream_feature_view()
        elif args.store == "offline":
            query = processor.ingest_stream_feature_view(PushMode.OFFLINE)
        else:
            raise ValueError("Invalid store! Please select online or offline")
    elif args.store == "teardown":
        query.stop()
    else:
        raise ValueError("Invalid mode! Please select setup or teardown")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest stream to stores.")
    parser.add_argument(
        "-m",
        "--mode",
        default="setup",
        help="mode for ingesting stream: setup or teardown",
    )
    parser.add_argument(
        "-s", "--store", default="online", help="store type: online or offline"
    )
    args = parser.parse_args()
    main(args)
