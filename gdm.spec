%define libselinuxver 1.27.7
%define libauditver 1.0.6
%define pango_version 1.2.0
%define gtk2_version 2.6.0
%define libglade2_version 2.0.0
%define libgnomeui_version 2.2.0
%define libgnomecanvas_version 2.0.0
%define librsvg2_version 2.0.1
%define libxml2_version 2.4.21
%define scrollkeeper_version 0.3.4
%define pam_version 0.75
%define desktop_file_utils_version 0.2.90
%define gail_version 1.2.0

Summary: The GNOME Display Manager.
Name: gdm
Version: 2.8.0.4
Release: 10
Epoch: 1
License: LGPL/GPL
Group: User Interface/X
Source: ftp://ftp.gnome.org/pub/GNOME/sources/gdm-%{PACKAGE_VERSION}.tar.bz2
Source1: gdm-allow-login.init
Source2: gdm-early-login.init
Source3: zzz-bootup-complete.init
URL: ftp://ftp.gnome.org/pub/GNOME/sources/gdm/

Patch1: gdm-2.8.0.2-change-defaults.patch
Patch2: gdm-2.8.0.2-add-pam-timestamp-module.patch
Patch3: gdm-2.8.0.2-fix-selinux-check.patch
Patch4: gdm-2.8.0.2-session-errors-in-tmp.patch
Patch5: gdm-2.8.0.2-update-switchdesk-location.patch
Patch6: gdm-2.6.0.7-wait-for-bootup.patch
Patch7: gdm-2.8.0.2-clean-up-xsession-errors.patch
Patch8: gdm-2.8.0.2-merge-resources.patch
Patch9: gdm-2.6.0.8-boot-throbber.patch
Patch10: gdm-2.8.0.2-dont-malloc-in-signal-handlers.patch
Patch11: gdm-2.6.0.8-xdmcp.patch
Patch12: gdm-2.8.0.2-process-all-messages.patch
Patch13: gdm-2.8.0.2-prune-lang-list.patch
Patch14: gdm-2.8.0.2-hide-throbber.patch
Patch15: gdm-2.8.0.4-clean-up-leaks.patch
Patch16: gdm-2.8.0.4-audit-login.patch
Patch17: gdm-2.8.0.4-modularx.patch

BuildRoot: %{_tmppath}/gdm-%{PACKAGE_VERSION}-root

Prereq: /usr/sbin/useradd
Prereq: /usr/bin/scrollkeeper-update
Requires: gtk2 >= 0:%{gtk2_version}
Requires: libglade2 >= 0:%{libglade2_version}
Requires: libgnomeui >= 0:%{libgnomeui_version}
Requires: libgnomecanvas >= 0:%{libgnomecanvas_version}
Requires: librsvg2 >= 0:%{librsvg2_version}
Requires: libxml2 >= 0:%{libxml2_version}
Requires: pam >= 0:%{pam_version}
Requires: /etc/pam.d/system-auth
Requires: usermode
Requires: xorg-x11-xinit
Requires: xorg-x11-xdm
Requires: xsri >= 1:2.0.2
Requires: /sbin/nologin
Requires: redhat-artwork >= 0:0.129-3
Requires: /usr/share/desktop-menu-patches/gnome-gdmsetup.desktop
BuildRequires: scrollkeeper >= 0:%{scrollkeeper_version}
BuildRequires: pango-devel >= 0:%{pango_version}
BuildRequires: gtk2-devel >= 0:%{gtk2_version}
BuildRequires: libglade2-devel >= 0:%{libglade2_version}
BuildRequires: libgnomeui-devel >= 0:%{libgnomeui_version}
BuildRequires: libgnomecanvas-devel >= 0:%{libgnomecanvas_version}
BuildRequires: librsvg2-devel >= 0:%{librsvg2_version}
BuildRequires: libxml2-devel >= 0:%{libxml2_version}
BuildRequires: usermode
BuildRequires: pam-devel >= 0:%{pam_version}
BuildRequires: fontconfig
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
BuildRequires: gail-devel >= 0:%{gail_version}
BuildRequires: libgsf-devel
BuildRequires: libtool automake14 autoconf
BuildRequires: libcroco-devel
BuildRequires: libattr-devel
BuildRequires: gettext 
BuildRequires: libselinux-devel >= %{libselinuxver}
BuildRequires: audit-libs-devel >= %{libauditver}
Requires: libselinux >= %{libselinuxver}
Requires: audit-libs >= %{libauditver}

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%prep
%setup -q

%patch1 -p1 -b .change-defaults
%patch2 -p1 -b .add-pam-timestamp-module
%patch3 -p1 -b .fix-selinux-check
%patch4 -p1 -b .session-errors-in-tmp
%patch5 -p1 -b .update-switchdesk-location
##%patch6 -p1 -b .wait-for-bootup
%patch7 -p1 -b .clean-up-xsession-errors
%patch8 -p1 -b .merge-resources
#%patch9 -p1 -b .boot-throbber
%patch10 -p1 -b .dont-malloc-in-signal-handlers
#%patch11 -p1 -b .xdmcp
%patch12 -p1 -b .process-all-messages
%patch13 -p1 -b .prune-lang-list
%patch14 -p1 -b .hide-throbber
%patch15 -p1 -b .clean-up-leaks
%patch16 -p1 -b .audit-login
%patch17 -p1 -b .modularx

