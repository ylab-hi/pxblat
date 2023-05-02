/* Connect via https. */

#ifndef NET_HTTPS_H
#define NET_HTTPS_H


#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus



int netConnectHttps(char *hostName, int port, boolean noProxy);
/* Return socket for https connection with server or -1 if error. */


#ifdef __cplusplus
}
#endif  // __cplusplus


#endif//ndef NET_HTTPS_H
