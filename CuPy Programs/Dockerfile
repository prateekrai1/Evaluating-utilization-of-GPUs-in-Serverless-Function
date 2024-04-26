FROM ghcr.io/openfaas/classic-watchdog:0.2.3 as watchdog

FROM cupy/cupy:latest

RUN mkdir -p /home/app

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

#RUN apt-get install python

RUN apt-get update && apt-get install -y python3
RUN python3 -V
# Add non root user
#RUN addgroup -S app && adduser app -S -G app
RUN groupadd -r app && useradd -r -g app app

RUN chown app /home/app

COPY index.py /home/app

WORKDIR /home/app

USER app

# Populate example here - i.e. "cat", "sha512sum" or "node index.js"
ENV fprocess="python3 index.py"
# Set to true to see request in function logs
ENV write_debug="true"

EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]