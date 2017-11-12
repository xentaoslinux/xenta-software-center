SUBDIRS = po

lscbindir = $(bindir)
lscbin_SCRIPTS = \
	xenta-software-center

lscsbindir = $(sbindir)
lscsbin_SCRIPTS = \
	scripts/xenta-software-center-build-db

lsclibscriptdir = $(pkgpyexecdir)
lsclibscript_SCRIPTS = \
        scripts/xenta-software-center-download-scrot \
	scripts/xenta-software-center-download-review

lscdir = $(pythondir)/LSC
lsc_PYTHON = \
	src/control.py \
	src/__init__.py \
	src/main.py \
	src/preferences.py \
	src/threadingops.py \
	src/UI.py \
	src/notify.py \
	src/testnet.py

lscwidgetsdir = $(pythondir)/LSC/widgets
lscwidgets_PYTHON = \
	src/widgets/__init__.py \
	src/widgets/appsinfo.py \
	src/widgets/basket.py \
	src/widgets/searchentry.py \
	src/widgets/toolbar.py \
	src/widgets/appsview.py \
	src/widgets/categories.py \
	src/widgets/pages.py \
	src/widgets/statusbox.py \
	src/widgets/screenshot.py

lscdatadir = $(datadir)/LSC
lscdata_DATA = \
	data/categories.ini \
	data/lsc.ui \
	data/preferences.ui

icon16dir = $(datadir)/icons/hicolor/16x16/apps
icon16_DATA = data/icons/16x16/xenta-software-center.png

icon24dir = $(datadir)/icons/hicolor/24x24/apps
icon24_DATA = data/icons/24x24/xenta-software-center.png

icon48dir = $(datadir)/icons/hicolor/48x48/apps
icon48_DATA = data/icons/48x48/xenta-software-center.png

icon128dir = $(datadir)/icons/hicolor/128x128/apps
icon128_DATA = data/icons/128x128/xenta-software-center.png

desktop_in_files = xenta-software-center.desktop.in 
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@
desktopdir = $(datadir)/applications

%.ini: %.ini.in $(INTLTOOL_MERGE) $(wildcard $(top_srcdir)/po/*.po) ; LC_ALL=C $(INTLTOOL_MERGE) -d -u -c $(top_builddir)/po/.intltool-merge-cache $(top_srcdir)/po $< $@

inidir = $(lscdatadir)
ini_in_files = $(wildcard data/*.ini.in)
 
ini_DATA = $(ini_in_files:.ini.in=.ini)
dist_noinst_DATA = $(ini_in_files)

dist_man_MANS = data/man/xenta-software-center.1 \
                data/man/xenta-software-center-build-db.1

CLEANFILES = \
	$(BUILT_SOURCES)
	
DISTCLEANFILES = \
	$(CLEANFILES)
	
EXTRA_DIST = \
        $(lscbin_SCRIPTS) \
        $(lscsbin_SCRIPTS) \
        $(lsclibscript_SCRIPTS) \
        $(lscdata_DATA) \
        $(lscman_DATA) \
        $(desktop_DATA) \
        $(desktop_in_files) \
        $(ini_DATA) \
        $(ini_in_files) \
        $(icon16_DATA) \
        $(icon24_DATA) \
        $(icon48_DATA) \
        $(icon128_DATA)

clean-local:
	rm -rf *.pyc *.pyo
