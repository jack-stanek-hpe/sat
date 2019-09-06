# Spec file for Shasta Admin Toolkit (SAT)
# Copyright 2019, Cray Inc. All Rights Reserved
%define ansible_framework_dir /opt/cray/crayctl/ansible_framework

Name: cray-sat
Version: 0.2.0
Release: %(echo ${BUILD_METADATA})
# TODO: Determine the correct license to use for SAT
License: Cray Proprietary
Source: %{name}-%{version}.tar.gz
Summary: Shasta Admin Toolkit (SAT)
Group: System/Management
BuildRoot: %{_topdir}
Vendor: Cray Inc.
Requires: python3-docker
Requires: python3-PrettyTable >= 0.7.2

%description
The Shasta Admin Toolkit (SAT) is a command-line utility to perform various
diagnostic activities on a Shasta system, including reporting on hardware
inventory, displaying the installed and running versions of software, and
displaying the status of the nodes in the system, among other things.

SAT was created to provide functionality similar to what was provided by the
xt-prefixed commands in the Cray XC platform, such as xthwinv, xtshowrev,
xtcli, and others.

%package crayctldeploy
Summary: Shasta Admin Toolkit (SAT) Deployment Ansible role
Requires: cray-crayctl

%description crayctldeploy
The Ansible role within the crayctl Ansible Framework that installs the Shasta
Admin Toolkit (SAT).

%prep
%setup -n %{name}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install -O1 --root="$RPM_BUILD_ROOT" --record=INSTALLED_FILES \
                             --install-scripts=/usr/bin

install -m 755 -d %{buildroot}/%{ansible_framework_dir}/roles
cp -r ansible/roles/cray_sat %{buildroot}/%{ansible_framework_dir}/roles/

# This is a hack taken from the DST-EXAMPLES / example-rpm-python repo to get
# the package directory, i.e. /usr/lib/python3.6/site-packages/sat which is not
# included in the INSTALLED_FILES list generated by setup.py.
# TODO: Replace this hack with something better, perhaps using %python_sitelib
cat INSTALLED_FILES | grep __pycache__ | xargs dirname | xargs dirname | uniq >> INSTALLED_FILES

# Our top-level `sat` script is currently installed by specifying our main
# function as an entry_point. Thus is it installed by `setup.py` above and
# listed in INSTALLED_FILES. If we change how that script is generated, we will
# need to manually install it here.

%files -f INSTALLED_FILES

%files crayctldeploy
%{ansible_framework_dir}/roles/cray_sat
