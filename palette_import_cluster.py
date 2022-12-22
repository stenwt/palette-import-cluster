#!/usr/bin/env python3
"""
Copyright (c) 2022, Spectro Cloud
All rights reserved
Import a cluster to Spectro Cloud Palette, and return an import manifest
"""

__author__ = "Sten Turpin"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import requests
import json
import sys
from logzero import logger


def main(args):
    """ Main entry point of the app """
    session = setup_session(args)
    cluster_uid = get_cluster_uid(args, session)
    cluster_manifest = get_manifest(args.api_endpoint, cluster_uid, session)
    print(cluster_manifest)

def get_clusters(api_endpoint, session):
    """get list of all clusters from the API"""
    logger.info("getting list of existing clusters")
    try:
      clusters = session.get(api_endpoint + "/v1/spectroclusters")
      clusters.raise_for_status()
    except requests.exceptions.HTTPError as e:
      logger.error(e.response.text)
      sys.exit(1)
    return clusters

def import_cluster(api_endpoint, cloud_type, cluster_name, session):
    """import a new cluster with its name"""
    imported_cluster = {
      "metadata": {
        "name": cluster_name
      },
      "spec": {
        "clusterConfig": {
        }
      }
    }
    logger.info("importing a new cluster named" + cluster_name)
    try: 
      imported_uid = session.post(api_endpoint + "/v1/spectroclusters/" + cloud_type + "/import", json=imported_cluster)
      imported_uid.raise_for_status()
    except requests.exceptions.HTTPError as e:
      logger.error(e.response.text)
      sys.exit(1)
    return imported_uid

def get_manifest(api_endpoint, cluster_uid, session):
    """print the imported cluster manifest"""
    logger.info("get the import manifest for cluster with id" + cluster_uid)
    try:
      imported_manifest = session.get(api_endpoint + "/v1/spectroclusters/" + cluster_uid + "/import/manifest")
      imported_manifest.raise_for_status()
    except requests.exceptions.HTTPError as e:
      logger.error(e.response.text)
      sys.exit(1)
    return(imported_manifest.text)

def setup_session(args):
    """set the required parameters to auth to the API"""
    session = requests.Session()
    session.headers.update({'ApiKey': args.api_key})
    session.headers.update({'ProjectUid': args.project_uid})
    return session

def get_cluster_uid(args, session):
    """look for clusters by name; if it exists, get the uid; if it doesn't exist, import it"""
    clusters = json.loads(get_clusters(args.api_endpoint, session).text)
    cluster_uid = None
    for cluster in clusters["items"]:
      if cluster["metadata"]["name"] == args.cluster_name[0]:
        logger.info("found existing cluster " + cluster["metadata"]["name"])
        # ignore deleted clusters
        if "deleted" in cluster["metadata"]["annotations"]:
          logger.info("ignoring deleted cluster " + cluster["metadata"]["name"])
          pass
        # stop if we find a cluster with our name
        else:
          logger.info("will get manifest for existing cluster " + cluster["metadata"]["name"] +
            " with id " + cluster["metadata"]["uid"])
          cluster_uid = cluster["metadata"]["uid"]
          break
    if cluster_uid == None:
      logger.info("no cluster found, doing import")
      cluster_uid = import_cluster(args.api_endpoint, args.cloud_type, args.cluster_name[0], session)
    return cluster_uid

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Name of the cluster to import
    parser.add_argument("cluster_name", help="name of the cluster to import", nargs=1)

    # Allow configuring API endpoint
    parser.add_argument("-a", "--api-endpoint", dest="api_endpoint", action="store", 
      default="https://api.spectrocloud.com", help="optionally configure the API endpoint location")

    # Project UID is a required parameter
    parser.add_argument("-u", "--project-uid", dest="project_uid", action="store", required=True,
      help="project UID - find in your Palette profile screen")

    # API key is a required parameter
    parser.add_argument("-k", "--api-key", dest="api_key", action="store", required=True,
      help="API key - find in your Palette profile screen")

    # Cloud type is a required parameter - cloud types map to API endpoints
    cloud_types=['aws','azure','edge-native','edge','gcp','generic','libvirt','maas','openstack','vsphere']
    parser.add_argument("-t", "--cloud-type", choices=cloud_types, action="store", required=True,
      help="set the cloud type to one of the supported options")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)