# fix the time format for ja
perl -pi -e "s|^msgstr \"%a %b %d, %H:%M\"|msgstr \"%m/%d \(%a\) %H:%M\"|; s|^msgstr \"%a %b %d, %I:%M %p\"|msgstr \"%m/%d \(%a\) %p %I:%M\"|" po/ja.po

%build
intltoolize --force --copy
aclocal-1.4
libtoolize --force --copy
automake-1.4 --add-missing
autoconf
autoheader
%configure --prefix=%{_prefix} --sysconfdir=/etc/X11 --with-pam-prefix=/etc --localstatedir=/var --enable-console-helper --disable-scrollkeeper \
--with-selinux
make

%install
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/X11/gdm/Init
mkdir -p $RPM_BUILD_ROOT/etc/X11/gdm/PreSession
mkdir -p $RPM_BUILD_ROOT/etc/X11/gdm/PostSession

make install DESTDIR=$RPM_BUILD_ROOT

# docs go elsewhere
rm -rf $RPM_BUILD_ROOT/%{prefix}/doc

# change default Init script for :0 to be Red Hat default
# XXX: hack, these shouldn't be in libdir -- #173081
(cd $RPM_BUILD_ROOT/etc/X11/gdm/Init; ln -sf ../../../../%{_libdir}/X11/xdm/Xsetup_0 :0)

# create log dir
mkdir -p $RPM_BUILD_ROOT/var/log/gdm

# remove the gdm Xsession as we're using the xdm one
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/gdm/Xsession

rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

# remove the gnome session file, since we don't use it anymore
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/X11/dm/Sessions/gnome.desktop

# remove the other gnome session file, since we put it in gnome-session
rm -rf $RPM_BUILD_ROOT%{_datadir}/xsessions

# no dumb flexiserver thing, Xnest is too broken
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/gdmflexiserver-xnest.desktop

# use patched gdmsetup desktop file
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/gdmsetup.desktop
(cd $RPM_BUILD_ROOT%{_datadir}/applications; ln -sf ../desktop-menu-patches/gnome-gdmsetup.desktop .)

# fix the "login photo" file
desktop-file-install --vendor gnome --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  $RPM_BUILD_ROOT%{_datadir}/applications/gdmphotosetup.desktop

rm -f $RPM_BUILD_ROOT%{_datadir}/applications/gdmflexiserver.destkop

# broken install-data-local in gui/Makefile.am makes this necessary
(cd $RPM_BUILD_ROOT%{_bindir} && ln -sf gdmXnestchooser gdmXnest)

rm -rf $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
install -m755 ${RPM_SOURCE_DIR}/gdm-early-login.init                          \
              ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gdm-early-login
install -m755 ${RPM_SOURCE_DIR}/gdm-allow-login.init                          \
              ${RPM_BUILD_ROOT}/etc/rc.d/init.d/gdm-allow-login
install -m755 ${RPM_SOURCE_DIR}/zzz-bootup-complete.init                      \
              ${RPM_BUILD_ROOT}/etc/rc.d/init.d/zzz-bootup-complete

%find_lang gdm

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/useradd -M -u 42 -d /var/gdm -s /sbin/nologin -r gdm > /dev/null 2>&1
/usr/sbin/usermod -d /var/gdm -s /sbin/nologin gdm >/dev/null 2>&1
# ignore errors, as we can't disambiguate between gdm already existed
# and couldn't create account with the current adduser.
exit 0

%post
/sbin/ldconfig
scrollkeeper-update
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

# Attempt to restart GDM softly by use of the fifo.  Wont work on older
# then 2.2.3.1 versions but should work nicely on later upgrades.
# FIXME: this is just way too complex
FIFOFILE=`grep '^ServAuthDir=' %{_sysconfdir}/X11/gdm/gdm.conf | sed -e 's/^ServAuthDir=//'`
if test x$FIFOFILE = x ; then
	FIFOFILE=%{_localstatedir}/gdm/.gdmfifo
else
	FIFOFILE="$FIFOFILE"/.gdmfifo
fi
PIDFILE=`grep '^PidFile=' %{_sysconfdir}/X11/gdm/gdm.conf | sed -e 's/^PidFile=//'`
if test x$PIDFILE = x ; then
	PIDFILE=/var/run/gdm.pid
fi
if test -w $FIFOFILE && test -f $PIDFILE && kill -0 `cat $PIDFILE` 2>/dev/null ; then
	(echo;echo SOFT_RESTART) >> $FIFOFILE
fi
# ignore error in the above
exit 0

%postun
/sbin/ldconfig
scrollkeeper-update
touch --no-create %{_datadir}/icons/hicolor
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  gtk-update-icon-cache -q %{_datadir}/icons/hicolor
fi

%files -f gdm.lang
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README TODO

