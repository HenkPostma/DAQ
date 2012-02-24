bin_PROGRAMS = ain
ain_SOURCES = ain.c common.c examples.h

# set the include path found by configure
INCLUDES = -lm -Icomedi $(all_includes)

# the library search path.
ain_LDFLAGS = $(all_libraries) 
ain_LDADD = -lcomedi -lm
