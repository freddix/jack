Summary:	The JACK Audio Connection Kit
Name:		jack
Version:	1.9.9.5
Release:	1
License:	LGPL v2.1+ (libjack), GPL v2+ (the rest)
Group:		Daemons
#Source0:	http://www.grame.fr/~letz/jack-%{version}.tgz
Source0:	https://dl.dropbox.com/u/28869550/jack-1.9.9.5.tar.bz2
# Source0-md5:	6c9de6b89db9d7076fa2ce222816cf4c
# git clone  https://github.com/jackaudio/jack2
# git archive --format=tar --prefix=jack-1.9.9/ HEAD | xz -c > jack-1.9.9.tar.xz
#Source0:	%{name}-%{version}.tar.xz
Patch0:		%{name}-link.patch
URL:		http://jackit.sourceforge.net/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	doxygen
BuildRequires:	libcap-devel
BuildRequires:	libffado-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libtool
#BuildRequires:	opus-devel
BuildRequires:	pkg-config
BuildRequires:	readline-devel
Requires:	%{name}-libs = %{version}-%{release}
Provides:	jack-audio-connection-kit = %{version}-%{release}
Obsoletes:	jack-audio-connection-kit < %{version}-%{release}
Obsoletes:	jack-utils < %{version}-%{release}
Obsoletes:	jack-driver-firewire < %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*%{_bindir}/jackd
%define		_noautochrpath	.*%{_libdir}/jackd

