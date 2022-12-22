Import a cluster to Palette via API
Returns an import cluster manifest on stdout

setup: 

virtualenv .
. bin/activate
pip install -r requirements.txt

usage: palette_import_cluster.py [-h] [-a API_ENDPOINT] -u PROJECT_UID -k API_KEY -t {aws,azure,edge-native,edge,gcp,generic,libvirt,maas,openstack,vsphere} [-v] [--version] cluster_name

positional arguments:
  cluster_name          name of the cluster to import

options:
  -h, --help            show this help message and exit
  -a API_ENDPOINT, --api-endpoint API_ENDPOINT
                        optionally configure the API endpoint location
  -u PROJECT_UID, --project-uid PROJECT_UID
                        project UID - find in your Palette profile screen
  -k API_KEY, --api-key API_KEY
                        API key - find in your Palette profile screen
  -t {aws,azure,edge-native,edge,gcp,generic,libvirt,maas,openstack,vsphere}, --cloud-type {aws,azure,edge-native,edge,gcp,generic,libvirt,maas,openstack,vsphere}
                        set the cloud type to one of the supported options
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program's version number and exit

