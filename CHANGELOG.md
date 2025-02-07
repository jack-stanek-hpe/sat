# Changelog

(C) Copyright 2020-2022 Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Added information regarding the `--bos-version` command line argument to man
  pages for relevant subcommands.
- Added a ``sat swap blade`` subcommand which partially automates the procedure
  for swapping compute and UAN blades.

### Changed
- Updated `sat bootsys` man page to reflect changes to stages and remove outdated information.

### Fixed
- Fixed unit tests that failed when run in PyCharm.

## [3.17.1] - 2022-07-05

### Changed
- Whenever `sat` is invoked, the permissions of the `~/.config/sat/sat.toml`
  file will be set to `0600`, and the permissions of the `~/.config/sat/tokens`
  and `~/.config/sat` directories will be set to `0700`.

### Fixed
- Fixed an issue where SAT crashed with a traceback if the file
  `/etc/opt/cray/site.yaml` existed but was empty. A warning message will now be
  logged instead.

## [3.17.0] - 2022-06-27

### Added
- Added client support for the BOS v2 API.
- Added a `--bos-version` command line option and `bos.api_version`
  configuration file option which can be used to specify which version of the
  BOS API to use.
- Added BOS v2 support to `sat bootprep`.
- Added BOS v2 support to `sat bootsys`.
- Added BOS v2 support to `sat status`, and added fields to `sat status` output
  listing the most recent BOS session, template, booted image, and boot status
  for nodes when BOS v2 is in use. Added a `--bos-fields` option to limit
  output to these fields.

### Fixed
- Fixed an issue causing `sat init` to not print a message when a new config was created.

### Removed
- Removed unused `docker` python package from requirements files.

### Changed
- Updated the project URL in `setup.py` to external GitHub location.
- Changed the format of the license and copyright text in all of the
  source files.

## [3.16.1] - 2022-06-07

### Fixed
- Fixed an issue in config-docker-sat.sh that was causing the builds to fail.

### Changed
- Changed builds to publish to the ``sat-docker`` Artifactory repository.

## [3.16.0] - 2022-05-31

### Changed
- Incremented the base version of Alpine used in the container image from 3.13
  to 3.15.
- Made changes related to the open sourcing of sat.
    - Update Jenkinsfile to use csm-shared-library.
    - Add Makefile for building container image.
    - Pull base container image from external location.
- Began using a separate ``cray_product_catalog`` package to query the product
  catalog in ``sat bootprep``.
- Began using a separate ``cray_product_catalog`` package to query the product
  catalog in ``sat showrev``.

### Fixed
- Fixed missing ``sat-hwhist`` man page.
- Fixed bug in ``sat status`` which caused a traceback when certain component
  state fields were missing in HSM.
- Fixed bug in ``sat status`` which caused a traceback when components were
  entirely missing from SLS.

## [3.15.1] - 2022-04-18

### Fixed
- Fixed tab completion in ``sat bash``.
- Fixed a bug with the ``$PATH`` environment variable not including the ``sat``
  executable in ``sat bash``.
- Fixed error reporting in ``sat firmware`` to treat responses containing the
  key "error" but an empty string for a value as non-errors.

## [3.15.0] - 2022-03-29

### Added
- Added a ``--bos-limit`` option to the  ``bos-operations`` stage of ``sat
  bootsys`` which passes the given limit string to the created BOS session.
  Also added a ``--recursive`` option to ``sat bootsys`` in order to allow
  specifying a slot or other higher-level component in the limit string.
- Added a ``--delete-ims-jobs`` option to ``sat bootprep run`` which causes
  successful IMS jobs to be deleted after ``sat bootprep`` is run. The default
  behavior was also changed to not delete jobs.
- Added information about nodes' CFS configuration status (desired
  configuration, configuration status, and error count) to ``sat status``.
- Added options to ``sat status`` to limit the output columns by specified
  CSM services. The added options are ``--hsm-fields``, ``--sls-fields``, and
  ``--cfs-fields``.
- Added a ``--bos-template`` option to ``sat status`` which allows the status
  report to be filtered by the specified session template's boot sets.

### Changed
- Changed the output of ``sat status`` to split different component types into
  different report tables.
- CFS image customization session container status logs in ``sat bootprep`` now
  automatically adjust space padding based on container name lengths.
- Added a stage to the Docker container build which runs ``pycodestyle`` on the
  SAT codebase and unit tests.

### Fixed
- Fixed ``sat bootprep`` to require the ``action`` positional argument.
- Fixed invalid reference to a FILES section in man page for ``sat bootprep``.

### Security
- Updated urllib3 dependency to version 1.26.5 to mitigate CVE-2021-33503, and
  refreshed Python dependency versions.