%dir /etc/X11/gdm
%config(noreplace) /etc/X11/gdm/gdm.conf
/etc/X11/gdm/factory-gdm.conf
%config /etc/X11/gdm/XKeepsCrashing
%config /etc/X11/gdm/locale.alias
%config /etc/X11/gdm/Init/*
%config /etc/X11/gdm/PostLogin/*
%config /etc/X11/gdm/PreSession/*
%config /etc/X11/gdm/PostSession/*
%config /etc/X11/gdm/modules/*
%config /etc/pam.d/gdm
%config /etc/pam.d/gdmsetup
%config /etc/pam.d/gdm-autologin
%config /etc/security/console.apps/gdmsetup
%config /etc/rc.d/init.d/*
%dir /etc/X11/gdm/Init
%dir /etc/X11/gdm/PreSession
%dir /etc/X11/gdm/PostSession
%dir /etc/X11/gdm/PostLogin
%dir /etc/X11/gdm/modules
%{_datadir}/pixmaps
%{_datadir}/icons
%{_datadir}/gdm
%{_datadir}/applications
%{_datadir}/gnome/help/gdm
%{_datadir}/omf/gdm
%{_libdir}/gtk-2.0/modules/*.so
%{_bindir}/*
%{_libexecdir}/*
%{_mandir}/man*/*
%{_sbindir}/*
%dir %{_localstatedir}/log/gdm


%attr(1770, root, gdm) %dir %{_localstatedir}/gdm

%changelog
* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> - 1:2.8.0.4-10
- also fix default xsession for where its moved in modular X

* Sun Nov 13 2005 Jeremy Katz <katzj@redhat.com> - 1:2.8.0.4-9
- change requirements for modular X
- patch to find x server with modular X

* Thu Oct 20 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.4-8
- redhat-artwork was busted, require new version

* Tue Oct 18 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.4-7
- zero-initialize message buffer,
  bug fixed by Josh Parson (jbparsons@usdavis.edu) (bug 160603)
- fix typo in redhat-artwork requires line

* Mon Oct 17 2005 Steve Grubb <sgrubb@redhat.com> 1:2.8.0.4-6
- add login audit patch (bug 170569)

* Mon Oct 17 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.4-5
- bump redhat-artwork requirement to get rid of the boot
  throbber for now, since it seems to have reappeared
  mysteriously (bug 171025)

* Thu Oct 13 2005 Dan Walsh <dwalsh@redhat.com> 1:2.8.0.4-4
- Change to use getseuserbyname

* Thu Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1:2.8.0.4-3
- Fix selinux not to fail when in permissive mode

* Thu Sep 27 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.4-2
- remove flexiserver from menus

* Thu Sep  8 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.4-1
- update to 2.8.0.4

* Tue Sep  6 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.2-4
- Apply clean up patch from Steve Grubb (gnome bug 315388).

* Tue Aug 30 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.2-3
- Prune language list of installed languages
- Make config file noreplace again (bug 167087).

* Sat Aug 20 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.2-2
- hide throbber

* Fri Aug 19 2005 Ray Strode <rstrode@redhat.com> 1:2.8.0.2-1
- update to 2.8.0.2
- disable early login stuff temporarily

* Thu Aug 18 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-18
- rebuild

* Wed Aug 10 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-17
- Prune uninstalled languages from language list.

* Mon May 23 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-16
- Make sure username/password incorrect message gets displayed
  (bug 158127).
- reread system locale before starting gdm in early login mode 
  (bug 158376).

* Thu May 19 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-15
- Take out some syslog spew (bug 157711).

* Thu May 12 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-14
- Fix processing of new-line characters that got broken
  in 2.6.0.8-11 (bug 157442).

* Tue May  3 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-12
- Fix processing of non-ascii characters that got broken
  in 2.6.0.8-11, found by Miloslav Trmac <mitr@redhat.com>,
  (bug 156590).

* Thu Apr 28 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-11
- Fix halt command (bug 156299)
- Process all messages sent to the greeter in a read, not just
  the first

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 1:2.6.0.8-10
- silence %%postun

* Tue Apr 26 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-9
- Change default standard greeter theme to clearlooks and 
  default graphical greeter theme to Bluecurve specifically.

- Change default path values (bug 154280)

* Mon Apr 25 2005 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.8-8
- for early-login, delay XDMCP initialization until allow-login

* Sun Apr 24 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-7
- calling gdm_debug and g_strdup_printf from signal handlers are
  bad news (Spotted by Mark McLoughlin <markmc@redhat.com>).

* Tue Apr 19 2005 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.8-6
- Add a throbber for early login

* Mon Apr 18 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-5
- Don't install gnome.desktop to /usr/share/xsessions (bug 145791)

* Thu Apr 14 2005 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.8-4
- Don't do early-login if firstboot is going to run
- Make early-login work with timed and automatic logins

* Wed Apr 13 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-3
- Don't hard code dpi setting to 96.0, but instead look at
  Xft.dpi

* Wed Apr 13 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-2
- touch /var/lock/subsys/gdm-early-login so gdm gets killed on
  runlevel changes (bug 154414)
- don't try to use system dpi settings for canvas text (bug 127532)
- merge resource database from displays other than :0

* Sat Apr  2 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.8-1
- update to 2.6.0.8
- add new init scripts to support early-login mode

* Tue Mar 29 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.7-8
- Add a --wait-for-bootup cmdline option.

* Mon Mar 28 2005 Christopher Aillon <caillon@redhat.com>
- rebuilt

* Fri Mar 25 2005 Christopher Aillon <caillon@redhat.com> 1:2.6.0.7-6
- Update the GTK+ theme icon cache on (un)install

* Fri Mar 11 2005 Alexandre Oliva <aoliva@redhat.com> 1:2.6.0.7-5
- fix patch for bug 149899 (fixes bug 150745)

* Wed Mar 09 2005 Than Ngo <than@redhat.com> 1:2.6.0.7-4
- add OnlyShowIn=GNOME;

* Mon Feb 28 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.7-3
- seteuid/egid as user before testing for presence of
  user's home directory (fixes bug 149899)

* Thu Feb 10 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.7-2
- Turn off "switchdesk" mode by default which accidentally got 
  turned on by default in 2.6.0.5-4

* Wed Feb  2 2005 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.7-1
- Update to 2.6.0.7

* Tue Jan 25 2005 Ray Strode <rstrode@redhat.com> 1:2.6.0.5-11
- Fix bug in greeter sort-session-list patch where selecting
  a session did nothing (bug 145626)

* Thu Dec 9 2004 Dan Walsh <dwalsh@redhat.com> 1:2.6.0.5-10
- Remove pam_selinux from gdmsetup pam file

* Wed Dec  1 2004  Ray Strode  <rstrode@redhat.com> 1:2.6.0.5-9 
- Look up and use username instead of assuming that user entered 
  login is cannonical.  Patch from
  Mike Patnode <mike.patnode@centrify.com> (fixes bug 141380).

* Thu Nov 11 2004  Ray Strode  <rstrode@redhat.com> 1:2.6.0.5-8 
- Sort session list so that default session comes out on top
  (fixes bug 107324)

* Wed Nov 10 2004  Ray Strode  <rstrode@redhat.com> 1:2.6.0.5-7 
- Make desktop file symlink instead of absolute (bug 104390)
- Add flexiserver back to menus

* Wed Oct 20 2004  Ray Strode  <rstrode@redhat.com> 1:2.6.0.5-6 
- Clean up xses if the session was successfullly completed.
  (fixes bug #136382)

* Tue Oct 19 2004  Ray Strode  <rstrode@redhat.com> 1:2.6.0.5-5 
- Prefer nb_NO over no_NO for Norwegian (fixes bug #136033)

* Thu Oct  7 2004 Alexander Larsson <alexl@redhat.com> - 1:2.6.0.5-4
- Change default greeter theme to "Default", require 
  redhat-artwork with Default symlink.

* Wed Sep 29 2004 Ray Strode <rstrode@redhat.com> 1:2.6.0.5-3
- Check if there is a selected node before using iterator.
  (fixes bug #133329).

* Fri Sep 24 2004 Ray Strode <rstrode@redhat.com> 1:2.6.0.5-2
- Don't mess with gdmphotosetup categories.  Upstream categories
  are fine.

* Mon Sep 20 2004 Ray Strode <rstrode@redhat.com> 1:2.6.0.5-1
- update to 2.6.0.5

* Tue Aug 3 2004 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.3-5
- fix messed up changelog

* Tue Aug 3 2004 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.3-4
- rebuilt

* Thu Aug 2 2004 Ray Strode <rstrode@redhat.com> 1:2.6.0.3-3
- rebuilt

* Mon Jul 26 2004 Bill Nottingham <notting@redhat.com> 1:2.6.0.3-2
- fix theme (#128599)

* Thu Jun 17 2004 Ray Strode <rstrode@redhat.com> 1:2.6.0.3-1
- update to 2.6.0.3 (fixes bug #117677)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 1:2.6.0.0-5
- rebuild

* Mon May 17 2004 Than Ngo <than@redhat.com> 1:2.6.0.0-4
- add patch to build gdm-binary with PIE

* Thu Apr 22 2004 Mark McLoughlin <markmc@redhat.com> - 1:2.6.0.0-3
- Update the "use switchdesk" message to only be display when
  switchdesk-gui is installed and to not reference a non existant
  menu item (bug #121460)

* Fri Apr  2 2004 Colin Walters <walters@redhat.com> 1:2.6.0.0-2
- Always put session errors in /tmp, in preparation for
  completely preventing gdm from writing to /home/

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 1:2.6.0.0-1
- update to 2.6.0.0

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 1:2.5.90.3-1
- Use selinux patch again

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 1:2.5.90.3-1
- Stop using selinux patch and use pam_selinux instead.

* Wed Mar 10 2004 Alex Larsson <alexl@redhat.com> 1:2.5.90.2-1
- update to 2.5.90.2

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Alexander Larsson <alexl@redhat.com> 1:2.5.90.1-1
- update to 2.5.90.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 03 2004 Warren Togami <wtogami@redhat.com> 1:2.4.4.5-9
- add two lines to match upstream CVS to xdmcp_sessions.patch
  Fully resolves #110315 and #113154

* Sun Feb 01 2004 Warren Togami <wtogami@redhat.com> 1:2.4.4.5-8
- patch30 xdmcp_session counter fix from gdm-2.5.90.0 #110315
- automake14 really needed, not automake
- BR libcroco-devel, libcroco-devel, libattr-devel, gettext
- conditionally BR libselinux-devel
- explicit epoch in all deps
- make the ja.po time format change with a sed expression rather than
  overwriting the whole file (Petersen #113995)

* Thu Jan 29 2004 Jeremy Katz <katzj@redhat.com> - 1:2.4.4.5-7
- fix build with current auto*

* Tue Jan 27 2004 Jeremy Katz <katzj@redhat.com> 1:2.4.4.5-5
- try a simple rebuild for libcroco abi change

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.5-4
- Fix call to is_selinux_enabled

* Fri Jan 16 2004 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.5-3
- Use /sbin/reboot and /sbin/poweroff instead of consolehelper version

* Thu Oct 30 2003 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.5-2.sel
- turn on SELinux

* Mon Oct 20 2003 Jonathan Blandford <jrb@redhat.com> 2:2.4.4.5-1
- get rid of the teal

* Fri Oct 17 2003 Jonathan Blandford <jrb@redhat.com> 1:2.4.4.5-1
- new version

* Thu Oct  9 2003 Jonathan Blandford <jrb@redhat.com> 1:2.4.4.3-6.sel
- new patch from George to fix #106189
- change bg color in rhdefaults patch
- turn off SELinux

* Thu Oct 8 2003 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.3-6.sel
- turn on SELinux

* Tue Oct  7 2003 Alexander Larsson <alexl@redhat.com> 1:2.4.4.3-5
- Fix greeter line-breaking crash (rest of #106189)

* Tue Oct  7 2003 Alexander Larsson <alexl@redhat.com> 1:2.4.4.3-4
- Set the BaseXSession properly in the config.
- This fixes parts of bug #106189

* Mon Oct  6 2003 Havoc Pennington <hp@redhat.com> 1:2.4.4.3-3
- change DefaultSession=Default.desktop to DefaultSession=default.desktop
- SELinux off again

* Fri Oct 3 2003 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.3-2.sel
- turn on SELinux

* Thu Oct  2 2003 Havoc Pennington <hp@redhat.com> 1:2.4.4.3-1
- 2.4.4.3
- --without-selinux for now, since libselinux not in the buildroot

* Mon Sep 8 2003 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.0-4
- turn off SELinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1:2.4.4.0-3.sel
- turn on SELinux

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 1:2.4.4.0-2
- Use the right default session (#103546)

* Wed Sep  3 2003 Alexander Larsson <alexl@redhat.com> 1:2.4.4.0-1
- update to 2.4.4.0
- update to georges new selinux patch

* Fri Aug 29 2003 Elliot Lee <sopwith@redhat.com> 1:2.4.2.102-2
- Remove scrollkeeper files

* Tue Aug 26 2003 George Lebl <jirka@5z.com> 1:2.4.2.102-1
- updated to 2.4.2.102
- removed outdated patches
- Use Xsetup_0 only for :0 since that's the way it works
  for xdm
- remove the gnome.desktop file, its going into gnome-session

* Thu Aug 14 2003 Havoc Pennington <hp@redhat.com> 1:2.4.1.6-1
- update to latest bugfix version on george's advice
- remove setlocale patch that's upstream
- remove console setup patches that are upstream

* Thu Jun 12 2003 Dan Walsh <dwalsh@redhat.com> 2.4.1.3-9
- Port to SELinux

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix post: localstatedir -> _localstatedir

* Thu May  1 2003 Havoc Pennington <hp@redhat.com> 1:2.4.1.3-6
- enable UTF-8 for CJK

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Owen Taylor <otaylor@redhat.com>
- Run the error dialogs under /bin/sh --login, so we
  get lang.sh, and thus unicode_start running. Fixes
  the X-doesn't-start dialog showing up as random
  blinking characters.

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 1:2.4.1.3-2
- nuke buildreq Xft

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 1:2.4.1.3-1
- upgrade to 2.4.1.3

* Mon Feb  3 2003 Matt Wilson <msw@redhat.com> 1:2.4.1.1-6
- added gdm-2.4.1.1-64bit.patch to fix 64 bit crash in cookie
  generation (#83334)

* Mon Feb  3 2003 Owen Taylor <otaylor@redhat.com>
- Add patch to fix problem where setting LC_COLLATE=C would give LC_MESSAGES=wa_BE (#82019)

* Thu Jan 30 2003 Matt Wilson <msw@redhat.com> 1:2.4.1.1-3
- fix pam.d entry, pam_env wasn't properly patched
- disable optimizations on x86_64 to work around gcc bug

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 20 2003 Owen Taylor <otaylor@redhat.com>
- Upgrade to 2.4.1.1 (Fixes #81907)
- Redirect stdout of kill to /dev/null (#80814)

* Thu Jan  9 2003 Havoc Pennington <hp@redhat.com>
- 2.4.1.0
- add patch from george to ask "are you sure?" for shutdown/reboot since it's now just one click away

* Thu Dec 19 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0.12
- update new patch for no-utf8-in-cjk
- drop patch to photo setup, now upstream
- drop confdocs patch now upstream
- move all the gdm.conf changes into single "rhconfig" patch
- remove "sid-fix" patch now upstream

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.0.7-14
- remove the directory part of module specifications from the PAM config files,
  allowing the same PAM config to work for either arch on multilib boxes

* Thu Sep  5 2002 Owen Taylor <otaylor@redhat.com>
- Change zh_CN entry in language menu to zh_CN.GB18030

* Thu Sep  5 2002 Akira TAGOH <tagoh@redhat.com> 2.4.0.7-12
- copied gdm-ja.po to ja.po.

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem where gdm was opening ~/.xsession-errors itself to bad effect

* Sat Aug 31 2002 Havoc Pennington <hp@redhat.com>
- include ja.po with new date format

* Wed Aug 28 2002 Havoc Pennington <hp@redhat.com>
- remove noreplace on gdm.conf #71309
- make gnome-gdmsetup absolute, #72910

* Wed Aug 28 2002 Havoc Pennington <hp@redhat.com>
- put /usr/X11R6/bin in path for now fixes #72781
- use proper i18n algorithm for word wrap, #71937
- remove greek text from language picker due to lack 
  of greek font
- reorder PAM config file #72657

* Wed Aug 28 2002 Havoc Pennington <hp@redhat.com>
- improve gdmsetup icon
- remove GNOME session, we will instead put it in gnome-session
- apply patch from george to make gdmphotosetup file selector 
  work

* Mon Aug 26 2002 Elliot Lee <sopwith@redhat.com> 2.4.0.7-6
- Patches for #64902, #66486, #68483, #71308
- post-install script changes from the gdm.spec mentioned in #70965
- noreplace on gdm.conf for #71309

* Sun Aug 25 2002 Havoc Pennington <hp@redhat.com>
- put in a patch from george to fix some setsid()/kill() confusion
  possibly fixing #72295
- turn off UseCirclesInEntry for now, fixes #72433

* Tue Aug 20 2002 Alexander Larsson <alexl@redhat.com>
- Set UseCirclesInEntry to true in config

* Thu Aug 15 2002 Havoc Pennington <hp@redhat.com>
- rename Gnome session to GNOME, this was just bugging me

* Thu Aug  8 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0.7 with bugfixes George kindly did for me, 
  including mnemonics for the graphical greeter
- use Wonderland gtk theme for the nongraphical greeter
- remove patches that are now upstream

* Tue Jul 30 2002 Havoc Pennington <hp@redhat.com>
- update rhconfig patch
- use pam_timestamp for the config tool
- link to a desktop file in redhat-menus
- update .gnome2 patch, filed upstream bug
- 2.4.0.4
- rebuild with new gail, librsvg2

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Require redhat-artwork, make the default greeter theme Wonderland
- Look for all configuration in .gnome2 not .gnome. This avoids problems 
  with changes in the set of session/lang.
- Remove English from locale.alias, make most locales UTF-8
- Call find_lang with the right name

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new libs
- put gdm-autologin pam config file in file list, hope
  its absence wasn't deliberate
- use desktop-file-install

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun 10 2002 Havoc Pennington <hp@redhat.com>
- 2.4.0.0

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 2.3.90.3

* Tue May 14 2002 Matt Wilson <msw@redhat.com> 2.3.90.2.90-1
- pulled from current CVS, named it 2.3.90.2.90-1

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new libs
- add URL tag

* Mon Feb 11 2002 Alex Larsson <alexl@redhat.com> 2.3.90.1.90-1
- Updated to a cvs snapshot that has the new greeter.

* Thu Jan 24 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide

* Tue Sep  4 2001 Havoc Pennington <hp@redhat.com>
- fix #52997 (ukrainian in language list)

* Fri Aug 31 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Wed Aug 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- set SESSION to true in console.apps control file

* Tue Aug 14 2001 Havoc Pennington <hp@redhat.com>
- change default title font to work in CJK, #51698

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- fix %pre for using /var/gdm as home dir

* Sun Aug  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- Tweak PAM setup for gdmconfig to match other consolehelper users

* Fri Aug  3 2001 Owen Taylor <otaylor@redhat.com>
- Set RUNNING_UNDER_GDM when running display init script
- Run xsri as the background program

* Thu Aug 02 2001 Havoc Pennington <hp@redhat.com>
- Change how session switching works, #49480
- don't offer to make Failsafe the default, #49479

* Thu Aug 02 2001 Havoc Pennington <hp@redhat.com>
- clean up some format string mess, and don't
  log username to syslog, #5681
- own some directories #50692

* Wed Aug 01 2001 Havoc Pennington <hp@redhat.com>
- require/buildrequire latest gnome-libs, to compensate
  for upstream crackrock. #50554

* Tue Jul 31 2001 Havoc Pennington <hp@redhat.com>
- get rid of GiveConsole/TakeConsole, bug #33710

* Sun Jul 22 2001 Havoc Pennington <hp@redhat.com>
- use Raleigh theme for gdm

* Thu Jul 19 2001 Havoc Pennington <hp@redhat.com>
- depend on usermode, xinitrc
 
* Thu Jul 19 2001 Havoc Pennington <hp@redhat.com>
- build requires pam-devel, should fix #49448

* Mon Jul 16 2001 Havoc Pennington <hp@redhat.com>
- log to /var/log/gdm/*

* Mon Jul 16 2001 Havoc Pennington <hp@redhat.com>
- make Halt... power off

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- gdm user's homedir to /var/gdm not /home/gdm

* Mon Jul 09 2001 Havoc Pennington <hp@redhat.com>
- put pam.d/gdm back in file list

* Sun Jul 08 2001 Havoc Pennington <hp@redhat.com>
- upgrade to 2.2.3.1, pray this fixes more than it breaks

* Thu Jul 05 2001 Havoc Pennington <hp@redhat.com>
- add "rpm" user to those not to show in greeter 

* Tue Jul 03 2001 Havoc Pennington <hp@redhat.com>
- Upgrade to 2.2.3
- require usermode since configure script now checks for it

* Fri Jun 01 2001 Havoc Pennington <hp@redhat.com>
- Prereq for scrollkeeper-update

* Thu May 30 2001 Havoc Pennington <hp@redhat.com>
- New CVS snap with the "no weird sessions" options; 
  more default settings changes

* Wed May 30 2001 Havoc Pennington <hp@redhat.com>
- Change a bunch of default settings; remaining fixes will involve C hacking

* Wed May 30 2001 Havoc Pennington <hp@redhat.com>
- After, oh, 2 years or so, finally upgrade version and set
  release to 1. Remove all hacks and patches, pretty much;
  this will break a few things, will be putting them back 
  via GNOME CVS. All changes should go in 'gdm2' module in 
  CVS for now.

  This RPM enables all kinds of features that I'm going to turn
  off shortly, so don't get excited about them. ;-)

* Thu Mar 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- reinitialize pam credentials after calling initgroups() -- the
  credentials may be group memberships

* Mon Mar 19 2001 Owen Taylor <otaylor@redhat.com>
- Fix colors patch

* Thu Mar 15 2001 Havoc Pennington <hp@redhat.com>
- translations

* Mon Mar  5 2001 Preston Brown <pbrown@redhat.com>
- don't screw up color map on 8 bit displays

* Fri Feb 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify
- Don't define and use "ver" and "nam" at the top of the spec file
- use %%{_tmppath}

* Tue Feb 13 2001 Tim Powers <timp@redhat.com>
- don't allow gdm to show some system accounts in the browser bugzilla
  #26898

* Fri Jan 19 2001 Akira TAGOH <tagoh@redhat.com>
- Updated Japanese translation.

* Tue Jan 02 2001 Havoc Pennington <hp@redhat.com>
- add another close() to the fdleak patch, bugzilla #22794

* Sun Aug 13 2000 Owen Taylor <otaylor@redhat.com>
- Return to toplevel main loop and start Xdcmp if enabled
  (Bug #16106) 

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Aug 02 2000 Havoc Pennington <hp@redhat.com>
- Requires Xsession script

* Wed Jul 19 2000 Owen Taylor <otaylor@redhat.com>
- Italian is better as it_IT than it_CH (bugzilla 12425)

* Mon Jul 17 2000 Jonathan Blandford <jrb@redhat.com>
- Don't instally gdmconfig as it doesn't work.

* Fri Jul 14 2000 Havoc Pennington <hp@redhat.com>
- Rearrange code to avoid calling innumerable system calls
  in a signal handler

* Fri Jul 14 2000 Havoc Pennington <hp@redhat.com>
- Verbose debug spew for infinite loop stuff

* Fri Jul 14 2000 Havoc Pennington <hp@redhat.com>
- Try to fix infinite loops on X server failure

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Havoc Pennington <hp@redhat.com>
- Remove Docdir

* Mon Jun 19 2000 Havoc Pennington <hp@redhat.com>
- Fix file descriptor leak (Bugzilla 12301)

* Mon Jun 19 2000 Havoc Pennington <hp@redhat.com>
- Apply security errata patch we released for 6.2
- Add Gnome.session back, don't know when it disappeared or why

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth

* Fri May 19 2000 Havoc Pennington <hp@redhat.com>
- rebuild for the Winston tree

* Fri Feb 04 2000 Havoc Pennington <hp@redhat.com>
- Modify Default.session and Failsafe.session not to add -login option to bash
- exec the session scripts with the user's shell with a hyphen prepended
- doesn't seem to actually work yet with tcsh, but it doesn't seem to 
  break anything. needs a look to see why it doesn't work

* Fri Feb 04 2000 Havoc Pennington <hp@redhat.com>
- Link PreSession/Default to xdm/GiveConsole
- Link PostSession/Default to xdm/TakeConsole

* Fri Feb 04 2000 Havoc Pennington <hp@redhat.com>
- Fix the fix to the fix (8877)
- remove docs/gdm-manual.txt which doesn't seem to exist from %doc

* Fri Feb 04 2000 Havoc Pennington <hp@redhat.com>
- Enhance 8877 fix by not deleting the "Please login" 
  message

* Fri Feb 04 2000 Havoc Pennington <hp@redhat.com>
- Try to fix bug 8877 by clearing the message below 
  the entry box when the prompt changes. may turn 
  out to be a bad idea.

* Mon Jan 17 2000 Elliot Lee <sopwith@redhat.com>
- Fix bug #7666: exec Xsession instead of just running it

* Mon Oct 25 1999 Jakub Jelinek <jakub@redhat.com>
- Work around so that russian works (uses koi8-r instead
  of the default iso8859-5)

* Tue Oct 12 1999 Owen Taylor <otaylor@redhat.com>
- Try again

* Tue Oct 12 1999 Owen Taylor <otaylor@redhat.com>
- More fixes for i18n

* Tue Oct 12 1999 Owen Taylor <otaylor@redhat.com>
- Fixes for i18n

* Fri Sep 26 1999 Elliot Lee <sopwith@redhat.com>
- Fixed pipewrite bug (found by mkj & ewt).

* Fri Sep 17 1999 Michael Fulbright <drmike@redhat.com>
- added requires for pam >= 0.68

* Fri Sep 10 1999 Elliot Lee <sopwith@redhat.com>
- I just update this package every five minutes, so any recent changes are my fault.

* Thu Sep 02 1999 Michael K. Johnson <johnsonm@redhat.com>
- built gdm-2.0beta2

* Mon Aug 30 1999 Michael K. Johnson <johnsonm@redhat.com>
- built gdm-2.0beta1

* Tue Aug 17 1999 Michael Fulbright <drmike@redhat.com>
- included rmeier@liberate.com patch for tcp socket X connections

* Mon Apr 19 1999 Michael Fulbright <drmike@redhat.com>
- fix to handling ancient gdm config files with non-standard language specs
- dont close display connection for xdmcp connections, else we die if remote
  end dies. 

* Fri Apr 16 1999 Michael Fulbright <drmike@redhat.com>
- fix language handling to set GDM_LANG variable so gnome-session 
  can pick it up

* Wed Apr 14 1999 Michael Fulbright <drmike@redhat.com>
- fix so certain dialog boxes dont overwrite background images

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- do not specify -r 42 to useradd -- it doesn't know how to fall back
  if id 42 is already taken

* Fri Apr 9 1999 Michael Fulbright <drmike@redhat.com>
- removed suspend feature

* Mon Apr 5 1999 Jonathan Blandford <jrb@redhat.com>
- added patch from otaylor to not call gtk funcs from a signal.
- added patch to tab when username not added.
- added patch to center About box (and bring up only one) and ignore "~"
  and ".rpm" files.

* Fri Mar 26 1999 Michael Fulbright <drmike@redhat.com>
- fixed handling of default session, merged all gdmgreeter patches into one

* Tue Mar 23 1999 Michael Fulbright <drmike@redhat.com>
- remove GNOME/KDE/AnotherLevel session scripts, these have been moved to
  the appropriate packages instead.
- added patch to make option menus always active (security problem otherwise)
- added jrb's patch to disable stars in passwd entry field

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- made sure /usr/bin isnt in default path twice
- strip binaries

* Wed Mar 17 1999 Michael Fulbright <drmike@redhat.com>
- fixed to use proper system path when root logs in

* Tue Mar 16 1999 Michael Fulbright <drmike@redhat.com>
- linked Init/Default to Red Hat default init script for xdm
- removed logo from login dialog box

* Mon Mar 15 1999 Michael Johnson <johnsonm@redhat.com>
- pam_console integration

* Tue Mar 09 1999 Michael Fulbright <drmike@redhat.com>
- added session files for GNOME/KDE/AnotherLevel/Default/Failsafe
- patched gdmgreeter to not complete usernames
- patched gdmgreeter to not safe selected session permanently
- patched gdmgreeter to center dialog boxes

* Mon Mar 08 1999 Michael Fulbright <drmike@redhat.com>
- removed comments from gdm.conf file, these are not parsed correctly

* Sun Mar 07 1999 Michael Fulbright <drmike@redhat.com>
- updated source line for accuracy

* Fri Feb 26 1999 Owen Taylor <otaylor@redhat.com>
- Updated patches for 1.0.0
- Fixed some problems in 1.0.0 with installation directories
- moved /usr/var/gdm /var/gdm

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- moved files from /usr/etc to /etc

* Tue Feb 16 1999 Michael Johnson <johnsonm@redhat.com>
- removed commented-out #1 definition -- put back after testing gnome-libs
  comment patch

* Sat Feb 06 1999 Michael Johnson <johnsonm@redhat.com>
- initial packaging
