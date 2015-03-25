%define __jar_repack %{nil}

%global username cassandra

%define relname apache-cassandra-%{version}

Name:           apache-cassandra11
Version:        %{version}
Release:        %{revision}
Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store.

Group:          Development/Libraries
License:        Apache Software License
URL:            http://cassandra.apache.org/
Source0:        http://www.ibiblio.org/pub/mirrors/apache/%{username}/%{version}/%{relname}-src.tar.gz
BuildRoot:      %{_tmppath}/%{relname}root-%(%{__id_u} -n)

BuildRequires: ant
BuildRequires: ant-nodeps

Conflicts:     cassandra
Obsoletes:     cassandra07
Obsoletes:     cassandra08
Conflicts:     apache-cassandra1

Requires:      java >= 1.6.0
Requires:      python(abi) >= 2.6
Requires(pre): user(cassandra)
Requires(pre): group(cassandra)
Requires(pre): shadow-utils
Provides:      user(cassandra)
Provides:      group(cassandra)

BuildArch:      noarch

# Don't examine the .so files we bundle for dependencies
AutoReqProv:   no

# Turn off the brp-python-bytecompile script, cause in RHEL 5 it only believes in python2.4.
# we'll byte-compile ourselves.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%description
Cassandra brings together the distributed systems technologies from Dynamo
and the data model from Google's BigTable. Like Dynamo, Cassandra is
eventually consistent. Like BigTable, Cassandra provides a ColumnFamily-based
data model richer than typical key/value systems.

For more information see http://cassandra.apache.org/

%prep
%setup -q -n %{relname}-src

%build
ant clean jar -Drelease=true
cd pylib && python2.6 setup.py build
cd pylib && python2.7 setup.py build