## [3.14.0] - 2022-02-24

### Added
- Added the ability to specify a commit hash in a product-based configuration
  layer in a ``sat bootprep`` input file.

### Changed
- The Dockerfile was reworked to leverage multistage builds and run unit tests
  in the same environment as the production container. The size of the container
  image has been cut in half as a result.
- Incremented the JSON Schema specification version for the ``sat bootprep``
  input file from draft-07 to 2020-12.
  in the same environment as the production container.

## [3.13.1] - 2022-01-26

### Added
- When ``--save-files`` is passed to ``sat bootprep``, BOS session template API
  request bodies will now be saved in addition to CFS configuration API request
  bodies.

### Fixed
- Improved ``sat bootprep`` to wait properly on CFS image configuration sessions
  to create the corresponding Kubernetes job before querying for pod status and
  to log helpful info messages when waiting on the job and pod.

## [3.13.0] - 2022-01-24

### Added
- Added a new subcommand, ``sat bootprep`` that automates creating CFS
  configurations, building and customizing IMS images, and creating BOS session
  templates which can be used to boot nodes in the system.

### Removed
- Removed password complexity checking from ``sat bmccreds`` due to incompatible
  open-source license.

## [3.12.1] - 2021-12-13

### Changed
- Bumped minor version to validate SAT after migration to internal HPE GitHub
  instance.

## [3.12.0] - 2021-12-07

### Changed
- Add a column to the output of ``sat showrev`` indicating when a product version
  is "active".

## [3.11.1] - 2021-11-22

### Changed
- Refactored `sat.apiclient` from a module into a subpackage.

## [3.11.0] - 2021-10-29

### Changed
- Added a ``--format`` option to ``sat xname2nid`` to set the output format
  to either 'range' or 'nid' for the node IDs.
- Added hostname information from SLS to `sat status` output.
- Added more information about unsuccessful API requests to the ``APIError``
  messages. This info is parsed from responses that use content type
  "application/problem+json" in their failure responses.

### Fixed
- Actions which wait on certain conditions (for example within ``sat bootsys``) will
  fail out more quickly when checking for the completion condition fails
  irrecoverably, instead of repeating a failing check until waiting times out.
- The ``ncn-power`` stage of ``sat bootsys`` will now only print one error
  message if ``impitool`` fails multiple times consecutively for a given
  component. If the number of failures for a given component exceeds 3, then
  that component will be marked as failed.
- Fixed the ``cabinet-power`` stage of ``sat bootsys`` to query CAPMC for power
  status of ComputeModules instead of the unsupported NodeBMC type.
- The ``cabinet-power`` stage of ``sat bootsys`` will now query CAPMC for chassis,
  compute modules, and router modules to power on or off individually instead of
  recursively in order to power on or off cabinets with disabled subcomponents.

## [3.10.0] - 2021-09-03

### Changed
- ``sat diag`` will now query HSM to verify that the components targeted for
  diagnostics are Rosetta switches.
- Changed sat to use the V2 HSM API.
- Changed ``sat xname2nid`` subcommand to translate slot, chassis, and cabinet
  xnames to node IDs in addition to node and node BMC xnames.

### Fixed
- Improved error handling of missing or empty FRUID key in system component data.
- The Ceph health timeout in the ``platform-services`` stage of ``sat bootsys boot``
  was changed to 60 seconds, from 600 seconds previously.
- If waiting for Ceph health to become "OK" times out during the ``platform-services``
  stage of ``sat bootsys boot``, the Ceph services will now be restarted on the
  storage nodes, and Ceph health will be waited on again.
- Fixed an error in the ``platform-services`` stage of ``sat bootsys boot``
  related to trying to start non-existent Ceph services.
- Fix a traceback that occurred if the user did not have permission to write to
  the log file.

### Added
- Added a check for running SDU sessions to the ``session-checks`` stage of a
  ``shutdown`` action in ``sat bootsys``.

### Security
- Incremented version of Alpine Linux from 3.13.2 to 3.13.5
  to address OpenSSL CVE-2021-3711.

## [3.9.0] - 2021-08-04

### Changed
- The ``--loglevel`` option is now an alias for the new ``--loglevel-stderr``.
- Remove the working directory ``/sat`` after the Docker container is built.
- Summaries generated by ``sat hwinv`` now have borders. Borders and headings may
  be toggled with ``--no-borders`` and ``--no-headings``.
- Changed the default logging level for stderr from "WARNING" to "INFO".
- Warn instead of rejecting on missing host keys in `sat bootsys` commands which
  use ssh to connect to other management NCNs.
- Disruptive shutdown stages in ``sat bootsys shutdown`` now prompt the user to
  continue before proceeding. A new option, ``--disruptive``, was added to
  bypass this when desired.
