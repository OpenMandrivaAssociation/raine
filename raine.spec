%define build_optimization 0
%{?_with_optimization: %{expand: %%global build_optimization 1}}

Name:		raine
Version:	0.60.0
Release:	1
Summary:	An arcade emulator
License:	Freeware
#i.e: "Raine license", open-source freeware, distributable
Group:		Emulators
URL:		http://rainemu.swishparty.co.uk/
Source0:	http://rainemu.swishparty.co.uk/htmlarchive/%{name}-%{version}.tar.bz2
Source1:	http://rainemu.swishparty.co.uk/html/archive/icons.zip
Source2:	http://rainemu.swishparty.co.uk/html/archive/rainedocs.zip
Source3:	http://rainemu.swishparty.co.uk/html/archive/raine.pdf
# From 0.50.6
Source4:	shots.pl
Source6:	raine-neocd-cheats.tar.gz
Source7:	hiscore.7z
# free rom
Source10:	http://www.rainemu.com/html/archive/f2demo.zip
Source11:	http://www.rainemu.com/html/archive/f3demo.zip

Source20:	%{name}.rpmlintrc

# emudx sources from : http://www.rainemu.com/html/archive/emudx/
# to add an emudx file :
# add its basename to the emudx_sources list below 
%define emudx_sources "dkongg dkongm froggerg froggerm galdxg galdxm\
 mspacmang pacmang"
#mspacmanm pacmanm
# this generates Source1xx tags (400 max)
%(echo %{emudx_sources} | awk 'BEGIN { RS=" "; n=0 }; { print "Source"100+n":\t"$1".dx2"; n++ };')
# this generates the list of emudx files for the install step
%define emudx_files %(echo %{emudx_sources} | awk 'BEGIN { RS=" "; files="" }; { files=files" %{_sourcedir}/"$1".dx2"}; END { print files };')

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

BuildRequires:	SDL-devel
#BuildRequires:	SDL_mixer-devel
BuildRequires:	SDL_sound-devel
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_ttf-devel
BuildRequires:	png-devel
BuildRequires:	muparser-devel
BuildRequires:	ElectricFence-devel
BuildRequires:	nasm
BuildRequires:	perl
BuildRequires:	p7zip
#for the converter
BuildRequires:	allegro-devel
BuildRequires:	desktop-file-utils

ExclusiveArch:	%{ix86}

%description
Raine is an emulator, it emulates some M68000 and M68020 arcade games
and is mainly focused on Taito and Jaleco games hardware.

%package artwork
Summary:	Artwork for Raine
Group:		Emulators
Requires:	raine

%description artwork
Artwork for Raine. These files are pictures used mainly to fill the ugly 
black borders in vertical games.

%package emudx2
Summary:	Files to enhance emulation of old arcade games in raine
Group:		Emulators
Requires:	raine
%rename		raine-emudx

%description emudx2
Files to enhance emulation of old arcade games.
Donkey Kong, Frogger, Galaxian, Pac-Man and Ms. Pac-Man are suported.

It requires the roms to be enhanced and the raine emulator.

%package neocd
Summary:	NeoRaine - raine version with support for NeoGeo CD
Group:		Emulators
Requires:	raine
Provides:	neoraine 

%description neocd
NeoRaine is a modified raine version with support for NeoGeo CD.
You'll need neocd.bin (or neocd.zip), which is the neocd bios to be in the 
(neo)raine's data directory : %{_gamesdatadir}/raine
So it depends on raine for now.

You may find other interesting information on 
http://www.rainemu.com/html/download/neoraine.html

%prep
%setup -q
%setup -q -n raine-%{version} -T -D -a 1 -a 2 -a 6
perl -pi -e "s|NEO=1|#NEO=1|g" makefile
cp -p %{_sourcedir}/raine.pdf %{_sourcedir}/shots.pl .
7za x -y %{_sourcedir}/hiscore.7z

%build
%if !%build_optimization
 rm -f cpuinfo
 echo "_MARCH=-march=i586 -mtune=pentiumpro" > cpuinfo
 echo "CPU=pentiumpro" >> cpuinfo 
%else
 rm -f cpuinfo
%endif
export OSTYPE
%make
make converter
#neoraine
%make NEO=1

%install
rm -rf %{buildroot}
%makeinstall_std VERBOSE=1

#savegame converter
install -D -m 755 converter %{buildroot}%{_gamesbindir}/raine-savegame-converter

#history
install -D -m 644 history.dat %{buildroot}%{_gamesdatadir}/raine/history.dat

#icons
install -D -m 644 Raine48x48.png %{buildroot}%{_liconsdir}/raine.png
install -D -m 644 Raine32X32.png %{buildroot}%{_iconsdir}/raine.png
install -D -m 644 Raine16X16.png %{buildroot}%{_miconsdir}/raine.png

#menu
desktop-file-install --vendor="" \
  --add-category="X-MandrivaLinux-MoreApplications-Emulators" \
  --dir %{buildroot}%{_datadir}/applications/ \
  %{buildroot}%{_datadir}/applications/*

#artwork
mkdir -p %{buildroot}%{_gamesdatadir}/raine/artwork
install -m 644 %{artwork_files} %{buildroot}%{_gamesdatadir}/raine/artwork

#emudx
install -d -m 755 %{buildroot}%{_gamesdatadir}/raine/emudx
install -m 644 %{emudx_files} %{buildroot}%{_gamesdatadir}/raine/emudx

#neoraine
%makeinstall_std NEO=1

%files
%defattr(0644,root,root,0755)
%doc raine.txt raine.pdf raine.lyx shots.pl
%attr(0755,root,root) %{_gamesbindir}/raine
%attr(0755,root,root) %{_gamesbindir}/raine-savegame-converter
%dir %{_gamesdatadir}/raine
%{_gamesdatadir}/raine/cheats.cfg
%{_gamesdatadir}/raine/hiscore.dat
%{_gamesdatadir}/raine/history.dat
%{_gamesdatadir}/raine/bitmaps
%{_gamesdatadir}/raine/fonts
%{_gamesdatadir}/raine/roms
%{_iconsdir}/raine.png
%{_miconsdir}/raine.png
%{_liconsdir}/raine.png
%{_datadir}/pixmaps/raine.png
%{_datadir}/applications/raine.desktop

%files artwork
%defattr(0644,root,root,0755)
%doc raine.txt
%{_gamesdatadir}/raine/artwork

%files emudx2
%defattr(0644,root,root,0755)
%doc raine.txt
%{_gamesdatadir}/raine/emudx

%files neocd
%defattr(0644,root,root,0755)
%doc raine.txt
%attr(0755,root,root) %{_gamesbindir}/neoraine
%{_gamesdatadir}/raine/neocheats.cfg
%{_datadir}/pixmaps/neoraine.png
%{_datadir}/applications/neoraine.desktop