%install
%{__rm} -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/%{username}/
mkdir -p %{buildroot}/usr/share/%{username}
mkdir -p %{buildroot}/usr/share/%{username}/lib
mkdir -p %{buildroot}/usr/share/%{username}/default.conf
mkdir -p %{buildroot}/etc/%{username}/default.conf
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/security/limits.d/
mkdir -p %{buildroot}/etc/default/
mkdir -p %{buildroot}/usr/sbin
mkdir -p %{buildroot}/usr/bin
( cd pylib && python2.6 setup.py install -c -O1 --skip-build --root %{buildroot}; )
( cd pylib && python2.7 setup.py install -c -O1 --skip-build --root %{buildroot}; )
cp -p conf/* %{buildroot}/etc/%{username}/default.conf
cp -p conf/* %{buildroot}/usr/share/%{username}/default.conf
# step on default config with our redhat one
cp -p redhat/cassandra.in.sh %{buildroot}/etc/%{username}/default.conf
cp -p redhat/cassandra.in.sh %{buildroot}/usr/share/%{username}/default.conf
cp -p redhat/%{username} %{buildroot}/etc/rc.d/init.d/
cp -p redhat/%{username}.conf %{buildroot}/etc/security/limits.d/
cp -p redhat/default %{buildroot}/etc/default/%{username}
cp -pr lib/* %{buildroot}/usr/share/%{username}/lib
cp -p build/tools/lib/stress.jar %{buildroot}/usr/share/%{username}/lib
unzip -o redhat/snappy-java-1.0.4.1.jar.zip -d %{buildroot}/usr/share/%{username}/lib
unzip -o redhat/snappy-java-1.0.5.jar.zip -d %{buildroot}/usr/share/%{username}/lib
mv redhat/cassandra.in.sh %{buildroot}/usr/share/%{username}
mv bin/cassandra %{buildroot}/usr/sbin
rm bin/*.bat 
rm -rf bin/daemon
cp -p bin/* %{buildroot}/usr/bin
cp -p tools/bin/cassandra-stress %{buildroot}/usr/bin
cp -p tools/bin/token-generator %{buildroot}/usr/bin
rm %{buildroot}/usr/bin/cassandra.in.sh
# Handle the case of interim SNAPHOST builds
cp build/*cassandra*jar %{buildroot}/usr/share/%{username}/lib
mkdir -p %{buildroot}/var/lib/%{username}/commitlog
mkdir -p %{buildroot}/var/lib/%{username}/data
mkdir -p %{buildroot}/var/lib/%{username}/saved_caches
mkdir -p %{buildroot}/var/run/%{username}
mkdir -p %{buildroot}/var/log/%{username}

%clean
%{__rm} -rf %{buildroot}

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
useradd -d /usr/share/%{username} -g %{username} -M -r %{username}
exit 0

%files
%defattr(-,root,root,0755)
%doc CHANGES.txt LICENSE.txt README.txt NEWS.txt NOTICE.txt
%attr(755,root,root) %{_bindir}/cassandra-cli
%attr(755,root,root) %{_bindir}/cassandra-stress
%attr(755,root,root) %{_bindir}/cqlsh
%attr(755,root,root) %{_bindir}/json2sstable
%attr(755,root,root) %{_bindir}/nodetool
%attr(755,root,root) %{_bindir}/sstable2json
%attr(755,root,root) %{_bindir}/sstablekeys
%attr(755,root,root) %{_bindir}/sstableloader
%attr(755,root,root) %{_bindir}/sstablescrub
%attr(755,root,root) %{_bindir}/stop-server
%attr(755,root,root) %{_bindir}/token-generator
%attr(755,root,root) %{_sbindir}/cassandra
%attr(755,root,root) /etc/rc.d/init.d/%{username}
%attr(755,root,root) /etc/default/%{username}
%attr(755,root,root) /etc/security/limits.d/%{username}.conf
%attr(755,%{username},%{username}) /usr/share/%{username}*
%attr(755,%{username},%{username}) %config(noreplace) /%{_sysconfdir}/%{username}
%attr(755,%{username},%{username}) %config(noreplace) /var/lib/%{username}/*
%attr(755,%{username},%{username}) /var/log/%{username}*
%attr(755,%{username},%{username}) /var/run/%{username}*
/usr/lib/python2.6/site-packages/cqlshlib/
/usr/lib/python2.6/site-packages/cassandra_pylib*.egg-info
/usr/lib/python2.7/site-packages/cqlshlib/
/usr/lib/python2.7/site-packages/cassandra_pylib*.egg-info

%post
alternatives --install /etc/%{username}/conf %{username} /etc/%{username}/default.conf/ 0
# alternatives --install /etc/default/cassandra %{username} /etc/%{username}/default.conf/cassandra.default 0
cd /usr/share/cassandra/lib
grep "release 5" /etc/redhat-release > /dev/null 2> /dev/null
if [ $? -eq 0 ]; then
  # Put old snappy file in place for old Linux distros. Basically
  # rename the newer version out of the way.
  if [ -f snappy-java-1.0.5.jar ]; then
    if [ -f snappy-java-1.0.5.jar.backup ]; then
      %{__rm} -f snappy-java-1.0.5.jar.backup
    fi
    %{__mv} snappy-java-1.0.5.jar snappy-java-1.0.5.jar.backup
  fi
else
  # Move old version of snappy out of the way on modern Linux versions
  if [ -f snappy-java-1.0.5.jar ]; then
    if [ -f snappy-java-1.0.4.1.jar ]; then
      if [ -f snappy-java-1.0.4.1.jar.backup ]; then
        %{__rm} -f snappy-java-1.0.4.1.jar.backup
      fi
      %{__mv} snappy-java-1.0.4.1.jar snappy-java-1.0.4.1.jar.backup
    fi
  fi
fi
exit 0

%preun
# only delete alternative on removal, not upgrade
if [ "$1" = "0" ]; then
    alternatives --remove %{username} /etc/%{username}/default.conf/
fi
if [ "$1" = "0" ]; then
  # restore original snappy files so package management is happy on removal
  cd /usr/share/cassandra/lib
  if [ -f snappy-java-1.0.5.jar.backup ]; then
    if [ -f snappy-java-1.0.5.jar ]; then
      %{__rm} -f snappy-java-1.0.5.jar
    fi
    %{__mv} snappy-java-1.0.5.jar.backup snappy-java-1.0.5.jar
  fi
  if [ -f snappy-java-1.0.4.1.jar.backup ]; then
    if [ -f snappy-java-1.0.4.1.jar ]; then
      %{__rm} -f snappy-java-1.0.4.1.jar
    fi
    %{__mv} snappy-java-1.0.4.1.jar.backup snappy-java-1.0.4.1.jar
  fi
fi
exit 0

%changelog
* Wed Dec 15 2010 Nate McCall <nate@riptano.com> - 0.7.0-rc2
- Version numbering change
- Added macro definition for build paths
- Fix license declaration to use ASF
* Tue Aug 03 2010 Nick Bailey <nicholas.bailey@rackpace.com> - 0.7.0-1
- Updated to make configuration easier and changed package name.
* Mon Jul 05 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.3-1
- Initial package

