FROM alpine:3.17
# Define build-time variables
ARG POOF_PORT 
ARG POOF_MODE
ARG POOF_BANNER
ARG TOKEN
ARG LOG_API

# Set the build-time variable as an environment variable
ENV POOF_PORT=${POOF_PORT}
ENV POOF_MODE=${POOF_MODE}
ENV POOF_BANNER=${POOF_BANNER}
ENV LOG_API=${LOG_API}

# Copy files
COPY ./src /home/poof/

# Update apt repository and install dependencies
RUN apk --no-cache -U add \
    python3 \
    py3-pip \
    git \
    python3-dev && \
    addgroup -g 2000 poof && \
    adduser -S -s /bin/ash -u 2000 -D -g 2000 poof && \
    chown poof:poof -R /home/poof/* && \
    pip3 install git+https://$TOKEN:x-oauth-basic@github.com/sofahd/sofahutils.git

WORKDIR /home/poof
USER poof:poof

CMD python3 PortSpoof.py -p 65100 -m "$POOF_MODE" -b "$POOF_BANNER" -i "$POOF_PORT" -l "$LOG_API"


