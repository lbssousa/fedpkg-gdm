# Note that this is NOT a relocatable package
%define ver      2.0beta2
%define rel 37tc1
%define prefix   /usr

Summary: The GNOME Display Manager.
Name: gdm
Version: %ver
Release: %rel
Epoch: 1
Copyright: LGPL/GPL
Group: User Interface/X
Source: ftp://ftp.socsci.auc.dk/pub/empl/mkp/gdm-%{PACKAGE_VERSION}.tar.gz
Source1: Gnome.session
Source2: Default.session
Source5: Failsafe.session

# FIXME: remove dead patches once we are sure they are really dead.  :-)
Patch0: gdm-2.0beta2-rhconf.patch
# msw says not needed.  :-)
Patch1: gdm-2.0beta1-installdirs.patch
# /etc/X11/gdm/gnomerc is missing...
Patch3: gdm-gnomerc.patch
# Patch4 not currently applied, but kept around for potential later use
Patch4: gdm-1.0.0-rhgreeter.patch
Patch7: gdm-2.0beta1-nosound.patch
# Patch8 not currently applied; make sure that tab completion isn't there
Patch8: gdm-1.0.0-notabcmpltion.patch
# Patch9 should now be unnecessary
Patch9: gdm-1.0.0-signal.patch
Patch10: gdm-2.0beta1-sessions.patch
# Patch11 should now be unnecessary
Patch11: gdm-1.0.0-nosuspend.patch
# Patch12 does not seem to be necessary
Patch12: gdm-1.0.0-dontblastlogo.patch
# We probably need this, but I don't know how to apply it right now...
Patch13: gdm-1.0.0-fixlangs2.patch
# Probably unnecessary
Patch14: gdm-1.0.0-noclosedspy.patch
# depends on fixlangs2
Patch15: gdm-1.0.0-norwegian.patch
# photo stuff is gone now?
Patch16: gdm-1.0.0-photofix.patch

Patch20: gdm-2.0beta2-sopfixes.patch
Patch21: gdm-2.0beta2-daemonfixes.patch
Patch22: gdm-2.0beta2-sop2.patch
Patch23: gdm-2.0beta2-xdmcp.patch
Patch24: gdm-2.0beta2-dblclick.patch
# 25 is RH-specific
Patch25: gdm-2.0beta2-rhconf2.patch
Patch26: gdm-2.0beta2-norootcheck.patch
Patch27: gdm-2.0beta2-dumberrmsg.patch
#Patch28: gdm-2.0beta2-fixlang.patch
# 29 is RH-specific
Patch29: gdm-2.0beta2-noiconify.patch
#Patch 30 is RH-specific
Patch30: gdm-2.0beta2-fixsesslang.patch

Patch31: gdm-2.0beta2-loginhang.patch
Patch32: gdm-2.0beta2-nogdmconfig.patch
Patch33: gdm-2.0beta2-pipewrite.patch

Patch34: gdm-2.0beta2-i18n.patch
Patch35: gdm-2.0beta2-ru.patch

Patch36: gdm-2.0beta2-chpass.patch
Patch37: gdm-2.0beta2-fixmessages.patch
Patch38: gdm-2.0beta2-fixfirstmessage.patch
Patch39: gdm-2.0beta2-usershell.patch
Patch40: gdm-2.0beta2-system-auth.patch
Patch41: gdm-2.0beta2-security2.patch
Patch42: gdm-2.0beta2-fdleak.patch
Patch43: gdm-2.0beta2-loopofdeath.patch
Patch44: gdm-2.0beta2-it.patch
Patch45: gdm-2.0beta2-ja.po.patch
Patch46: gdm-2.0beta2-zh_TW.po.patch

BuildRoot: /var/tmp/gdm-%{PACKAGE_VERSION}-root

Prereq: /usr/sbin/useradd
Requires: pam >= 0.68
Requires: gnome-libs >= 1.0.17
Requires: /etc/pam.d/system-auth
Requires: /etc/X11/xdm/Xsession

%description
Gdm (the GNOME Display Manager) is a highly configurable
reimplementation of xdm, the X Display Manager. Gdm allows you to log
into your system with the X Window System running and supports running
several different X sessions on your local machine at the same time.

%prep
%setup -q
%patch0 -p1 -b .rhconf
#%patch1 -p1 -b .installdirs
%patch3 -p1 -b .gnomerc
#%patch4 -p1 -b .rhgreeter
# don't know if this is necessary, as gdm.conf adds --disable-sound
%patch7 -p1 -b .nosound
#%patch8 -p1 -b .notabcmpltion
#%patch9 -p1 -b .signal
%patch10 -p1 -b .sessions
#%patch11 -p1 -b .nosuspend
#%patch12 -p1 -b .dontblastlogo
#%patch13 -p1 -b .fixlangs
#%patch14 -p1 -b .noclosedspl
#%patch15 -p1 -b .norwegian
#%patch16 -p1 -b .photofix