- Changed all informational print statements to be INFO level logging messages.

### Fixed
- Fixed a case where `sat xname2nid` and `sat nid2xname` failed when the input had
  extraneous whitespace.
- Fixed `--logfile` to accept a file name without leading directories.
- Fixed issues with filter error messages being printed twice or not being printed.
- Improved error messages when invalid filter syntax was supplied to
  refer to documentation of the syntax specification.
- Fixed an issue with specific field options not overriding `--fields` when listing
  components with `sat hwinv`.

### Added
- Added a ``--fields`` option to allow displaying only specific fields
  in subcommands which display a report.
- Added ``--loglevel-stderr`` and ``--loglevel-file`` to set logging level for
  stderr and log file separately.
- Added help and man page documentation on files that are absolute or relative
  paths in or below the home or current directory.
- Added prompt for whether user would like to continue when ``sat auth`` would
  overwrite an existing token.
- Added ``--excluded-ncns`` option to ``sat bootsys`` that can be used to omit
  NCNs from the platform-services and ncn-power stages in case they are
  inaccessible.
- Added support for ``--format json`` to print reports in JSON.
- Added support for the ``--filter``, ``--fields``, and ``--reverse`` options
  for summaries created by ``sat hwinv``.
- Added option to customize the default HTTP timeout length, both using the
  configuration file (with the ``api_gateway.api_timeout`` option) and with a new
  command line option, ``--api-timeout``.
- Added FRUID to output from ``sat hwinv``.
- Added a new ``sat hwhist`` subcommand to display hardware component history
  by xname (location) or by FRUID.

## [3.8.0] - 2021-06-23

### Changed
- When explicitly specifying a field using any ``--*-fields`` option with ``sat
  hwinv``, or when filtering against a field in any ``sat`` subcommand, those
  columns will now always be shown, even if all rows contain ``EMPTY`` or
  ``MISSING`` values.

### Fixed
- Fixed a case where filtering specific columns with any ``--*-fields`` option
  with ``sat hwinv`` failed when leading or trailing whitespace was present in
  the field name.
- Fixed the help text of `sat status` to list all available component types.
- Improved an error message which could sometimes occur when FAS reported a
  target with no xname.
- Fixed filtering so that the exact match of a column name used in the
  ``--filter`` query is always used instead of matching subsequences.
- Fixed filtering so that if there are multiple matches of column names
  using the ``--filter`` query, a WARNING is printed and the first match
  is used. This is consistent with ``--sort-by`` usage.
- Fixed filtering to handle spaces in column names by requiring them to
  be enclosed in double quotes.
- Changed warning message when filter returns no output to an error.

### Added
- Added power off of all non-management nodes in air-cooled cabinets
  to ``sat bootsys shutdown --stage cabinet-power``.
- Added a 'Subrole' column to the output of ``sat status``.
- Added ``sat bmccreds`` subcommand to provide a simple interface
  for setting BMC Redfish access credentials.
- Added ``sat slscheck`` subcommand to do a cross-check between SLS and HSM.
- Added confirmation message when ``sat setrev`` writes site info file to S3.

## [3.7.0] - 2021-05-13

### Changed
- Removed Redfish username and password from configuration file since
  they are no longer used by any subcommands.
- Changed the ``sat sensors`` command to use the Telemetry API to get
  sensor data instead of accessing Redfish directly.
- Changed the "unfreeze Ceph" step of the ``platform-services`` stage of
  ``sat bootsys boot`` to behave as follows:
  - Start any inactive Ceph services
  - Unfreeze Ceph
  - Wait for Ceph health
- Changed the ``platform-services`` stage of ``sat bootsys boot`` to prompt
  for confirmation of storage NCN hostnames in addition to Kubernetes managers
  and workers.

### Fixed
- Fixed a case where ``sat showrev`` fails when the Kubernetes configuration
  map ``cray-product-catalog`` is in an unexpected state.
- Improved error handling in ``sat showrev`` when connecting to the Kubernetes
  API fails.
- Added missing description of ``sat swap`` to output of ``sat --help``.
- Added back missing man pages to the container image.
- Removed an old ``slingshot-tools`` dependency from the RPM spec file.
  However, note that RPM installation has not been tested since the move to
  running ``sat`` in a container and is not officially supported.

### Added
- Added a new ``--update-until-timeout`` command-line option to ``sat sensors``.
- Added new fields to ``sat setrev`` and ``sat showrev``.
    - System description
    - Product number
    - Company name
    - Country code
- Added additional description of all fields when running ``sat setrev``,
  and added input validation for fields.
