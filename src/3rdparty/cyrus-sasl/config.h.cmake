#ifndef CONFIG_H
#define CONFIG_H
/* Name of package */
#cmakedefine PACKAGE "@PACKAGE@"

#cmakedefine VERSION "@VERSION@"

/* Do we have a getnameinfo() function? */
#cmakedefine HAVE_GETNAMEINFO 1

/* Do we have a getaddrinfo() function? */
#cmakedefine HAVE_GETADDRINFO 1

/* Do we have a getpid() function? */
#cmakedefine HAVE_GETPID 1

/* Do we have a gettimeofday() function? */
#cmakedefine HAVE_GETTIMEOFDAY 1

/* Do we have a gettimeofday() function? */
#cmakedefine HAVE_SNPRINTF 1

/* Do we have a socklen_t? */
#undef HAVE_SOCKLEN_T
#ifndef HAVE_SOCKLEN_T
typedef unsigned int socklen_t;
#endif /* HAVE_SOCKLEN_T */

/* define if your compiler has __attribute__ */
#cmakedefine HAVE___ATTRIBUTE__ 1
#ifndef HAVE___ATTRIBUTE__
/* Can't use attributes... */
#define __attribute__(foo)
#endif

#cmakedefine HAVE_SYS_SOCKET_H 1
#ifdef HAVE_SYS_SOCKET_H
  #include <sys/socket.h>
#endif

#cmakedefine HAVE_SYSLOG 1

#cmakedefine HAVE_TIME_H 1

#cmakedefine HAVE_UNISTD_H 1

#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

/* Defined in RFC 1035. max strlen is only 253 due to length bytes. */
#ifndef MAXHOSTNAMELEN
# define MAXHOSTNAMELEN  255
#endif

/* Runtime plugin location */
#cmakedefine PLUGINDIR "@PLUGINDIR@"
#cmakedefine CONFIGDIR "@CONFIGDIR@"

#ifndef HAVE_GETADDRINFO
#define	getaddrinfo	sasl_getaddrinfo
#define	freeaddrinfo	sasl_freeaddrinfo
#define	gai_strerror	sasl_gai_strerror
#endif

#ifndef HAVE_GETNAMEINFO
#define	getnameinfo	sasl_getnameinfo
#endif

#if !defined(HAVE_GETNAMEINFO) || !defined(HAVE_GETADDRINFO)
#include "gai.h"
#endif

#ifndef AI_NUMERICHOST   /* support glibc 2.0.x */
#define AI_NUMERICHOST  4
#define NI_NUMERICHOST  2
#define NI_NAMEREQD     4
#define NI_NUMERICSERV  8
#endif

#ifndef WIN32
# include <netdb.h>
# ifdef HAVE_SYS_PARAM_H
#  include <sys/param.h>
# endif
#else /* WIN32 */
# include <winsock2.h>
# ifndef strncasecmp
#  define strncasecmp strnicmp
# endif
# ifndef strcasecmp
#  define strcasecmp stricmp
# endif
# ifndef snprintf
#  define snprintf _snprintf
# endif

/* Registry key that contains the locations of the plugins */
# define SASL_ROOT_KEY "SOFTWARE\\Carnegie Mellon\\Project Cyrus\\SASL Library"
# define SASL_PLUGIN_PATH_ATTR "SearchPath"
# define SASL_CONF_PATH_ATTR "ConfFile"

#endif /* WIN32 */

#ifndef HIER_DELIMITER
# define HIER_DELIMITER @HIER_DELIMITER@
#endif
#endif
