# SOFAH Port Spoof Service

The Port Spoof service is a key component of the SOFAH (Speedy Open Framework for Automated Honeypot-development) framework, designed to enhance the honeypot's realism by emulating open ports and services. This service deceives network scanners and attackers into believing various services are running on the honeypot, thereby increasing the honeypot's interaction with potential threats.

## Overview

Port Spoofing plays a critical role in the SOFAH ecosystem by simulating the presence of services across a wide range of ports. This not only diverts attackers from real services but also gathers intelligence on attempted interactions. The service operates by dynamically responding to port scans and access attempts with configured or randomized responses, mimicking real service behaviors.

## Features

- **Dynamic Response Emulation**: Mimics responses from various services to deceive port scanners and manual probing attempts.
- **Configurable Port Responses**: Allows for customized responses per port, enhancing the honeypot's simulation capabilities.
- **Integration with ENNORM**: Works seamlessly with the ENNORM module for automated deployment and configuration based on reconnaissance data.


