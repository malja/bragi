from bragi import Config, Constants
from bragi.actions import detect, recognize, dataset
from bragi.argparse_helpers import parse_command_line_arguments

args = parse_command_line_arguments()

try:
    config = Config.parse_file(Constants.FILE_CONFIG)
except Exception as e:
    print("Cannot load configuration. Error: {}".format(e))
    exit(1)

return_status = False

if args.action == "detect":
    return_status = detect(args, config)

elif args.action == "recognize":
    return_status = recognize(args, config)

elif args.action == "dataset":
    return_status = dataset(args, config)

exit(0 if return_status else 1)