- Added a "Location Name" field to the listing of node accelerators output by
  `sat hwinv --list-node-accels`.

### Removed
- Removed the ``ceph-check`` stage of ``sat bootsys boot``.

## [3.6.0] - 2021-04-16

### Fixed
- Improved error handling in several cases of ``sat firmware``.
    - When multiple xnames and/or snapshots are given, a failure to query
      one of them will be logged as an error, but the valid snapshots
      and xnames will be printed.
    - If a given xname is not in a requested snapshot, a warning is logged.
    - If ``--snapshots`` is specified without arguments (to list all snapshot
      names) and xnames are provided on the command line, a warning is logged
      that the supplied xnames will be ignored.
    - If a given snapshot and/or xname combination yields no results,
      then the command will exit with an error.

### Changed
- Incremented version of Alpine Linux from 3.12.0 to 3.13.2.
- Changed the Ceph health check in ``sat bootsys boot --stage ceph-check``
  to be consistent with the check in the ``platform-services`` stage of
  ``sat bootsys boot`` and ``sat bootsys shutdown``.
- Changed the ``sat diag`` command to use the Fox API for launching controller
  diagnostics instead of accessing Redfish directly.

### Removed
- Removed Ansible and all of its dependencies from our container image by
  removing from our locked requirements files.
- Removed the ``cray-sat-crayctldeploy`` subpackage.
- Removed ``sat linkhealth`` which has been replaced by
  ``slingshot-topology-tool --cmd "show switch <ports,jacks> <switch xname>"``.
- Removed support for Firmware Update Service (FUS) in ``sat firmware``
  and ``sat bootsys shutdown --stage session-checks``. These commands now
  only use Firmware Action Service (FAS).

## [3.5.0] - 2021-03-24

### Added
- Added a new ``sat nid2xname`` subcommand to translate node IDs to node xnames.
- Added a new ``sat xname2nid`` subcommand to translate node and node BMC xnames
  to node IDs.

### Changed
- Changed ``sat swap`` to get all port policies when creating an offline port
  policy to check if the offline port policy already exists.
- Changed requirements files to ``requirements.txt`` and
  ``requirements-dev.txt``. Added ".lock" versions of these files and changed
  build process to use them, so that exact library versions are used.
- ``sat bootsys shutdown --stage bos-operations`` no longer forcefully powers
  off all compute nodes and application nodes using CAPMC when BOS sessions are
  complete or when it times out waiting for BOS sessions to complete.

### Fixed
- Addressed an error in ``sat bootsys``  when waiting for the ``hms-discovery``
  Kubernetes cronjob to be scheduled when there is no previous record of the
  job being scheduled.

## [3.4.0] - 2021-03-03

### Added
- Added a new ``--bos-templates`` command-line option and a ``bos_templates``
  configuration file option to ``sat bootsys boot|shutdown --stage bos-operations``.
  This is intended to replace ``--cle-bos-template``, ``--uan-bos-template``,
  and their respective configuration file options, ``cle_bos_template`` and
  ``uan_bos_template``.
- Added a confirmation message when generating a configuration file via
  ``sat init``.

### Changed
- ``--cle-bos-template`` and ``--uan-bos-template`` now no longer have defaults
  for ``sat bootsys boot|shutdown --stage bos-operations``. If a CLE or UAN
  session template is not specified then it will not be used for the boot or
  shutdown.
- Changed the default for s3.endpoint in ``sat.toml``
  from ``https://rgw-vip`` to ``https://rgw-vip.nmn``.
- Changed ``sat firmware`` to display both 'name' and 'targetName' fields from
  FAS, and changed the 'ID' header in the table to read 'name'.
- Improved step of ``sat bootsys shutdown --stage platform-services`` that stops
  containers by adding prompt whether to continue if stopping containers fails
  and added log messages about running and stopped containers.
- Improved console logging during `sat bootsys boot|shutdown --stage ncn-power`
  by adding a check for active screen sessions after they are created to account
  for the case when some other process like conman is holding the console.
- Changed info-level log messages to print statements for important messages
  about progress during the `ncn-power` stage of `sat bootsys`.

### Fixed
- Changed "BIS server" in SAT man page to "Kubernetes manager nodes", reworded
  description to discuss all of SAT's uses, and corrected several small typos
  in the SAT man page.
- Improved error handling in ``sat showrev`` when the cray-product-catalog
  Kubernetes configuration map does not exist, and when an invalid value is
  given for the S3 endpoint URL.
- Stopped printing a byte string of every container ID that was stopped during
  ``sat bootsys shutdown --stage platform-services`` when ``crictl stop``
  command times out.

## [3.3.0] - 2021-02-05

