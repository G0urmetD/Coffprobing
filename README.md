# Coffprobing
Coffprobing is a small python tool to check the http status code of several urls

```bash

   ______      ________                 __    _
  / ____/___  / __/ __/___  _________  / /_  (_)___  ____ _
 / /   / __ \/ /_/ /_/ __ \/ ___/ __ \/ __ \/ / __ \/ __ `/
/ /___/ /_/ / __/ __/ /_/ / /  / /_/ / /_/ / / / / / /_/ /
\____/\____/_/ /_/ / .___/_/   \____/_.___/_/_/ /_/\__, /
                  /_/                             /____/   1.2.2
                                                           G0urmetD


[INF] Coffprobing has the [latest] version: 1.2.2 ...
usage: coffprobing.py [-h] [-mt MASS_TARGET] [-fc FILTER_CODE] [-r RATE_LIMIT] [-u]

Coffprobing - Subdomain URL checker

options:
  -h, --help            show this help message and exit
  -mt MASS_TARGET, --mass-target MASS_TARGET
                        Path to file containing subdomains
  -fc FILTER_CODE, --filter-code FILTER_CODE
                        Filter specific HTTP codes in the output
  -r RATE_LIMIT, --rate-limit RATE_LIMIT
                        Requests per second (default: 10)
  -u, --update          Update the tool to the latest version
```
