Summary:	Home computer cron daemon
Summary(de):	Home computer cron daemon 
Summary(fr):	D�mon Home computer cron
Summary(pl):	Demon cron dla domowego komputera
Summary(tr):	Home computer cron s�reci, periyodik program �al��t�rma yetene�i
Name:		hc-cron
Version:	0.14
Release:	4
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	ftp://hc-cron.berlios.de/pub/hc-cron/stable/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	cron.logrotate
Source3:	%{name}.crontab
Source4:	crontab.1.pl
Source5:	cron.8.pl
Source6:	cron.sysconfig
Patch0:		%{name}-syscrondir.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-time.patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
Requires:	/bin/run-parts
Requires:	psmisc >= 20.1
Provides:	crontabs
Provides:	crondaemon
Obsoletes:	crondaemon
Obsoletes:	vixie-cron
Obsoletes:	crontabs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cron is a standard UNIX program that runs user-specified programs at
periodic scheduled times. hc-cron adds a number of features to the
basic UNIX cron, including better security and more powerful
configuration options.

%description -l de
cron ist ein Standard-UNIX-Programm, das zu vorgegebenen Zeiten vom
Benutzer angegebene Programme ausf�hrt. hc-cron weist mehr Funktionen
auf als cron aus UNIX, u.a. bessere Sicherheit und leistungsf�higere
Konfigurationsoptionen.

%description -l fr
cron est un des programmes UNIX standard qui permet � un utilisateur
donn� de lancer des p�riodiquement des programmes selon un ordre
planifi�. hc-cron ajoute de nombreuses fonctionnalit�s au cron UNIX de
base, dont une plus grande s�curit� et des options de configuration
plus puissantes.

%description -l pl
cron to standardowy uniksowy program, kt�ry okresowo uruchamia
okre�lone przez u�ytkownik�w programy. hc-cron dodaje mo�liwo�ci
podstawowemu uniksowemu cronowi, w tym lepsze bezpiecze�stwo i
bogatsze opcje konfiguracyjne.

%description -l tr
cron UNIX'de standart olarak belirli zamanlarda bir program�
�al��t�rmak i�in kullan�lan daemon'dur. hc-cron, standart cron'dan
daha g�venlidir ve daha geli�mi� yap�land�rma se�enekleri i�erir.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} OPTIM="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{cron.{hourly,daily,weekly,monthly},cron} \
$RPM_BUILD_ROOT%{_sysconfdir}/{cron.d,rc.d/init.d,logrotate.d,sysconfig} \
	$RPM_BUILD_ROOT%{_mandir}/{man{1,5,8},pl/man{1,8}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_bindir}} \
	$RPM_BUILD_ROOT/var/{spool/cron,log} 

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/pl/man1/crontab.1
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/pl/man8/cron.8

echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/man8/crond.8
echo ".so cron.8" > $RPM_BUILD_ROOT%{_mandir}/pl/man8/crond.8

echo "# Simple define users for cron" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
echo "root" > $RPM_BUILD_ROOT%{_sysconfdir}/cron/cron.allow
:> $RPM_BUILD_ROOT/var/log/cron

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/crond
install %{SOURCE2} $RPM_BUILD_ROOT/etc/logrotate.d/cron
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.d/system
install %{SOURCE6} $RPM_BUILD_ROOT/etc/sysconfig/cron

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add crond
if [ -f /var/lock/subsys/crond ]; then
	/etc/rc.d/init.d/crond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to start cron daemon."
fi
touch /var/log/cron
chmod 640 /var/log/cron

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/crond ]; then
		/etc/rc.d/init.d/crond stop >&2
	fi
	/sbin/chkconfig --del crond
fi

%triggerpostun -- vixie-cron
/sbin/chkconfig --add crond

%files
%defattr(644,root,root,755)

%attr(754,root,root) /etc/rc.d/init.d/crond

%attr(640,root,root) %config(noreplace) /etc/logrotate.d/*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*

%attr(750,root,root) %dir %{_sysconfdir}/cron.*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/cron/*
%attr(640,root,root) /etc/cron.d/*

%attr(0755,root,root) %{_sbindir}/crond
%attr(4711,root,root) %{_bindir}/crontab

%{_mandir}/man*/*
%lang(pl) %{_mandir}/pl/man*/*

%attr(750,root,root) %dir /var/spool/cron
%attr(640,root,root) %ghost /var/log/*