%description
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (ie. as a
normal application), or can they can run within a JACK server (ie. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.

%package libs
Summary:	JACK library
License:	LGPL
Group:		Libraries
Provides:	jack-audio-connection-kit-libs = %{version}-%{release}
Obsoletes:	jack-audio-connection-kit-libs < %{version}-%{release}

%description libs
Shared JACK library.

%package devel
Summary:	Header files for JACK
License:	LGPL
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	jack-audio-connection-kit-devel = %{version}-%{release}
Obsoletes:	jack-audio-connection-kit-devel < %{version}-%{release}

%description devel
Header files for the JACK Audio Connection Kit.

%package apidocs
Summary:	JACK API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
JACK API documentation.

%prep
%setup -q
#%patch0 -p1

%build
LINKFLAGS="%{rpmcflags} %{rpmldflags}"	\
CXXFLAGS="%{rpmcxxflags} -I/usr/include/ncurses"	\
PREFIX="%{_prefix}"		\
./waf configure			\
	--alsa			\
	--classic		\
	--firewire		\
	--libdir=%{_libdir}	\
	--nocache

./waf build -v

%install
rm -rf $RPM_BUILD_ROOT

./waf install --destdir=$RPM_BUILD_ROOT

# waf workaround
chmod +x $RPM_BUILD_ROOT%{_libdir}/{lib*.so*,jack/*.so}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
# note: COPYING only specifies which parts fall under GPL and LGPL
%attr(755,root,root) %{_bindir}/jackd

%if 0
%attr(755,root,root) %{_bindir}/jackdbus
%{_datadir}/dbus-1/services/org.jackaudio.service
%endif

%dir %{_libdir}/jack
%attr(755,root,root) %{_libdir}/jack/audioadapter.so
%attr(755,root,root) %{_libdir}/jack/inprocess.so
%attr(755,root,root) %{_libdir}/jack/jack_alsa.so
%attr(755,root,root) %{_libdir}/jack/jack_alsarawmidi.so
%attr(755,root,root) %{_libdir}/jack/jack_dummy.so
%attr(755,root,root) %{_libdir}/jack/jack_firewire.so
%attr(755,root,root) %{_libdir}/jack/jack_loopback.so
%attr(755,root,root) %{_libdir}/jack/jack_net.so
%attr(755,root,root) %{_libdir}/jack/jack_netone.so
%attr(755,root,root) %{_libdir}/jack/netadapter.so
%attr(755,root,root) %{_libdir}/jack/netmanager.so
%attr(755,root,root) %{_libdir}/jack/profiler.so
%{_mandir}/man1/jackd.1*

# utils
%attr(755,root,root) %{_bindir}/alsa_in
%attr(755,root,root) %{_bindir}/alsa_out
%attr(755,root,root) %{_bindir}/jack_alias
%attr(755,root,root) %{_bindir}/jack_bufsize
%attr(755,root,root) %{_bindir}/jack_connect
%attr(755,root,root) %{_bindir}/jack_control
%attr(755,root,root) %{_bindir}/jack_cpu
%attr(755,root,root) %{_bindir}/jack_cpu_load
%attr(755,root,root) %{_bindir}/jack_disconnect
%attr(755,root,root) %{_bindir}/jack_evmon
%attr(755,root,root) %{_bindir}/jack_freewheel
%attr(755,root,root) %{_bindir}/jack_iodelay
%attr(755,root,root) %{_bindir}/jack_latent_client
%attr(755,root,root) %{_bindir}/jack_load
%attr(755,root,root) %{_bindir}/jack_lsp
%attr(755,root,root) %{_bindir}/jack_metro
%attr(755,root,root) %{_bindir}/jack_midi_dump
%attr(755,root,root) %{_bindir}/jack_midi_latency_test
%attr(755,root,root) %{_bindir}/jack_midiseq
%attr(755,root,root) %{_bindir}/jack_midisine
%attr(755,root,root) %{_bindir}/jack_monitor_client
%attr(755,root,root) %{_bindir}/jack_multiple_metro
%attr(755,root,root) %{_bindir}/jack_net_master
%attr(755,root,root) %{_bindir}/jack_net_slave
%attr(755,root,root) %{_bindir}/jack_netsource
%attr(755,root,root) %{_bindir}/jack_rec
%attr(755,root,root) %{_bindir}/jack_samplerate
%attr(755,root,root) %{_bindir}/jack_server_control
%attr(755,root,root) %{_bindir}/jack_session_notify
%attr(755,root,root) %{_bindir}/jack_showtime
%attr(755,root,root) %{_bindir}/jack_simple_client
%attr(755,root,root) %{_bindir}/jack_simple_session_client
%attr(755,root,root) %{_bindir}/jack_test
%attr(755,root,root) %{_bindir}/jack_thru
%attr(755,root,root) %{_bindir}/jack_transport
%attr(755,root,root) %{_bindir}/jack_unload
%attr(755,root,root) %{_bindir}/jack_wait
%attr(755,root,root) %{_bindir}/jack_zombie

%{_mandir}/man1/alsa_in.1*
%{_mandir}/man1/alsa_out.1
%{_mandir}/man1/jack_bufsize.1*
%{_mandir}/man1/jack_connect.1*
%{_mandir}/man1/jack_disconnect.1
%{_mandir}/man1/jack_freewheel.1*
%{_mandir}/man1/jack_impulse_grabber.1*
%{_mandir}/man1/jack_iodelay.1*
%{_mandir}/man1/jack_load.1*
%{_mandir}/man1/jack_lsp.1*
%{_mandir}/man1/jack_metro.1*
%{_mandir}/man1/jack_monitor_client.1*
%{_mandir}/man1/jack_netsource.1*
%{_mandir}/man1/jack_samplerate.1*
%{_mandir}/man1/jack_showtime.1*
%{_mandir}/man1/jack_simple_client.1*
%{_mandir}/man1/jack_transport.1*
%{_mandir}/man1/jack_unload.1*
%{_mandir}/man1/jack_wait.1*
%{_mandir}/man1/jackrec.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libjack*.so.?
%attr(755,root,root) %{_libdir}/libjack*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjack*.so
%{_includedir}/jack
%{_pkgconfigdir}/jack.pc

#%files apidocs
#%defattr(644,root,root,755)
#%{_gtkdocdir}/*