%patch20 -p1 -b .sopgui
%patch21 -p1 -b .sopdaemon
%patch22 -p1 -b .soproot
%patch23 -p1 -b .xdmcp
%patch24 -p1 -b .dblclick
%patch25 -p1 -b .rhconf2
%patch26 -p1 -b .norootcheck
%patch27 -p1 -b .dumberrmsg
#%patch28 -p1 -b .fixlang
%patch29 -p1 -b .noiconify
%patch30 -p1 -b .fixsesslang
%patch31 -p1 -b .loginhang
%patch32 -p1 -b .nogdmconfig
%patch33 -p1 -b .pipewrite
%patch34 -p1 -b .i18n
%patch35 -p1 -b .ru
%patch36 -p1 -b .chpass
%patch37 -p1 -b .fixmessages
%patch38 -p1 -b .fixfirstmessage
%patch39 -p1 -b .usershell
%patch40 -p1 -b .system-auth
%patch41 -p1 -b .security2
%patch42 -p1 -b .fdleak
%patch43 -p1 -b .loopofdeath
%patch44 -p1 -b .it
%patch45 -p1 -b .jaupdate
%patch46 -p1 -b .zh_TW

# So it doesn't get automatically rebuilt
touch -t '199001010000' configure.in

%build
libtoolize --force
automake
autoconf
autoheader
CFLAGS="-g $RPM_OPT_FLAGS" ./configure --prefix=%prefix --sysconfdir=/etc/X11 --localstatedir=/var
make
(cd config; make gdm.conf gnomerc Gnome)

%install
rm -rf $RPM_BUILD_ROOT

/usr/sbin/useradd -r gdm > /dev/null 2>&1 || /bin/true

make prefix=$RPM_BUILD_ROOT%{prefix} sysconfdir=$RPM_BUILD_ROOT/etc/X11 localstatedir=$RPM_BUILD_ROOT/var install
# docs go elsewhere
rm -rf $RPM_BUILD_ROOT/%{prefix}/doc

# install RH specific session files
rm -f $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/*

install -m 755 %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/Gnome
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/Default
install -m 755 %{SOURCE5} $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/Failsafe
ln -sf Default $RPM_BUILD_ROOT/etc/X11/gdm/Sessions/default

# put gnomerc in the right place
install -m 644 config/gnomerc $RPM_BUILD_ROOT/etc/X11/gdm/gnomerc

# change default Init script to be Red Hat default
ln -sf ../../xdm/Xsetup_0 $RPM_BUILD_ROOT/etc/X11/gdm/Init/Default

# run GiveConsole/TakeConsole
mkdir $RPM_BUILD_ROOT/etc/X11/gdm/PreSession
mkdir $RPM_BUILD_ROOT/etc/X11/gdm/PostSession
ln -sf ../../xdm/GiveConsole $RPM_BUILD_ROOT/etc/X11/gdm/PreSession/Default
ln -sf ../../xdm/TakeConsole $RPM_BUILD_ROOT/etc/X11/gdm/PostSession/Default

# move pam.d stuff to right place
mv $RPM_BUILD_ROOT/etc/X11/pam.d $RPM_BUILD_ROOT/etc

# strip binaries
rm $RPM_BUILD_ROOT%{prefix}/bin/gdmconfig
# strip $RPM_BUILD_ROOT%{prefix}/bin/*

%clean
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/useradd -u 42 -r gdm > /dev/null 2>&1
# ignore errors, as we can't disambiguate between gdm already existed
# and couldn't create account with the current adduser.
exit 0

%files
%defattr(-, root, root)

%doc AUTHORS COPYING ChangeLog NEWS README
%{prefix}/bin/*
%config /etc/pam.d/gdm
%config /etc/X11/gdm/gnomerc
%config /etc/X11/gdm/gdm.conf
%config /etc/X11/gdm/locale.alias
%config /etc/X11/gdm/Sessions/*
%config /etc/X11/gdm/Init/*
%config /etc/X11/gdm/PreSession/*
%config /etc/X11/gdm/PostSession/*
%{prefix}/share/locale/*/*/*
%{prefix}/share/pixmaps/*
%attr(750, gdm, gdm) %dir /var/gdm

%changelog
* Sun Jan  7 2001 Jason Wilson <jwilson@redhat.com>
- added Traditional Chinese translations
- added Chinese and Korean to locale list

* Tue Sep 12 2000 Matt Wilson <msw@redhat.com>
- updated Japanese translation from Nakai-san

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