### Changed
- Changed method of getting hostnames of management non-compute nodes (NCNs) in
  ``sat bootsys`` from using Ansible groups to using the ``/etc/hosts`` file.
- Changed the platform services stage of ``sat bootsys shutdown`` to
  shut down containerd containers using crictl, and to stop the containerd
  service using ``systemctl``.
- Changed the platform services stage of ``sat bootsys shutdown`` to check
  health of the Ceph cluster and freeze the Ceph cluster before shutting down.
- Changed the platform services stage of ``sat bootsys boot`` to check
  health of the Ceph cluster and unfreeze the Ceph cluster before booting.
- Changed the platform services stage of ``sat bootsys boot`` to start
  containerd on the management NCNs and ensure it's enabled.
- Changed the platform services stage of ``sat bootsys shutdown`` to stop and
  disable kubelet on the Kubernetes management NCNs.
- Changed the platform services stage of ``sat bootsys boot`` to start and
  enable kubelet on the Kubernetes management NCNs.
- Changed the platform services stage of ``sat bootsys shutdown`` to save a
  snapshot of etcd and stop the etcd service on the manager Kubernetes NCNs.
- Changed the platform services stage of ``sat bootsys boot`` to ensure etcd is
  started and enabled on the manager Kubernetes NCNs.
- Changed ``sat swap switch`` to use the new Fabric Manager API.
- Changed the ``ncn-power`` stage of ``sat bootsys`` to no longer start and stop
  dhcpd, which is unnecessary now that NCNs and their management interfaces have
  statically assigned IP addresses.
- Changed the command prompt in ``sat bash`` to display 'sat-container' in
  addition to the container ID.
- Changed the ``ncn-power`` stage of ``sat bootsys`` to start console monitoring
  of NCNs using ``screen`` sessions launched over an SSH connection to ncn-m001
  instead of using ``ipmi_console_start.sh`` and ``ipmi_console_stop.sh``
  scripts.
- Changed the ``ncn-power`` stage of ``sat bootsys`` to exit with an error if it
  cannot start console monitoring prior to booting or shutting down NCNs.
- Changed ``sat linkhealth`` to correctly process status output from
  the Redfish API for newer versions of Rosetta switch firmware.
- Changed ``sat swap cable`` to use the new Fabric Manager API and Shasta p2p file.

### Removed
- Removed the ``hsn-bringup`` stage of ``sat bootsys boot`` due to removal of
  underlying Ansible playbook, ``ncmp_hsn_bringup.yaml``, and old fabric
  controller service.
- Removed call to ``ncmp_hsn_bringup.yaml`` Ansible playbook from currently
  unused ``HSNBringupWaiter`` class.
- Removed calls to removed Ansible playbooks ``enable-dns-conflict-hosts.yml``
  and ``disable-dns-conflict-hosts.yml`` during ``ncn-power`` stage of
  ``sat bootsys``.
- Removed the ``bgp-check`` stage of ``sat bootsys {boot,shutdown}`` due to
  removal of underlying Ansible playbook that implemented this stage.
- Removed ``run_ansible_playbook`` function from ``sat.cli.bootsys.util`` module
  since it is no longer used anywhere.
- Removed ``RunningService`` context manager since it is no longer used.

### Fixed
- Removed error message and 'ERROR' value for Slurm version in system
  table in ``sat showrev`` when Slurm is not present.
- Add missing space in help text for ``sat showrev`` ``--all`` option.

### Security
- Incremented required version of Python PyYAML package to 5.4.1.
- Incremented required version of Python RSA package to 4.7.

## [3.2.0] - 2020-12-17

### Changed
- Changed ``sat showrev`` to display product information from kuberetes
  configuration map. Previous product information is now accessible with
  the ``--release-files`` option.
- Changed ``sat showrev`` to display separate tables for system-wide
  information and host-local information. Added the ``--local`` option to
  ``sat showrev``.
- ``sat showrev`` will first read from ``/opt/cray/sat/etc/os-release``
  and from ``/etc/os-release`` if that does not exist for the SLES
  version.
- Modified output and logging of ``sat bootsys boot|shutdown --stage bos-operations``
  to include more information about the BOS session, BOA jobs and BOA pods.
- Changed ``sat swap`` to print an error message since the Fabric Controller API
  that is used is no longer available.

### Removed
- Removed Lustre and PBS versions from ``sat showrev``.
- Removed ``--packages`` and ``--docker`` options from ``sat showrev``.
- Removed package and docker image listing from output of
  ``sat showrev --all``.
- Removed ``sat cablecheck``.
- Removed ``slingshot-tools`` from the Docker image.

### Fixed
- Improved error handling in ``sat showrev --docker``.
- Fixed a missing comma in the ``sat`` man page.
- Added a space between sentences in S3 error logging in ``sat showrev``.

