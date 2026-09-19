# Config (global ARGs; each stage re-declares the ones it uses)
ARG BRANCH="master"
# Ubuntu 22.04 ships clang 15 natively, so no external LLVM apt repository is needed.
ARG CLANG_VERSION=15

FROM ubuntu:22.04 AS base
ARG CLANG_VERSION

# Run dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -yq "clang-${CLANG_VERSION}" \
 && rm -rf /var/lib/apt/lists/*


# Build binder
FROM base AS build
ARG CLANG_VERSION
ARG BRANCH

# Build dependencies
RUN apt-get update
RUN apt-get install -yq \
	"libclang-${CLANG_VERSION}-dev" \
	cmake \
	git \
    build-essential \
    zlib1g-dev \
    libhts-dev \
    libssl-dev

# Clone binder source
ARG REPO="https://github.com/RosettaCommons/binder.git"
RUN git clone --depth 1 --branch "${BRANCH}" "${REPO}" /binder

# Build
WORKDIR "/build"
RUN cmake \
	-DCMAKE_CXX_COMPILER="$(which clang++-"${CLANG_VERSION}")" \
	-DBINDER_ENABLE_TEST=OFF \
	/binder
RUN make "-j$(nproc)"
RUN make install


# Install image
FROM base AS install
COPY --from=build /usr/local/bin/binder /usr/local/bin/binder
