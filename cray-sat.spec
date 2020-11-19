# Spec file for System Admin Toolkit (SAT)
# (C) Copyright 2019-2020 Hewlett Packard Enterprise Development LP.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
%define ansible_framework_dir /opt/cray/crayctl/ansible_framework
%define satmandir %{_mandir}/man8

Name: cray-sat
Version: %(./tools/changelog.py ./CHANGELOG.md)
Release: %(echo ${BUILD_METADATA})
License: MIT
Source: %{name}-%{version}.tar.gz
Summary: System Admin Toolkit (SAT)
Group: System/Management
BuildRoot: %{_topdir}
Vendor: Hewlett Packard Enterprise Company
Requires: slingshot-tools
Requires: python3-argcomplete
Requires: python3-python-dateutil >= 2.7.3, python3-python-dateutil < 3.0
Requires: python3-docker
Requires: python3-croniter >= 0.3, python3-croniter < 1.0
Requires: python3-inflect < 3.0
Requires: python3-kubernetes
Requires: python3-paramiko >= 2.4.2
Requires: python3-parsec
Requires: python3-PrettyTable >= 0.7.2, python3-PrettyTable < 1.0
Requires: python3-PyYAML
Requires: python3-requests < 3.0
Requires: python3-requests-oauthlib
Requires: python3-toml >= 0.10.0, python3-toml < 1.0
Requires: python3-urllib3 >= 1.0, python3-urllib3 < 2.0

%description
The System Admin Toolkit (SAT) is a command-line utility to perform various
diagnostic activities on a system including reporting on hardware
inventory, displaying the installed and running versions of software, and
displaying the status of the nodes in the system, among other things.

SAT was created to provide functionality similar to what was provided by the
xt-prefixed commands in the XC platform, such as xthwinv, xtshowrev,
xtcli, and others.

%package crayctldeploy
Summary: System Admin Toolkit (SAT) Deployment Ansible role
Requires: cray-crayctl

%description crayctldeploy
The Ansible role within the crayctl Ansible Framework that installs the System
Admin Toolkit (SAT).

%prep
%setup -n %{name}-%{version}

%build

# make man pages
python3 setup.py build
cd docs/man
make
cd -

# generate auto-completion script
mkdir -p etc/
register-python-argcomplete sat > etc/sat-completion.bash

%install
python3 setup.py install -O1 --root="$RPM_BUILD_ROOT" --record=INSTALLED_FILES \
                             --install-scripts=/usr/bin

# Install logging directory and config file
install -m 755 -d %{buildroot}/var/log/cray
install -m 755 -d %{buildroot}/etc

# This directory is used to hold the user-created site_info.yml
install -m 755 -d %{buildroot}/opt/cray/etc

# Holds state dumps gathered during shutdown.
install -m 755 -d %{buildroot}/var/sat/bootsys
# Holds pod state dumps gathered during shutdown.
install -m 755 -d %{buildroot}/var/sat/bootsys/pod-states

# Install ansible content for crayctldeploy subpackage
install -m 755 -d %{buildroot}/%{ansible_framework_dir}/roles
cp -r ansible/roles/cray_sat %{buildroot}/%{ansible_framework_dir}/roles/

# Install man pages
install -m 755 -d %{buildroot}%{satmandir}/
cp docs/man/*.8 %{buildroot}%{satmandir}/

# Install bash completion script
install -m 755 -d %{buildroot}/etc/bash_completion.d
install -m 644 etc/sat-completion.bash %{buildroot}/etc/bash_completion.d

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
%dir /var/log/cray
%dir /opt/cray/etc
%dir /var/sat/bootsys
%dir /var/sat/bootsys/pod-states
%{satmandir}/*.8.gz
/etc/bash_completion.d/sat-completion.bash

%files crayctldeploy
%{ansible_framework_dir}/roles/cray_sat