## [3.1.0] - 2020-12-04

### Added
- Ability to list node enclosure power supplies in ``sat hwinv`` with
  ``--list-node-enclosure-power-supplies``.
- Ability to list node accelerators (e.g. GPUs) in ``sat hwinv`` with
  ``--list-node-accels``.
- New field for accelerator counts when listing and summarizing nodes
  in ``sat hwinv``.
- Ability to list node accelerator risers (e.g. Redstone Modules)
  in ``sat hwinv`` with ``--list-node-accel-risers``.
- New field for accelerator riser counts when listing and summarizing nodes
  in ``sat hwinv``.
- Ability to list node HSN NICs in ``sat hwinv`` with ``--list-node-hsn-nics``.
- New field for HSN NIC counts when listing and summarizing nodes
  in ``sat hwinv``.

### Changed
- Changed ``sat bootsys`` state capture and hsn/k8s checks to use an S3
  bucket instead of local files.
- ``sat setrev`` now writes the site information file to S3, and
  ``sat showrev`` now downloads the site information file from S3.
- Changed default logging directory to ``/var/log/cray/sat/sat.log``.

### Removed
- Removed parsing of ``/etc/cray-release`` from ``sat showrev``.

### Fixed
- Fixed dumping of serial number in ``sat setrev`` so that it is always
  a string.

## [3.0.0] - 2020-11-18

### Added
- New ``sat init`` subcommand that generates a config file for the user at
  ``$HOME/.config/sat/sat.toml`` and populates it with defaults.
- ``Dockerfile`` to build a Docker image containing sat and its
  dependencies, including ipmitool, kubectl, and slingshot-tools.
- ``requirements.docker.txt`` that explicitly specifies the ``sat`` python
  package's dependencies and their versions that are installed in the Docker
  image.
- ``Jenkinsfile.docker`` that builds the Docker image in a DST pipeline.

### Changed
- Changed default location of configuration file from ``/etc/sat.toml`` to
  ``$HOME/.config/sat/sat.toml`` to more easily allow each user to have their
  own configuration file.
- Modified all ``sat`` commands to generate a config file at the new default
  location, ``$HOME/.config/sat/sat.toml``, if one does not exist yet.
- Renamed ``Jenkinsfile`` to ``Jenkinsfile.rpm`` to differentiate from the newly
  added ``Jenkinsfile.docker`` that builds the Docker image.
- Moved sat from the shasta-standard and shasta-premium product streams to the
  sat product stream.

### Fixed
- Updated Vendor tag in RPM spec file to HPE.
- Fixed RPM build failure in DST pipeline by removing `BuildRequires` tags that
  result in conflicting requirements installed in container used to build RPM.

### Security
- Incremented required version of python cryptography package from 3.1 to 3.2.

## [2.4.0] - 2020-10-08

### Added
- ``sat bootsys shutdown`` and ``sat bootsys boot`` have been split into stages
  which are specified with ``--stage``. Behavior of ``sat bootsys shutdown``
  without stage specified is to run the ``session-checks`` stage for backwards
  compatibility with the previous release.
- Stages added to ``sat bootsys shutdown`` to automate additional stages of the
  system shutdown procedure. Stages are as follows:
    - capture-state: captures state of HSN and k8s pods on the system.
    - session-checks: checks for active sessions in BOS, CFS, CRUS, FAS, and NMD
      services.
    - bos-operations: shuts down compute nodes and User Access Nodes (UANs)
      using BOS.
    - cabinet-power: shuts down power to the liquid-cooled compute cabinets in
      the system and suspends hms-discovery cronjob in k8s.
    - bgp-check: checks BGP peering sessions on spine switches and
      re-establishes if necessary.
    - platform-services: stops platform services running on management NCNs.
    - ncn-power: shuts down and powers off the management NCNs.
- Stages added to ``sat bootsys boot`` to automate additional stages of the
  system boot procedure. Stages are as follows:
    - ncn-power: powers on and boots managment NCNs.
    - platform-services: starts platform services on management NCNs.
    - k8s-check: waits for k8s pod health to reach state from before shutdown.
    - ceph-check: restarts ceph services and waits for them to be healthy.
    - bgp-check: checks BGP peering sessions on spine switches and
      re-establishes if necessary.
    - cabinet-power: resumes hms-discovery cronjob in k8s, waits for it to be
      scheduled, and then waits for chassis in liquid-cooled cabinets to be
      powered on.
    - hsn-bringup: brings up the HSN and waits for it be as healthy as it was
      before shutdown.
    - bos-operations: boots compute nodes and User Access Nodes (UANs) using
      BOS.
