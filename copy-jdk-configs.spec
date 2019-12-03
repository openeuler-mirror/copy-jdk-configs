%global pretrans_install %(cat %{SOURCE0} | sed s/%%/%%%%/g | sed s/\\^%%%%/^%%/g)
Name:      copy-jdk-configs
Version:   3.7
Release:   3
Summary:   JDKs Configuration File
License:   BSD
URL:       https://pagure.io/copy_jdk_configs
Source0:   %{URL}/blob/1d18ce8b5dec47a0468136ab6cdadfb93defe2c4/f/copy_jdk_configs.lua
Source1:   %{URL}/blob/1d18ce8b5dec47a0468136ab6cdadfb93defe2c4/f/LICENSE
Source2:   %{URL}/blob/1d18ce8b5dec47a0468136ab6cdadfb93defe2c4/f/copy_jdk_configs_fixFiles.sh
BuildArch: noarch
Requires:  lua lua-posix

%description
Utility script for transferring JDK configuration files when updating or
archiving. Repair rpmnew file created by error by using scrip

%prep
cp -a %{SOURCE1} .

%build
%pretrans -p <lua>
function createPretransScript()
  os.execute("mkdir -p %{_localstatedir}/lib/rpm-state")
  temp_path="%{_localstatedir}/lib/rpm-state/copy_jdk_configs.lua"
  file = io.open(temp_path, "w")
  file:write([[%{pretrans_install}]])
  file:close()
end

if pcall(createPretransScript) then
-- ok
else
--  print("Error running %{name} pretrans.")
end

%install
install -D %{SOURCE0} $RPM_BUILD_ROOT/%{_libexecdir}/copy_jdk_configs.lua
install -D %{SOURCE2} $RPM_BUILD_ROOT/%{_libexecdir}/copy_jdk_configs_fixFiles.sh

%posttrans
rm "%{rpm_state_dir}/copy_jdk_configs.lua" 2> /dev/null || :

%files
%{_libexecdir}/*
%license LICENSE

%changelog
* Thu Nov 28 2019 gulining<gulining1@huawei.com> - 3.7-3
- Pakcage init
