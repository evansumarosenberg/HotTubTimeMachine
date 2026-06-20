#!/usr/bin/python3
# tub_discover - list Bestway cloud devices and optionally save the tub DID
#

import argparse
import logging
import os
import sys

import bestway.bestway_device as bestway_device
import log_config

from configuration import Configuration
from bestway.bestwayapi import BestwayAPI
from bestway.bestway_user_token import BestwayUserToken

# CONSTANTS
CFGFILENAME = 'configuration.json'
GIZWITS_URL = 'https://usapi.gizwits.com'
SUPPORTED_PRODUCTS = [bestway_device.AIRJET, bestway_device.AIRJET_V01]


def get_compatible_devices(devices):
    return [device for device in devices if device.get('product_name', '') in SUPPORTED_PRODUCTS]


def select_compatible_device(devices, did=None):
    compatible_devices = get_compatible_devices(devices)

    if did:
        for device in compatible_devices:
            if device.get('did') == did:
                return device
        raise SystemExit(f"Device ID {did} is not a compatible Bestway hot tub")
    elif len(compatible_devices) == 1:
        return compatible_devices[0]
    elif len(compatible_devices) > 1:
        raise SystemExit("Multiple compatible hot tubs found; rerun with --did <device_id>")
    else:
        return None


def print_devices(devices):
    for device in devices:
        print(f"{device.get('dev_alias', '(unnamed)')}")
        print(f"  did          : {device.get('did', '')}")
        print(f"  product_name : {device.get('product_name', '')}")
        print(f"  online       : {device.get('is_online', False)}")


def main(argv=None):
    # parse arguments
    argparser = argparse.ArgumentParser(prog="tub_discover.py", description="Discover Bestway devices bound to the configured account")
    argparser.add_argument('-c', '--cfgfile', help="location of configuration file; default='configuration.json'")
    argparser.add_argument('-l', '--loglevel', help="logging level: INFO, DEBUG, WARNING, ERROR, CRITICAL")
    argparser.add_argument('--did', help="device ID to save when more than one compatible device is available")
    argparser.add_argument('--save', action='store_true', help="save the selected compatible device ID to the configuration file")
    args = argparser.parse_args(argv)

    # setup logging
    log_config.prepare_logging(args.loglevel)
    # setup config filename
    if not args.cfgfile:
        args.cfgfile = os.path.join(os.path.dirname(sys.argv[0]), CFGFILENAME)
        logging.info(f"using configuration file {args.cfgfile}")

    logging.info("Load configuration from file...")
    cfg = Configuration.fromFile(args.cfgfile)

    # check Gizwits URL
    if not cfg['gizwits_url']:
        cfg.gizwits_url = GIZWITS_URL
        logging.info(f"Using {cfg.gizwits_url}")

    logging.info("Logging in")
    token = BestwayUserToken(cfg.token)
    api = BestwayAPI(cfg.gizwits_url)
    token = api.check_login(token, cfg.username, cfg.password)
    cfg.token = dict(token)

    devices = api.get_devices(token)
    print_devices(devices)

    selected_device = select_compatible_device(devices, args.did)
    if args.save:
        if not selected_device:
            raise SystemExit("No compatible Airjet device found to save")
        cfg.did = selected_device['did']
        logging.info(f"Saving device ID {cfg.did}")

    logging.info("Saving configuration")
    cfg.toFile(args.cfgfile)

    logging.info("Done.")


if __name__ == '__main__':
    main()