- Debug logging for every stage of `sat bootsys` operations including duration
  of each stage.
- Developer documentation in markdown format.
- Added ``sat swap`` subcommand for swapping cables and switches.  The
  existing functionality of ``sat switch`` is now duplicated under
  ``sat swap switch``, and ``sat switch`` is deprecated.  Changed
  exit codes of ``sat switch`` to align with ``sat swap``.

### Fixed
- Fixed missing values in info messages logged from sat.filtering module.
- Stopped using deprecated "cray" public client and started using new "shasta"
  public client for authentication.
- Respect configured stderr log level and stop emitting duplicate log messages
  to stderr.
- Fixed typos on ``sat linkhealth`` and ``sat status`` man pages.
- Added ``show_empty`` and ``show_missing`` FORMAT config file options to
  ``sat`` man page.
- Added sat-switch subcommand to ``sat`` man page.
- ``sat firmware`` now logs an error for unknown xnames.
- Fixed bug in flattening of list of NCN hostnames in the ``ncn-power`` stage of
  ``sat bootsys boot``.

## [2.3.0] - 2020-07-01

### Added
- Kubernetes pod state is dumped to a file during ``sat bootsys shutdown``.

### Fixed
- Fixed incorrect FAS URL used by ``sat firmware`` commands.
- Fixed minor bug in FAS error handling in ``sat firmware``.
- Stopped logging tokens when log level is set to debug.

## [2.2.0] - 2020-06-11

### Added
- FAS support for ``sat firmware``.
- Added ``sat bootsys`` subcommand and implemented first portion of the
  ``shutdown`` action.

### Changed
- Author in man pages now reads HPE.
- Split contributing guidelines to separate ``CONTRIBUTING.md`` file and added
  instructions for signing off on the Developer Certificate of Origin (DCO).

### Removed
- Removed Kibana objects, supporting scripts, and metadata from RPM. The
  ``sat`` command is not affected.

### Fixed
- Fixed two critical errors in ``sat showrev --system`` that resulted in an
  uncaught ``TypeError`` or ``IndexError``.
- ``sat k8s`` and ``sat showrev`` now catch ``FileNotFoundError`` that can be
  raised when loading kubernetes config.
