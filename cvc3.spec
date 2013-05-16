Summary:	Validity checker of many-sorted first-order formulas with theories
Name:		cvc3
Version:	2.4.1
Release:	1
License:	BSD and MIT
Group:		Applications/Engineering
URL:		http://www.cs.nyu.edu/acsys/cvc3/
Source0:	http://www.cs.nyu.edu/acsys/cvc3/download/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9b082b0e8c80e1459e9653de044e0d6e
Patch0:		%{name}-doxygen.patch
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	perl
BuildRequires:	python
BuildRequires:	texlive-latex
BuildRequires:	time
BuildRequires:	transfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CVC3 is an automatic theorem prover for Satisfiability Modulo Theories
(SMT) problems. It can be used to prove the validity (or, dually, the
satisfiability) of first-order formulas in a large number of built-in
logical theories and their combination.

CVC3 is the latest offspring of a series of popular SMT provers, which
originated at Stanford University with the SVC system. In particular,
it builds on the code base of CVC Lite, its most recent predecessor.
Its high level design follows that of the Sammy prover.

CVC3 works with a version of first-order logic with polymorphic types
and has a wide variety of features including:

 - several built-in base theories: rational and integer linear
   arithmetic, arrays, tuples, records, inductive data types, bit
   vectors, and equality over uninterpreted function symbols;
 - support for quantifiers;
 - an interactive text-based interface;
 - a rich C and C++ API for embedding in other systems;
 - proof and model generation abilities;
 - predicate subtyping;
 - essentially no limit on its use for research or commercial purposes
   (see license).

For example, if you run 'cvc3 +interactive' and submit: i, j: INT;
ASSERT i = j + 1; QUERY i>j; it will determine "Valid." If you then
ask: QUERY i<j; COUNTERMODEL; it will determine "Invalid." and show an
example demonstrating when the formula is not true (e.g., i = 0 and j
= -1).

%package devel
Summary:	Header files for development with CVC3
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files need to develop with CVC3.

%package doc
Summary:	API documentation for CVC3
Group:		Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description doc
API documentation for CVC3.

%package java
Summary:	Java interface for CVC3
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	java
Requires:	jpackage-utils

%description java
Java interface for CVC3.

%prep
%setup -q
%patch0

# Use the appropriate compiler flags
sed -e "s|^  LOCAL_CXXFLAGS = -O2|  LOCAL_CXXFLAGS =|" \
    -e "s|^LOCAL_CXXFLAGS += -Wall|LOCAL_CXXFLAGS +=|" \
    -i Makefile.std

# We can't use loadLibrary, since the JNI libaries are not in a standard place
sed -i \
 "s|loadLibrary(\"cvc3jni\")|load(\"%{_libdir}/%{name}/libcvc3jni.so\")|" \
 java/src/cvc3/Embedded.java

# Get rid of an unused direct shared library dependency
sed -i "s|-lcvc3 \$(LD_LIBS)|-Wl,--as-needed -lcvc3 \$(LD_LIBS)|" java/Makefile

%build
%configure \
	--with-build=optimized \
	--enable-dynamic \
	--enable-java \
	--disable-zchaff \
	--with-java-home=%{java_home}

%{__make}

# Build the documentation
%{__make} -C doc
rm -f doc/html/*.{map,md5}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

%{__make} install \
	datarootdir=$RPM_BUILD_ROOT%{_datadir} \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	incdir=$RPM_BUILD_ROOT%{_includedir}/%{name} \
	javadir=$RPM_BUILD_ROOT%{_libdir}/%{name}

# Add missing executable bits to the shared libraries
chmod a+x $RPM_BUILD_ROOT%{_libdir}/*.so.*

# Move the JNI libraries to the right place
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libcvc3jni.* $RPM_BUILD_ROOT%{_libdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc INSTALL LICENSE PEOPLE README
%attr(755,root,root) %{_bindir}/cvc3
%{_libdir}/libcvc3.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/cvc3
%{_libdir}/*.so
%{_pkgconfigdir}/%{name}.pc

%files doc
%defattr(644,root,root,755)
%doc doc/html

%files java
%defattr(644,root,root,755)
%{_libdir}/%{name}
