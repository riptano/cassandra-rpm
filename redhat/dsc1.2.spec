%global username cassandra

%define dscsrcname dsc-%{dscversion}-src
%define relname %{name}-%{version}
%define cass_name apache-cassandra-%{version}
%define __jar_repack %{nil}


Name:           dsc12
Version:        %{dscversion}
Release:        %{revision}
Summary:        Meta RPM for installation of the DataStax DSC platform

Group:          Development/Libraries
License:        ASL 2.0
URL:            http://www.datastax.com/products/community
Source0:        %{dscsrcname}.tar.gz
BuildRoot:      %{_tmppath}/%{relname}-root-%(%{__id_u} -n)

Requires:      cassandra12 = 1.2.5
Requires:      python(abi) >= 2.6
BuildArch:     noarch

%description
DataStax Community Edition is a free packaged distribution of the Apache
Cassandra database.

This package depends on the other components of DSC.

%prep

%build

%install

%clean

%files