- Suppressed ugly ``YAMLLoadWarning` that appeared when loading kubernetes
  config in ``sat k8s`` and ``sat showrev`` commands.

## [2.1.1] - 2020-06-03

### Changed
- ``sat hwmatch`` now displays a message if no mismatches were found.
- ``sat cablecheck`` now calls ``/usr/bin/check-hsn-cables`` which is the new
  name of the script after a slingshot-tools packaging refactor.

## [2.1.0] - 2020-05-26

### Added
- Extended Kibana dashboard for rasdaemon with panels that show just errors.
- Kibana dashboard to show heartbeat losses.
- New column showing ratio of co-located replicas to running pods for a given
  replicaset in output of ``sat k8s``.
- Support for exact field name matching using double quotes in ``sat hwinv``.

### Changed
- ``sat cablecheck`` now directly executes ``check_hsn_cables.py`` instead of
  calling with ``python2``.
- Changed "MISSING" values to "NOT APPLICABLE" when cable is not present in
  ``sat linkhealth``.

### Removed
- Removed "flow_control_config" field from ``sat linkhealth``. It is no longer
  present in Redfish, by design.

### Fixed
- Man page for ``sat diag`` updated to state explicitly what devices it can
  be applied to.
- Man page for ``sat showrev`` updated to describe the release directory and
  provide an example of products output.
- Restored certificate-nonvalidation warning circumvention from ``sat diag``,
  ``sat linkhealth``, and ``sat sensors``.

## [2.0.0] - 2020-05-06

### Added
- ``sat sensors`` supports ``--types`` for BMC types.
- ``sat sensors`` handles ``--xnames`` consistenty with ``sat linkhealth``.
- ``sat diag`` supports shared ``--redfish-username`` option.
- ``sat cablecheck`` supports ``check_hsn_cables.py``'s options.
- Ability to list drives in ``sat hwinv`` with ``--list-drives``.
- Ability to list CMM rectifiers in ``sat hwinv`` with ``--list-cmm-rectifiers``
- New fields for drive counts and total drive capacity when listing and
  summarizing nodes in ``sat hwinv``.
- New `--show-empty` and `--show-missing` options to allow override of default
  behavior to hide columns that are all EMPTY or MISSING.
- ``sat switch`` command for automation of switch enable/disable during
  switch replacement.
- ``sat k8s`` command which currently shows replica pods spun up on the
  same node.

### Changed
- Default behavior when printing tables is now to hide columns when values for
  those columns are either all EMPTY or all MISSING. The default behavior can be
  overridden using the `--show-empty` and `--show-missing` options.
- Man page of ``sat sensors`` revised to be more explicit with respect to
  supported BMC types and for style consistency.
- Errors in ``sat sensors`` changed to be less confusing. The xname is
  included in query errors and the "unable to identify" error is omitted
  if one of these errors is logged.
- Man page of ``sat diag`` revised to better cover interactive mode.
- Showrev will no longer exit at the first failure to retrieve a set of
  information. E.g., a failure to retrieve package version info will not impact
  showrev's ability to display system revision information.
- Improved sitefile handling by ``sat setrev`` to create directory and better
  detect and warn if file does not appear to be as expected.
- Included username in warning for failure to authenticate with token.
- Moved Redfish indication in user/password prompt to left side of colon.
- ``sat hwinv`` now reports memory in GiB rounded to 2 places.
- Changed project license from Cray Proprietary to MIT license and added notices
  to all source files.
- Implementation of ``processor_count`` property of ``Node`` objects now counts
  ``Processor`` objects instead of relying on 'LocationInfo' field in HSM.

### Removed
- Removed ``--substr`` option from ``sat showrev``, the effect of which can
  be accomplished using the general ``--filter`` option instead.
- Removed certificate-nonvalidation warning circumvention from ``sat diag``,
  ``sat linkhealth``, and ``sat sensors``. Occurrence of this warning is no
  longer normal behavior.

### Fixed
- Build version in ``sat showrev`` is now read from the ``/etc/cray-release``
  file and the field now reads "Release version".
- Slurm version now checked via pod.

## [1.3.0] - 2020-04-09

### Added
- Added ``Class`` to the fields reported by ``sat status``.
- ``--snapshots`` option for sat firmware.

### Changed
- Revised man pages for improved style and consistency.
- Changed ``sat linkhealth`` to display ``flow_control_config`` rather than
  ``flow_control_configuration`` as a column heading.
- Changed dependency from slingshot-cable-validation to slingshot-tools.

### Removed
- Removed unsupported ``--xname`` option from ``sat status`` man page.

## [1.2.0] - 2020-03-27

### Added
- Kibana dashboard for AER messages.
- Kibana dashboard for rasdaemon messages.

### Changed
- Kibana kernel dashboards to use DSL from KQL.
- Put list of subcommands in usage help in alphabetical order.
- All Kibana dashboards include time, hostname, message, and severity columns in
  the search output.

### Fixed
- The regular expression for the Kibana LBUG search query has been corrected.
- The output of firmware subcommand now properly sorts xnames by their numerical
  components.

## [1.1.2] - 2020-03-25

### Fixed
- Updated ``setup.py`` to not include our ``tools`` python package and
  subpackages of our ``tests`` package.

## [1.1.1] - 2020-03-20

### Changed
- Changed ``sat linkhealth`` to target switches contained by specifed xnames,
  for example xname component x1000c1 contains xname component x1000c1s2b0, as
  does x1000c1s2b0 (an xname component contains itself).

## [1.1.0] - 2020-03-18

### Added
- Kibana dashboards for kernel-related error messages.
- A kibana dasbhoard for viewing nodes set admindown and Application Task
  Orchestration and Management (ATOM) test failure log messages in the system
  monitoring framework.
- ``contains_component`` method added to ``XName`` class to test whether a
  component represented by an xname contains another.
- New ``--products`` option for ``sat showrev`` that shows information about
  installed product versions from ``/opt/cray/etc/release`` directory.

### Changed
- The xnames specified with the ``--xnames`` or ``--xname-file`` options are
  now made unique while preserving order.

### Fixed

- Fixed sorting by xname in output of ``sat status``.
- Made ``sat status`` more robust when keys are missing from data returned by
  HSM API.
- Fixed boolean operator precedence in filtering queries.
- Fixed exception that occurred in ``sat sensors`` when trying to split a list
  of xnames on commas or to iterate over None.
- Fixed ``sat showrev`` traceback that resulted from ``/opt/cray/etc/release``
  being changed from a file to a directory.

## [1.0.0] - 2020-02-27

This is the version at which we started properly maintaining our version
number.

### Added

- CHANGELOG.md in a simple markdown format.

## [0.0.3] - 2020-02-26

This is the version prior to the version at which we started properly maintaining
our version number.

### Added

- A sat command and all its subcommands, including sensors, firmware, diag,
  hwinv, cablecheck, setrev, auth, hwmatch, linkhealth, status, and showrev.
- A Jenkinsfile and spec file to build sat as an rpm.
- An Ansible role that installs sat within the crayctl ansible framework.
- A kibana dasbhoard for viewing MCE log messages in the system monitoring
  framework.
