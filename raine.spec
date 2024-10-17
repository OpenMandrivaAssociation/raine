# Debug is not properly generated and we don't need it anyway here
%define _enable_debug_packages %{nil}
%define debug_package %{nil}

%define build_optimization 0
%{?_with_optimization: %{expand: %%global build_optimization 1}}

Summary:	An arcade emulator
Name:		raine
Version:	0.64.10
Release:	1
License:	Freeware
#i.e: "Raine license", open-source freeware, distributable
Group:		Emulators
Url:		https://raine.1emulation.com/
Source0:	http://raine.1emulation.com/htmlarchive/%{name}-%{version}.tar.gz
Source1:	http://raine.1emulation.com/html/archive/icons.zip
Source2:	http://raine.1emulation.com/html/archive/rainedocs.zip
Source6:	raine-neocd-cheats.tar.gz
Source7:	hiscore.7z
Source20:	%{name}.rpmlintrc
Patch1:		raine-0.63.12-makefile-libs.patch

# artwork sources from : http://www.rainemu.com/html/download/extras.html
# to add an artwork archive :
# add its basename to the artwork_sources list below
%define artwork_sources "1941 19xx arbalest arkanoid arknoid2 batrider\
 bjtwin block darius2 ddonpach dfeveron dkong dogyuun donpachi downtown\
 driftout extrmatn fireshrk frogger ghoulsu gunbird majest12 matmania\
 mercs msh mspacman msword ninjaw outzone pacman pacplus pengo puckman\
 s1945 sf2ce slammast ssi superman tdragon terracre thunderl tknight\
 tndrcade varth vimana warriorb xmcota"
# this generates Source5xx tags
%(echo %{artwork_sources} | awk 'BEGIN { RS=" "; n=0 }; { print "Source"500+n":\t"$1".zip"; n++ };')
# this generates the list of artwork files for the install step
%define artwork_files %(echo %{artwork_sources} | awk 'BEGIN { RS=" "; files="" }; { files=files" %{_sourcedir}/"$1".zip"}; END { print files };')

BuildRequires:	desktop-file-utils
BuildRequires:	nasm
BuildRequires:	p7zip
# for the converter
BuildRequires:	pkgconfig(allegro)
# the rest
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(muparser)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_ttf)
BuildRequires:	SDL_sound-devel
ExclusiveArch:	%{ix86}
Obsoletes:	%{name}-neocd < 0.62.0
Provides:	neoraine = %{EVRD}

%description
Raine is an emulator, it emulates some M68000 and M68020 arcade games
and is mainly focused on Taito and Jaleco games hardware.

Since 0.62 Raine was merged with NeoRaine into one emulator.

To play NeoGeo CD games you need neocd.bin (or neocd.zip), which is the
neocd bios to be in the (neo)raine's data directory:
%{_gamesdatadir}/raine

%package artwork
Summary:	Artwork for Raine
Group:		Emulators
Requires:	raine

%description artwork
Artwork for Raine. These files are pictures used mainly to fill the ugly 
black borders in vertical games.

%prep
%setup -q
%autopatch -p1

%setup -q -T -D -a 1 -a 2 -a 6
7za x -y %{SOURCE7}

%build
%if !%{build_optimization}
 rm -f cpuinfo
 echo "_MARCH=-march=i586 -mtune=pentiumpro" > cpuinfo
 echo "CPU=pentiumpro" >> cpuinfo
%else
 rm -f cpuinfo
%endif
export OSTYPE
%make
make converter

%install
%makeinstall_std VERBOSE=1

# savegame converter
install -D -m 755 converter %{buildroot}%{_gamesbindir}/raine-savegame-converter

# icons
install -D -m 644 Raine48x48.png %{buildroot}%{_liconsdir}/raine.png
install -D -m 644 Raine32X32.png %{buildroot}%{_iconsdir}/raine.png
install -D -m 644 Raine16X16.png %{buildroot}%{_miconsdir}/raine.png

# menu
desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-MoreApplications-Emulators" \
  --dir %{buildroot}%{_datadir}/applications/ \
  %{buildroot}%{_datadir}/applications/*

# artwork
mkdir -p %{buildroot}%{_gamesdatadir}/raine/artwork
install -m 644 %{artwork_files} %{buildroot}%{_gamesdatadir}/raine/artwork

# remove no longer needed but still installed neoraine files
rm -f %{buildroot}%{_datadir}/pixmaps/neoraine.png
rm -f %{buildroot}%{_datadir}/applications/neoraine.desktop

%files
%defattr(0644,root,root,0755)
%doc raine.txt raine.lyx
%attr(0755,root,root) %{_gamesbindir}/raine
%attr(0755,root,root) %{_gamesbindir}/raine-savegame-converter
%dir %{_gamesdatadir}/raine
%{_gamesdatadir}/raine/cheats.cfg
%{_gamesdatadir}/raine/hiscore.dat
%{_gamesdatadir}/raine/debug_dips.txt
%{_gamesdatadir}/raine/bitmaps
%{_gamesdatadir}/raine/fonts
%{_gamesdatadir}/raine/roms
%{_gamesdatadir}/raine/scripts
%{_gamesdatadir}/raine/shaders
%{_gamesdatadir}/raine/locale
%{_iconsdir}/raine.png
%{_miconsdir}/raine.png
%{_liconsdir}/raine.png
%{_datadir}/pixmaps/raine.png
%{_datadir}/applications/raine.desktop
# ex-neocd files
%{_gamesdatadir}/raine/neocheats.cfg

%files artwork
%defattr(0644,root,root,0755)
%doc raine.txt
%{_gamesdatadir}/raine/artwork

