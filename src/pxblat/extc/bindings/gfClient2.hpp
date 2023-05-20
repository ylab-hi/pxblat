// * gfClient - A client for the genomic finding program that produces a .psl file. */
/* Copyright 2001-2003 Jim Kent.  All rights reserved. */
#include "aliType.h"
#include "common.h"
#include "errCatch.h"
#include "fa.h"
#include "fuzzyFind.h"
#include "genoFind.h"
#include "gfClient.hpp"
#include "linefile.h"
#include "options.h"
#include "portable.h"
#include "psl.h"

namespace cppbinding2 {
using namespace cppbinding;

std::string pygfClient2(gfClientOption &option);
}  // namespace cppbinding2
